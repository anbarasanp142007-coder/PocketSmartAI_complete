from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .database import init_db
from .routers import auth,planners,history,pages
s=get_settings()
@asynccontextmanager
async def lifespan(app):
    init_db(); yield
app=FastAPI(title=s.app_name,version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=s.cors_origin_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
Path("app/static").mkdir(parents=True,exist_ok=True)
app.mount("/static",StaticFiles(directory="app/static"),name="static")
app.include_router(pages.router); app.include_router(auth.router); app.include_router(planners.router); app.include_router(history.router)
@app.get("/health")
def health(): return {"status":"ok","app":s.app_name,"gemini_enabled":bool(s.gemini_api_key and s.use_gemini)}
if __name__=="__main__":
    import uvicorn; uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)
