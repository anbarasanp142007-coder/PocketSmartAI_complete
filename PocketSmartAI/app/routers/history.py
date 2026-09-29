from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..database import get_db
from ..models import User,Recommendation
router=APIRouter()
@router.get("/history")
def history(u:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return [{"id":x.id,"planner":x.planner,"title":x.title,"budget":x.budget,"created_at":x.created_at.isoformat()} for x in db.query(Recommendation).filter_by(user_id=u.id).order_by(Recommendation.created_at.desc()).all()]
@router.get("/recommendations-details/{rid}")
def detail(rid:int,u:User=Depends(get_current_user),db:Session=Depends(get_db)):
    x=db.query(Recommendation).filter(Recommendation.id==rid,Recommendation.user_id==u.id).first()
    if not x: raise HTTPException(404,"Recommendation not found")
    return {"id":x.id,"planner":x.planner,"title":x.title,"budget":x.budget,"request":x.request_json,"result":x.response_json,"created_at":x.created_at.isoformat()}
