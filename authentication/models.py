from datetime import datetime
import pyotp
from pydantic import BaseModel
import datetime as dt
from typing import Dict, List, Optional
from jose import JWTError, jwt
import db
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from ultils import settings,decode_id,encode_id

class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    This class is taken directly from FastAPI:
    https://github.com/tiangolo/fastapi/blob/26f725d259c5dbe3654f221e608b14412c6b40da/fastapi/security/oauth2.py#L140-L171
    
    The only change made is that authentication is taken from a cookie
    instead of from the header!
    """
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        # IMPORTANT: this is the line that differs from FastAPI. Here we use 
        # `request.cookies.get(settings.COOKIE_NAME)` instead of 
        # `request.headers.get("Authorization")`
        authorization: str = request.cookies.get(settings.COOKIE_NAME) 
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")

class User(BaseModel):
    id:int
    email:str=None
    password:str=None
    created_date:str=None
    rolename:str=None
    idprofile:int=None
    statuslogin:bool=False
    getdate:datetime=None

def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
    
def decode_token(token: str) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials."
    )
    token = token.removeprefix("Bearer").strip()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception
    
    user = get_user(id)
    return user

def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current user from the cookies in a request.

    Use this function when you want to lock down a route so that only 
    authenticated users can see access the route.
    """
    user = decode_token(token)
    return user


def get_current_user_from_cookie(request: Request) -> User:
    """
    Get the current user from the cookies in a request.
    
    Use this function from inside other routes to get the current user. Good
    for views that should work for both logged in, and not logged in users.
    """
    token = request.cookies.get(settings.COOKIE_NAME)
    user = decode_token(token)
    return user

def get_user(id:str) -> User:
    conn=db.connection()
    cursor=conn.cursor()
    sql="select a.*,p.id,r.rolename from account a join profileuser p on a.id=p.idaccount join roleuser r on r.id=a.role_id where a.id=%s"
    value=(id,)
    cursor.execute(sql,value)
    user_temp=cursor.fetchone()
    conn.commit()
    conn.close()
    
    if user_temp is not None:
        user=User(id=user_temp[0],email=user_temp[1],password=user_temp[2],created_date=user_temp[3].strftime('%Y-%m-%d %H:%M:%S'),idprofile=user_temp[5],rolename=user_temp[6],statuslogin=1,getdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        user = User(
            id=0,
            email="",
            password="",
            created_date="",
            idprofile=0,
            rolename="",
            statuslogin=0,
            getdate=""
        )
    
    return user
