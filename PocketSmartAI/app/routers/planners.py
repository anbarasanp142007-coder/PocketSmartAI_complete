from fastapi import APIRouter,Depends,File,Form,HTTPException,UploadFile
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..database import get_db
from ..models import User,Recommendation as RecommendationModel
from ..schemas import *
from ..services.recommendation_service import RecommendationService
from ..config import get_settings
router=APIRouter(); service=RecommendationService()
def save(db,u,planner,budget,payload,result):
    row=RecommendationModel(user_id=u.id,planner=planner,title=result.title,budget=budget,request_json=payload,response_json=result.model_dump()); db.add(row); db.commit()
@router.post("/generate-home",response_model=RecommendationResponse)
def home(p:HomeRequest,u:User=Depends(get_current_user),db:Session=Depends(get_db)):
    r=service.generate_home(p); save(db,u,"home",p.budget,p.model_dump(),r); return r
@router.post("/generate-party",response_model=RecommendationResponse)
def party(p:PartyRequest,u:User=Depends(get_current_user),db:Session=Depends(get_db)):
    r=service.generate_party(p); save(db,u,"party",p.budget,p.model_dump(),r); return r
@router.post("/generate-jewelry",response_model=RecommendationResponse)
async def jewelry(budget:int=Form(...),currency:str=Form("INR"),occasion:str=Form(...),style:str=Form("elegant"),outfit_description:str|None=Form(None),color_preferences:str=Form(""),outfit_image:UploadFile|None=File(None),u:User=Depends(get_current_user),db:Session=Depends(get_db)):
    s=get_settings(); data=None; mime=None
    if outfit_image:
        if not outfit_image.content_type or not outfit_image.content_type.startswith("image/"): raise HTTPException(400,"Outfit upload must be an image")
        data=await outfit_image.read()
        if len(data)>s.max_upload_mb*1024*1024: raise HTTPException(413,f"Image must be <= {s.max_upload_mb} MB")
        mime=outfit_image.content_type
    p=JewelryRequest(budget=budget,currency=currency,occasion=occasion,style=style,outfit_description=outfit_description,color_preferences=[x.strip() for x in color_preferences.split(",") if x.strip()])
    r=service.generate_jewelry(p,data,mime); save(db,u,"jewelry",budget,p.model_dump(),r); return r
