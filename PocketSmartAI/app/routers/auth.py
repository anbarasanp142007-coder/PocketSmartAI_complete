from fastapi import APIRouter,Depends,HTTPException,Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User,Recommendation
from ..schemas import *
from ..auth import *
router=APIRouter()
@router.post("/register",response_model=UserOut,status_code=201)
def register(p:UserCreate,db:Session=Depends(get_db)):
    if db.query(User).filter(User.email==p.email.lower()).first(): raise HTTPException(409,"Email is already registered")
    u=User(email=p.email.lower(),full_name=p.full_name.strip(),password_hash=hash_password(p.password)); db.add(u); db.commit(); db.refresh(u); return u
def auth(p,db):
    u=db.query(User).filter(User.email==p.email.lower()).first()
    if not u or not verify_password(p.password,u.password_hash): raise HTTPException(401,"Invalid email or password")
    return u
@router.post("/login",response_model=UserOut)
def login(p:UserLogin,response:Response,db:Session=Depends(get_db)):
    u=auth(p,db); response.set_cookie("access_token",create_access_token(u.id),httponly=True,samesite="lax",max_age=86400); return u
@router.post("/token",response_model=TokenResponse)
def token(p:UserLogin,db:Session=Depends(get_db)): return TokenResponse(access_token=create_access_token(auth(p,db).id))
@router.post("/logout")
def logout(response:Response): response.delete_cookie("access_token"); return {"message":"Logged out"}
@router.get("/session-info")
def session_info(u:User=Depends(get_current_user)): return {"authenticated":True,"user_id":u.id,"email":u.email,"full_name":u.full_name}
@router.get("/session-data")
def session_data(u:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return {"user":UserOut.model_validate(u).model_dump(),"recommendation_count":db.query(Recommendation).filter_by(user_id=u.id).count()}
