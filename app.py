from dotenv import load_dotenv
load_dotenv()

import urllib3
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from routes.main import router as main_router
from routes.auth import router as auth_router
from database.session import Base, engine

# Initialize SQLAlchemy database (using alembic for actual table creation, but this is a fallback)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lead Generation SaaS API")

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

from routes.dashboard import router as dashboard_router
from routes.leads import router as leads_router
from routes.search_history import router as search_history_router
from routes.saved_searches import router as saved_searches_router
from routes.exports import router as export_router
from routes.ai import router as ai_router
from routes.heatmap import router as heatmap_router

# Include Routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(leads_router, prefix="/api/leads", tags=["leads"])
app.include_router(search_history_router, prefix="/api/search-history", tags=["search-history"])
app.include_router(saved_searches_router, prefix="/api/saved-searches", tags=["saved-searches"])
app.include_router(export_router, prefix="/api/exports", tags=["exports"])
app.include_router(ai_router, prefix="/api/ai", tags=["ai"])
app.include_router(heatmap_router, prefix="/api/heatmap", tags=["heatmap"])
app.include_router(main_router, prefix="/api", tags=["main"])

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
