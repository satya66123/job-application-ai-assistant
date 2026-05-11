from fastapi import FastAPI
from app.routes.resume_routes import router as resume_router

app = FastAPI(
    title="Job Application AI Assistant",
    description="AI-powered resume tailoring assistant",
    version="1.0.0"
)

app.include_router(resume_router)


@app.get("/")
def home():
    return {
        "message": "Job Application AI Assistant API Running"
    }