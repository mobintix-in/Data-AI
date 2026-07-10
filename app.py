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

# Include Routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
