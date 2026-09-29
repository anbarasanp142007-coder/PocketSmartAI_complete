from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field
Planner=Literal["home","party","jewelry"]

class UserCreate(BaseModel):
    email: EmailStr
    password: str=Field(min_length=8,max_length=128)
    full_name: str=Field(min_length=2,max_length=120)
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class TokenResponse(BaseModel):
    access_token: str
    token_type: str="bearer"
class UserOut(BaseModel):
    id:int; email:str; full_name:str
    model_config=ConfigDict(from_attributes=True)

class RoomSpec(BaseModel):
    room_type:str=Field(min_length=2,max_length=80)
    quantity:int=Field(default=1,ge=1,le=20)
    items:list[str]=Field(default_factory=list,max_length=30)
class HomeRequest(BaseModel):
    budget:int=Field(gt=0,le=10_000_000)
    currency:str=Field(default="INR",min_length=3,max_length=3)
    style:str=Field(default="modern",min_length=2,max_length=80)
    rooms:list[RoomSpec]=Field(min_length=1,max_length=20)
    location:str|None=Field(default=None,max_length=120)
    priorities:list[str]=Field(default_factory=list,max_length=10)
class PartyRequest(BaseModel):
    budget:int=Field(gt=0,le=10_000_000)
    currency:str=Field(default="INR",min_length=3,max_length=3)
    guest_count:int=Field(gt=0,le=10_000)
    event_type:str=Field(min_length=2,max_length=80)
    venue:str|None=Field(default=None,max_length=120)
    city:str|None=Field(default=None,max_length=120)
    preferences:list[str]=Field(default_factory=list,max_length=15)
class JewelryRequest(BaseModel):
    budget:int=Field(gt=0,le=10_000_000)
    currency:str=Field(default="INR",min_length=3,max_length=3)
    occasion:str=Field(min_length=2,max_length=80)
    style:str=Field(default="elegant",min_length=2,max_length=80)
    outfit_description:str|None=Field(default=None,max_length=1000)
    color_preferences:list[str]=Field(default_factory=list,max_length=10)

class CatalogItem(BaseModel):
    id:str; name:str; platform:str; category:str; price:int; currency:str="INR"; description:str; url:str
class Recommendation(BaseModel):
    item:CatalogItem
    reason:str
    estimated_total:int=Field(ge=0)
class RecommendationResponse(BaseModel):
    planner:Planner
    title:str
    budget:int
    currency:str
    budget_allocation:dict[str,int]
    recommendations:list[Recommendation]
    tips:list[str]
    disclaimer:str
