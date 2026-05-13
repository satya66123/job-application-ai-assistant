from pydantic import BaseModel


class ResumeRequest(BaseModel):
    resume: str
    jobDescription: str
    modelName: str
    userMessage: str = ""