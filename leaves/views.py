import db
from fastapi import APIRouter,Request,status,Response,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
from authentication.models import User,get_current_user_from_cookie,get_current_user_from_token
from datetime import datetime
leave = APIRouter()
templates = Jinja2Templates(directory="templates")

@leave.get("/requestemployee",tags=['Leave management'], response_class=HTMLResponse)
async def requestemployee(request:Request,current_user: User = Depends(get_current_user_from_token)):
    current_date = datetime.now()

    # Lấy tháng và năm hiện tại
    #current_month = current_date.month
    current_year = current_date.year
    return RedirectResponse(url=f"/request/{current_year}/all",status_code=status.HTTP_302_FOUND)



@leave.get("/request/{year}/{type}",tags=["leave"], response_class=HTMLResponse)
async def request_get(request: Request,year,type,current_user: User = Depends(get_current_user_from_token)):
    projects=[]
    projects.append((0,'all'))
    conn=db.connection()
    cursor=conn.cursor()
    sql="select * from project"
    cursor.execute(sql)
    project_temp=cursor.fetchall()
    conn.commit()
    conn.close()

    for project in project_temp:
        projects.append((project[0],project[1]))
    if type=='all':
        conn=db.connection()
        cursor=conn.cursor()
        sql="""

    select ur.id,p.projecttype,l.task,ur.startdate,ur.enddate,ur.reason,ur.status
    from user_request ur join leave_off l on l.id=ur.idtask join project p on l.projectid=p.id
    join profileuser pr on pr.id=ur.idprofile where ur.idprofile=%s 
    """
        value=(current_user.idprofile,)
        cursor.execute(sql,value)
        leave_temp=cursor.fetchall()
        conn.commit()
        conn.close()
    else:
        conn=db.connection()
        cursor=conn.cursor()
        sql="""

    select ur.id,p.projecttype,l.task,ur.startdate,ur.enddate,ur.reason,ur.status
    from user_request ur join leave_off l on l.id=ur.idtask join project p on l.projectid=p.id
    join profileuser pr on pr.id=ur.idprofile where ur.idprofile=%s and p.projecttype=%s
    """
        value=(current_user.idprofile,type,)
        cursor.execute(sql,value)
        leave_temp=cursor.fetchall()
        conn.commit()
        conn.close()
    leaves=[(leave[0],leave[1],leave[2],leave[3],leave[4],leave[5],leave[6])for leave in leave_temp]
    context={
        "request":request,
        "roleuser":"employee",
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "leaves":leaves,
        "projects":projects,
        "is_authenticated":1,
        "current_user":current_user,
        "year":year
    }
    return templates.TemplateResponse("leave/leave.html",context)

@leave.post("/request/{year}/{type}",tags=["leave"], response_class=HTMLResponse)
async def request_post(request: Request,year,type,current_user: User = Depends(get_current_user_from_token)):
    form_method=await request.form()
    
    if "yearform" in form_method and form_method.get("yearform")=="yearform":
        return RedirectResponse(url=f"/request/{form_method.get("year")}/{type}",status_code=status.HTTP_302_FOUND)
    elif "find" in form_method and form_method.get("find")=="find":
        return RedirectResponse(url=f"/request/{year}/{form_method["projecttype"]}",status_code=status.HTTP_302_FOUND)
    elif "addleave" in form_method and form_method.get("addleave")=="addleave":
        return RedirectResponse(url=f"/request_addtask/{year}/{type}",status_code=status.HTTP_302_FOUND)
    elif 'removeleave' in form_method and form_method['removeleave']=='removeleave':
        selecttiontasks=form_method.getlist('checkbox')
        
        for select in selecttiontasks:
            removeleaves(select)
        return RedirectResponse(url=f"/request/{year}/{type}",status_code=status.HTTP_302_FOUND)
    elif 'submitleave'in form_method and form_method.get('submitleave')=='submitleave':
        selecttiontasks=form_method.getlist('checkbox')
        for id in selecttiontasks:
            submitleaves(id)
        return RedirectResponse(url=f"/request/{year}/{type}",status_code=status.HTTP_302_FOUND)

@leave.post('/get_task',tags=['leave'])
async def get_task(request:Request):
    form=await request.form()
    selected_project = form['selected_project']
    conn=db.connection()
    cursor=conn.cursor()
    sql="select l.* from leave_off l join project p on p.id=l.projectid where  l.projectid=%s"
    cursor.execute(sql,(selected_project,))
    task_temp=cursor.fetchall()
    conn.commit()
    conn.close()
    tasks_options=[(task[0],task[1])for task in task_temp]
    
    return JSONResponse(content={'tasks':tasks_options})

@leave.get("/request_addtask/{year}/{type}",tags=['Leave'],status_code=status.HTTP_302_FOUND)
async def addtask_get(request:Request,year,type,current_user: User = Depends(get_current_user_from_token)): 
    conn=db.connection()
    cursor=conn.cursor()
    sql="select * from project"
    cursor.execute(sql)
    project_temp=cursor.fetchall()
    projects=[(project[0],project[1])for project in project_temp]
    conn=db.connection()
    cursor=conn.cursor()
    sql="select l.* from leave_off l join project p on p.id=l.projectid where  l.projectid=%s"
    cursor.execute(sql,(projects[0][0],))
    task_temp=cursor.fetchall()
    conn.commit()
    conn.close()
    tasks=[(task[0],task[1])for task in task_temp]
    context={
        "request":request,
        "roleuser":"employee",
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "projects":projects,
        "tasks":tasks,
        "is_authenticated":1,
        "current_user":current_user,
        "year":year
    }
    return templates.TemplateResponse("leave/addleave.html",context)

@leave.post("/request_addtask/{year}/{type}",tags=['Leave'],status_code=status.HTTP_302_FOUND)
async def addtask(request:Request,year,type,current_user: User = Depends(get_current_user_from_token)):
    form_method=await request.form() 
    startdate = datetime.strptime(form_method['startdate'], '%Y-%m-%d')
    enddate = datetime.strptime(form_method['enddate'], '%Y-%m-%d')
    conn=db.connection()
    cursor=conn.cursor()
    sql="insert into user_request(idtask,idprofile,startdate,enddate,reason,status)values(%s,%s,%s,%s,%s,'created')"
    value=(form_method['task'],current_user.idprofile,startdate,enddate,form_method["reason"],)
    cursor.execute(sql,value)
    conn.commit()
    conn.close()
    return RedirectResponse(url=f"/request/{year}/{type}",status_code=status.HTTP_302_FOUND)


def removeleaves(leaveid):
    conn=db.connection()
    cursor=conn.cursor()
    sql="delete from user_request where id=%s and status!='aproval'"
    cursor.execute(sql,(leaveid,))
    conn.commit()
    conn.close()

def submitleaves(leaveid):
    conn=db.connection()
    cursor=conn.cursor()
    sql="update user_request set status='pending aproval' where id=%s and status!='aproval'"
    cursor.execute(sql,(leaveid,))
    conn.commit()
    conn.close()

@leave.get("/annualleaveadmin_view/{type}",tags=['Leave'],status_code=status.HTTP_302_FOUND)
async def annualleaveadmin_view_get(request:Request,type,current_user: User = Depends(get_current_user_from_token)): 
    projects=[]
    projects.append((0,'all'))
    conn=db.connection()
    cursor=conn.cursor()
    sql="select * from project"
    cursor.execute(sql)
    project_temp=cursor.fetchall()
    conn.commit()
    conn.close()

    for project in project_temp:
        projects.append((project[0],project[1]))
    if type=='all':
        conn=db.connection()
        cursor=conn.cursor()
        sql="""
        select ur.id,pr.fullname ,p.projecttype,l.task,ur.startdate,ur.enddate,ur.reason,ur.status
    from user_request ur join leave_off l on l.id=ur.idtask join project p on l.projectid=p.id
    join profileuser pr on pr.id=ur.idprofile where ur.status!='created'"""
        cursor.execute(sql)
        leave_temp=cursor.fetchall()
        conn.commit()
        conn.close() 
    else:
        conn=db.connection()
        cursor=conn.cursor()
        sql="""
        select ur.id,pr.fullname ,p.projecttype,l.task,ur.startdate,ur.enddate,ur.reason,ur.status
    from user_request ur join leave_off l on l.id=ur.idtask join project p on l.projectid=p.id
    join profileuser pr on pr.id=ur.idprofile where ur.status!='created' and p.projecttype=%s"""
        cursor.execute(sql,(type,))
        leave_temp=cursor.fetchall()
        conn.commit()
        conn.close()
    leaves=[(leave[0],leave[1],leave[2],leave[3],leave[4],
             leave[5],leave[6],leave[7])for leave in leave_temp]
    context={
        "request":request,
        "roleuser":"manager",
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "leaves":leaves,
        "projects":projects,
        "is_authenticated":1,
        "current_user":current_user
    }
    return templates.TemplateResponse("leave/annualleaveadminview.html",context)

@leave.post("/annualleaveadmin_view/{type}",tags=['leave'],status_code=status.HTTP_302_FOUND)
async def annualleaveadmin_view(request:Request,type,current_user: User = Depends(get_current_user_from_token)): 
    form_method=await request.form()
    if "approvals" in form_method and form_method.get('approvals')=="approvals":
        sellectionItem=form_method.getlist("checkbox")
        approvaldayoff(sellectionItem)
        return RedirectResponse(url=f"/annualleaveadmin_view/{type}",status_code=status.HTTP_302_FOUND)
    elif "pendingapprovals" in form_method and form_method.get('pendingapprovals')=="pendingapprovals":
        sellectionItem=form_method.getlist("checkbox")
        pendingapprovaldayoff(sellectionItem)
        return RedirectResponse(url=f"/annualleaveadmin_view/{type}",status_code=status.HTTP_302_FOUND)
    elif "find" in form_method and form_method.get('find')=="find":
        return RedirectResponse(url=f"/annualleaveadmin_view/{form_method["projecttype"]}",status_code=status.HTTP_302_FOUND)


def approvaldayoff(selectionItem):
    for item in selectionItem:
        conn=db.connection()
        cursor=conn.cursor()
        sql="update user_request set status='approval' where id=%s"
        cursor.execute(sql,(item,))
        conn.commit()
        conn.close()

def pendingapprovaldayoff(selectionItem):
    for item in selectionItem:
        conn=db.connection()
        cursor=conn.cursor()
        sql="update user_request set status='unapproval' where id=%s"
        cursor.execute(sql,(item,))
        conn.commit()
        conn.close()
