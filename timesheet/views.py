import db
from fastapi import APIRouter,Request,status,Response,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
from authentication.models import User,get_current_user_from_cookie,get_current_user_from_token
from datetime import datetime
timesheet = APIRouter()
templates = Jinja2Templates(directory="templates")


@timesheet.get("/updatetimesheet",tags=["timesheet"], response_class=HTMLResponse)
async def timesheet_get(request: Request,current_user: User = Depends(get_current_user_from_token)):
    conn=db.connection()
    cursor=conn.cursor()
    sql="select * from timesheet where idprofile=%s"
    cursor.execute(sql,(current_user.idprofile,))
    timesheet_temp=cursor.fetchall()
    conn.commit()
    conn.close()
    timesheets=[(timesheetv[0],timesheetv[1],timesheetv[2],timesheetv[4])for timesheetv in timesheet_temp]
    context={
        "request":request,
        "roleuser":"employee",
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "timesheets":timesheets,
        "is_authenticated":1,
        "current_user":current_user
    }
    return templates.TemplateResponse("timesheet/timesheet.html",context)

@timesheet.post("/updatetimesheet",tags=["timesheet"], response_class=HTMLResponse)
async def timesheet_post(request: Request,current_user: User = Depends(get_current_user_from_token)):
    form_method= await request.form()
    if "addtimesheet" in form_method and form_method.get("addtimesheet")=="addtimesheet":
        return RedirectResponse(url=f"/addtimesheet",status_code=status.HTTP_302_FOUND)
    elif "submittimsheet" in form_method and form_method.get("submittimsheet")=="submittimsheet": 
        selecttiontasks=form_method.getlist('checkbox')
        for id in selecttiontasks:
            submittimesheet(id)
        return RedirectResponse(url="/updatetimesheet",status_code=status.HTTP_302_FOUND)
    elif "removetimesheet" in form_method and form_method.get("removetimesheet")=="removetimesheet": 
        selecttiontasks=form_method.getlist('checkbox')
        for id in selecttiontasks:
            removetimesheet(id)
        return RedirectResponse(url="/updatetimesheet",status_code=status.HTTP_302_FOUND)
    elif "recalltimesheet" in form_method and form_method.get("recalltimesheet")=="recalltimesheet": 
        selecttiontasks=form_method.getlist('checkbox')
        for id in selecttiontasks:
            recalltimesheet(id)
        return RedirectResponse(url="/updatetimesheet",status_code=status.HTTP_302_FOUND)


@timesheet.get("/addtimesheet",tags=["timesheet"], response_class=HTMLResponse)
async def addtimesheet_get(request: Request,current_user: User = Depends(get_current_user_from_token)):
    context={
        "request":request,
        "roleuser":"employee",
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "current_user":current_user
    }
    return templates.TemplateResponse("timesheet/addtimesheet.html",context)


@timesheet.post("/addtimesheet",tags=["timesheet"], response_class=HTMLResponse)
async def addtimesheet(request: Request,current_user: User = Depends(get_current_user_from_token)):
    form=await request.form()
    conn=db.connection()
    cursor=conn.cursor()
    sql="insert into timesheet(updatedate,hours,idprofile,status)values(%s,%s,%s,'created') "
    cursor.execute(sql,(form["date"],form["hours"],current_user.idprofile,))
    conn.commit()
    conn.close()
    return RedirectResponse(url=f"/updatetimesheet",status_code=status.HTTP_302_FOUND) 
    
def submittimesheet(id):
    conn=db.connection()
    cursor=conn.cursor()
    sql="update timesheet set status='pending aproval' where id=%s and status='created' or id=%s and status ='pending approval'"
    cursor.execute(sql,(id,id,))
    conn.commit()
    conn.close()

def removetimesheet(id):
    conn=db.connection()
    cursor=conn.cursor()
    sql="delete from timesheet where id=%s and status='created' or id=%s and status ='pending approval' or id=%s and status ='unapproval'"
    cursor.execute(sql,(id,id,id,))
    conn.commit()
    conn.close()

def recalltimesheet(id):
    conn=db.connection()
    cursor=conn.cursor()
    sql="update timesheet set status='recall' where id=%s and status='approval'"
    cursor.execute(sql,(id,))
    conn.commit()
    conn.close()


@timesheet.get("/timesheetview",tags=["timesheet"], response_class=HTMLResponse)
async def timesheetview_get(request: Request,current_user: User = Depends(get_current_user_from_token)):
    conn=db.connection()
    cursor=conn.cursor()
    sql="select t.id,p.fullname,t.updatedate,t.hours,t.status from timesheet t join profileuser p on p.id=t.idprofile"
    cursor.execute(sql,)
    timesheet_temp=cursor.fetchall()
    conn.commit()
    conn.close()
    timesheets=[(timesheetv[0],timesheetv[1],timesheetv[2],timesheetv[3],timesheetv[4])for timesheetv in timesheet_temp]
    context={
        "request":request,
        "roleuser":"manager",
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "timesheets":timesheets,
        "is_authenticated":1,
        "current_user":current_user
    }
    return templates.TemplateResponse("timesheet/timesheetview.html",context)

@timesheet.post("/timesheetview",tags=["timesheet"], response_class=HTMLResponse)
async def timesheetview(request: Request,current_user: User = Depends(get_current_user_from_token)):
    form_method=await request.form()
    if "approvals" in form_method and form_method.get('approvals')=="approvals":
        sellectionItem=form_method.getlist("checkbox")
        approvaltimesheet(sellectionItem)
        return RedirectResponse(url=f"/timesheetview",status_code=status.HTTP_302_FOUND)
    elif "pendingapprovals" in form_method and form_method.get('pendingapprovals')=="pendingapprovals":
        sellectionItem=form_method.getlist("checkbox")
        pendingapprovaltimesheet(sellectionItem)
        return RedirectResponse(url=f"timesheetview",status_code=status.HTTP_302_FOUND)
    

def approvaltimesheet(selectionItem):
    for item in selectionItem:
        conn=db.connection()
        cursor=conn.cursor()
        sql="select status from timesheet where id=%s"
        cursor.execute(sql,(item,))
        status=cursor.fetchone()
        conn.commit()
        conn.close()
        if status[0]=="recall":
            conn=db.connection()
            cursor=conn.cursor()
            sql="update timesheet set status='pending approval' where id=%s"
            cursor.execute(sql,(item,))
            conn.commit()
            conn.close()
        else:
            conn=db.connection()
            cursor=conn.cursor()
            sql="update timesheet set status='approval' where id=%s"
            cursor.execute(sql,(item,))
            conn.commit()
            conn.close()

def pendingapprovaltimesheet(selectionItem):
    for item in selectionItem:
        conn=db.connection()
        cursor=conn.cursor()
        sql="select status from timesheet where id=%s"
        cursor.execute(sql,(item,))
        status=cursor.fetchone()
        conn.commit()
        conn.close()
        if status[0]=="recall":
            conn=db.connection()
            cursor=conn.cursor()
            sql="update timesheet set status='approval' where id=%s"
            cursor.execute(sql,(item,))
            conn.commit()
            conn.close()
        else:
            conn=db.connection()
            cursor=conn.cursor()
            sql="update timesheet set status='unapproval' where id=%s"
            cursor.execute(sql,(item,))
            conn.commit()
            conn.close()
