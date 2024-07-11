from .forms import LoginForm
from .models import get_current_user_from_cookie
import db
from fastapi import APIRouter,Request,status,Response,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from .models import create_access_token,User
from typing import Dict
from ultils import settings
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import datetime
auth = APIRouter()
templates = Jinja2Templates(directory="templates")

@auth.get("/",tags=["authentication"], response_class=HTMLResponse)
def index():
    return RedirectResponse(url="/signin",status_code=status.HTTP_302_FOUND)

@auth.get("/signin",tags=["authentication"], response_class=HTMLResponse)
async def signin_get(request: Request):
    try:
        user = get_current_user_from_cookie(request)
    except:
        user = None
    form = LoginForm(request)
    context={
        "request":request,
        "form":form,
        "is_authenticated":0,
        "current_user":user
    }
    return templates.TemplateResponse("authentication/login.html",context)


@auth.post("resgisteraccersstoken",tags=["authentication"])
def resgister_for_access_token(response: Response, user: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    access_token = create_access_token(data={"id":user.id})
    response.set_cookie(
        key=settings.COOKIE_NAME, 
        value=f"Bearer {access_token}", 
        httponly=True
    )  
    return {settings.COOKIE_NAME: access_token, "token_type": "bearer"}



@auth.post("/signin",tags=["authentication"], response_class=HTMLResponse)
async def signin(request: Request):   
    try:
        current_user = get_current_user_from_cookie(request)
    except:
        current_user = None
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
      
        conn=db.connection()
        cursor=conn.cursor()
        cursor.execute("CALL login_user(%s, %s, @output)", (form.email, form.password))
        cursor.execute("SELECT @output;")
        id_user =cursor.fetchone()
        conn.commit()
        conn.close()
        if id_user[0]!=0:
    
            user=User(id=id_user[0])
            response= RedirectResponse(url=f"/authorizationUser",status_code=status.HTTP_302_FOUND)
            #response= RedirectResponse(url=VERIFY_2FA_URL)
            resgister_for_access_token(response=response, user=user)
        else:
            messages=[("danger","Invalid username and/or password.")]
            response= RedirectResponse(url="/signin",status_code=status.HTTP_302_FOUND)
    return response