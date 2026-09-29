from datetime import datetime,timedelta,timezone
import jwt
from fastapi import Depends,HTTPException,Request,status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from .config import get_settings
from .database import get_db
from .models import User

ph=PasswordHash.recommended()
oauth2=OAuth2PasswordBearer(tokenUrl="/token",auto_error=False)
def hash_password(x): return ph.hash(x)
def verify_password(x,y): return ph.verify(x,y)
def create_access_token(uid):
    s=get_settings()
    return jwt.encode({"sub":str(uid),"exp":datetime.now(timezone.utc)+timedelta(minutes=s.access_token_expire_minutes)},s.secret_key,algorithm="HS256")
def get_current_user(request:Request,token:str|None=Depends(oauth2),db:Session=Depends(get_db)):
    token=token or request.cookies.get("access_token")
    if not token: raise HTTPException(401,"Authentication required")
    try: uid=int(jwt.decode(token,get_settings().secret_key,algorithms=["HS256"])["sub"])
    except Exception as e: raise HTTPException(401,"Invalid or expired authentication token") from e
    user=db.get(User,uid)
    if not user: raise HTTPException(401,"User not found")
    return user
