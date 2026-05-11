from fastapi import FastAPI

app = FastAPI(
    title="Job Application AI Assistant",
    description="AI-powered resume tailoring assistant",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Job Application AI Assistant API Running"
    }