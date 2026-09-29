from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

def utcnow(): return datetime.now(timezone.utc)

class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    email: Mapped[str]=mapped_column(String(255),unique=True,index=True)
    full_name: Mapped[str]=mapped_column(String(120))
    password_hash: Mapped[str]=mapped_column(String(255))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow)
    recommendations: Mapped[list["Recommendation"]]=relationship(back_populates="user",cascade="all, delete-orphan")

class Recommendation(Base):
    __tablename__="recommendations"
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"),index=True)
    planner: Mapped[str]=mapped_column(String(30),index=True)
    title: Mapped[str]=mapped_column(String(255))
    budget: Mapped[int]=mapped_column(Integer)
    request_json: Mapped[dict]=mapped_column(JSON)
    response_json: Mapped[dict]=mapped_column(JSON)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow)
    user: Mapped[User]=relationship(back_populates="recommendations")
