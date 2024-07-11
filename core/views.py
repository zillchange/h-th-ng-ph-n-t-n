
import db
from fastapi import APIRouter,Request,status,Response,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from .models import user_avatar
from ultils import file_path_default,settings
from datetime import datetime
from authentication.models import User,get_current_user_from_cookie,get_current_user_from_token
core_bp = APIRouter()
templates = Jinja2Templates(directory="templates")

@core_bp.get("/authorizationUser",tags=['authentication'])
async def authorizationUser(request:Request,response:Response,current_user: User = Depends(get_current_user_from_token)):
    conn=db.connection()
    cursor=conn.cursor()
    sql="select * from profileuser where idaccount=%s"
    value=(current_user.id,)
    cursor.execute(sql,value)
    user_temp=cursor.fetchone()
    
    #   set image path
    image_path_value=None
    found_avatar = user_avatar.find_picture_name_by_id(current_user.idprofile)
    if found_avatar and found_avatar[2] != "":
        response.set_cookie(key="image_path_session", value=str(found_avatar[2]))
        image_path_value=found_avatar[2]
    else:
        image_path_value=file_path_default
        response.set_cookie(key="image_path_session", value=file_path_default)
    
    fullname_value=user_temp[1]
    response.set_cookie(key="fullname_session", value=str(user_temp[1]))
        
    conn=db.connection()
    cursor=conn.cursor()
    sql="insert into calendar(checkin,idaccount) values(%s,%s)"
    value=(datetime.now(),user_temp[0],)
    cursor.execute(sql,value)
    conn.commit()
    conn.close()
    new_id = cursor.lastrowid
        
    if current_user.rolename=="employee":
        response=RedirectResponse(url="/home",status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="checkinid", value=new_id)
        response.set_cookie(key="roleuser", value="employee")
        response.set_cookie(key="image_path_session", value=image_path_value)
        response.set_cookie(key="fullname_session", value=fullname_value)
        return response
        
        

    elif current_user.rolename=="manager":
        response= RedirectResponse(url='/home')
        response.set_cookie(key="checkinid", value=new_id)
        response.set_cookie(key="roleuser", value="manager")
        response.set_cookie(key="image_path_session", value=image_path_value)
        response.set_cookie(key="fullname_session", value=fullname_value)
        return response
    else:
        return "You have not been granted access to the resource"

@core_bp.get("/logout",tags=['user'], response_class=HTMLResponse)
def logout_get(request:Request):
    response = RedirectResponse(url="/")
    response.delete_cookie(settings.COOKIE_NAME)
    response.delete_cookie('roleuser')
    response.delete_cookie('rolemanager')
    response.delete_cookie('image_path_manager')
    response.delete_cookie('fullname_manager')
    response.delete_cookie('image_path_session')
    response.delete_cookie('fullname_session')

    conn=db.connection()
    cursor=conn.cursor()
    sql="update calendar set checkout=%s where id=%s"
    value=(datetime.now(),int(request.cookies.get("checkinid")),)
    cursor.execute(sql,value)
    conn.commit()
    conn.close()
    return response

@core_bp.get("/home",tags=['user'], response_class=HTMLResponse)
async def home(request:Request,current_user: User = Depends(get_current_user_from_token)):

    context={
        "request":request,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "current_user":current_user
    }
    return templates.TemplateResponse("core/homepage.html",context)


@core_bp.get("/calendarcheckin",tags=['user'], response_class=HTMLResponse)
async def calendarcheckin(request:Request,current_user: User = Depends(get_current_user_from_token)):
    conn=db.connection()
    cursor=conn.cursor()
    sql="select * from calendar where checkout is not null and idaccount=%s"
    value=(current_user.id,)
    cursor.execute(sql,value)
    calendar_temp=cursor.fetchall()
    conn.commit()
    conn.close()
    calendar = []
    checkin = []

    for temp in calendar_temp:
        total = temp[2] - temp[1]
        total_seconds = total.total_seconds()
        
        if temp[1].date() not in calendar:
            calendar.append(temp[1].date())
            checkin.append([temp[0], temp[1], temp[2], total_seconds])  # Sử dụng danh sách thay vì tuple
        else:
            for a in checkin:
                if a[1].date() == temp[1].date():
                    a[3] = total_seconds + a[3]
                                        
        # hours = int(total_seconds // 3600)
        # minutes = int((total_seconds % 3600) // 60)
        # seconds = int(total_seconds % 60)
        # totalstring=hours+":"+minutes+":"+seconds
    checkinstring=[]
    for i in checkin:
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        totalstring=str(hours)+":"+str(minutes)+":"+str(seconds)
        checkinstring.append((i[0],i[1].date().strftime("%Y-%m-%d"),i[2].date().strftime("%Y-%m-%d"),totalstring))
    context={
        "request":request,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "checkinstring":checkinstring,
        "current_user":current_user
    }
    return templates.TemplateResponse("core/calendarcheckin.html",context)

        