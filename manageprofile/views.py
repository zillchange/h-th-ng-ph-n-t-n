import db
from fastapi import APIRouter,Request,status, Form, Response,Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
from authentication.models import User,get_current_user_from_cookie,get_current_user_from_token
from datetime import datetime

manageprofile = APIRouter()
templates = Jinja2Templates(directory="templates")

@manageprofile.get("/profile", tags=["manageProfile"], response_class=HTMLResponse)
async def displayAllProfile(request: Request,current_user: User = Depends(get_current_user_from_token)):
    
    role = request.cookies.get("roleuser")
    conn = db.connection()
    cursor = conn.cursor()
    sql = " "
    if role == "manager":
        sql = "select * from profileuser"
        cursor.execute(sql)
    elif role == "employee":
        sql = "select * from profileuser where id = %s"
        id = (current_user.id,)
        cursor.execute(sql,id)
    
    # sql = "select * from profileuser"
    
    profiles = cursor.fetchall()
    conn.commit()
    conn.close()

    context = {
        "request": request,
        "profiles": profiles,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "current_user":current_user
    }
    
    return templates.TemplateResponse("manageprofile/displayAllProfiles.html",context)

@manageprofile.get("/updateProfile", tags=["manageProfile"],response_class=HTMLResponse)
async def displayCurrentProfile(request:Request,profileId: int, current_user: User = Depends(get_current_user_from_token)):
    conn = db.connection()
    cursor = conn.cursor()
    sql = "select * from profileuser where id= %s"
    id = (profileId,)
    cursor.execute(sql,id)
    profiles = cursor.fetchall()

    context = {
        "request": request,
        "profileId":profileId,
        "profiles": profiles,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "current_user":current_user
    }
    return templates.TemplateResponse("manageprofile/updateProfile.html",context)

@manageprofile.get("/viewProfile", tags=["manageProfile"],response_class=HTMLResponse)
async def displayCurrentProfile(request:Request,profileId: int, current_user: User = Depends(get_current_user_from_token)):
    conn = db.connection()
    cursor = conn.cursor()
    sql = "select * from profileuser where id= %s"
    id = (profileId,)
    cursor.execute(sql,id)
    profiles = cursor.fetchall()
    conn.commit()
    conn.close()
    context = {
        "request": request,
        "profileId":profileId,
        "profiles": profiles,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "current_user":current_user
    }
    return templates.TemplateResponse("manageprofile/viewProfile.html",context)

# @manageprofile.post("/requestUpdate",tags=["manageProfile"],response_class=HTMLResponse)
# async def requestUpdate(request: Request,current_user: User = Depends(get_current_user_from_token)):
#     form_method = await request.form()


@manageprofile.post("/saveProfile",tags=["manageProfile"],status_code=status.HTTP_302_FOUND)
async def updateProfile(
    request: Request,
    profileId: int = Form(...),
    fullname: str = Form(...),
    nationalId: str = Form(...),
    taxnumber: str = Form(...),
    phonenumber: str = Form(...),
    address: str = Form(...),
    bankcode: str = Form(...),
    bankname: str = Form(...),
    current_user: User=Depends(get_current_user_from_token)
    ):
    conn = db.connection()
    cursor = conn.cursor()
    sql = "update profileuser set fullname = %s, cccd = %s, tax = %s, phone = %s, address = %s, bankcode = %s, bankname = %s where id = %s"
    value = (fullname,nationalId,taxnumber,phonenumber,address,bankcode,bankname,profileId,)
    cursor.execute(sql,value)
    conn.commit()
    conn.close()
    return RedirectResponse(url="/profile",status_code=status.HTTP_302_FOUND)

@manageprofile.get("/createAccount",tags=["manageProfile"],response_class=HTMLResponse)
async def displayCreateAccountForm(request:Request,current_user: User = Depends(get_current_user_from_token)):
    conn = db.connection()
    cursor = conn.cursor()
    sql = "select * from roleuser"
    cursor.execute(sql)
    roleusers = cursor.fetchall()
    context = {
        "request": request,
        "roleusers": roleusers,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "current_user":current_user
    }
    return templates.TemplateResponse("manageprofile/createAccount.html",context)

# checking whether registeredEmail has already existed 
@manageprofile.post("/checkEmail",tags=["manageProfile"])
async def checkEmail(request: Request):
    data = await request.json()
    email = data.get("email")

    conn = db.connection()
    cursor = conn.cursor()
    sql = "select * from account where email = %s"
    value = (email,)
    cursor.execute(sql,value)
    check = cursor.fetchone()
    conn.commit()
    conn.close()
    if check:
        raise HTTPException(status_code=400, detail="Email already exists")
    return {"detail": "Email is available"}

@manageprofile.post("/createAccount",tags=["manageProfile"])
async def addNewAccount(
    request:Request,
    current_user: User=Depends(get_current_user_from_token)
    ):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")
    conn = db.connection()
    cursor = conn.cursor()
    sql = "insert into account(email,password,created_date,role_id) values (%s,%s,curdate(),%s)"
    value = (email,password,role,)
    cursor.execute(sql,value)
    conn.commit()
    conn.close()
    

@manageprofile.get("/addProfile",tags=["manageProfile"],response_class=HTMLResponse)
async def displayAddProfileForm(request:Request,current_user: User = Depends(get_current_user_from_token)):
    conn = db.connection()
    cursor = conn.cursor()
    sql = "select * from account where id not in (select idaccount from profileuser) order by id desc"
    cursor.execute(sql)
    emails = cursor.fetchall()
    conn.commit()
    conn.close()
    context = {
        "request": request,
        "emails": emails,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "current_user":current_user
    }
    return templates.TemplateResponse("manageprofile/addProfile.html",context)

@manageprofile.post("/addProfile",tags=["manageProfile"],status_code=status.HTTP_302_FOUND)
async def addProfile(request:Request,
                    email: int = Form(...),
                    fullname: str = Form(...),
                    nationalId: str = Form(...),
                    taxnumber: str = Form(...),
                    phonenumber: str = Form(...),
                    address: str = Form(...),
                    bankcode: str = Form(...),
                    bankname: str = Form(...),
                    current_user:User = Depends(get_current_user_from_token)):
    
    conn = db.connection()
    cursor = conn.cursor()
    sql = "insert into profileuser(fullname,cccd,tax,phone,address,bankcode,bankname,idaccount) value (%s,%s,%s,%s,%s,%s,%s,%s)"
    value = (fullname,nationalId,taxnumber,phonenumber,address,bankcode,bankname,email,)
    cursor.execute(sql,value)
    conn.commit()
    conn.close()
    return RedirectResponse(url="/profile",status_code=status.HTTP_302_FOUND)

