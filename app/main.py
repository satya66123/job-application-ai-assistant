from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.init_db import init_database
from app.routes.auth_routes import router as auth_router

# existing imports
from app.routes.resume_routes import router as resume_router
from app.routes.history_routes import router as history_router
from app.routes.rag_routes import router as rag_router

app = FastAPI(
    title="Job Application AI Assistant API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_database()

app.include_router(auth_router)
app.include_router(history_router)
app.include_router(resume_router)
app.include_router(rag_router)


@app.get("/")
def home():
    return {
        "message": "Job Application AI Assistant API running"
    }