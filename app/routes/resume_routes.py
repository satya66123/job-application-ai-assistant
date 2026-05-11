from fastapi import APIRouter
from app.models.request_models import ResumeRequest
from app.prompts.prompts import RESUME_PROMPT
from app.prompts.prompts import COVER_LETTER_PROMPT
from app.services.openai_service import generate_resume_content

router = APIRouter()


@router.post("/generate-resume")
def generate_resume(data: ResumeRequest):

    prompt = RESUME_PROMPT.format(
        resume=data.resume,
        job_description=data.jobDescription
    )

    result = generate_resume_content(prompt)

    formatted_points = result.split("\n")

    cleaned_points = []

    for point in formatted_points:

        point = point.strip()

        # Remove empty lines
        if not point:
            continue

        # Remove unwanted intro sentence
        if "here are" in point.lower():
            continue

        # Remove bullet symbols
        point = point.replace("•", "").strip()

        cleaned_points.append(point)

    return {
        "generated_resume_points": cleaned_points
    }

@router.post("/generate-cover-letter")
def generate_cover_letter(data: ResumeRequest):

    prompt = COVER_LETTER_PROMPT.format(
        resume=data.resume,
        job_description=data.jobDescription
    )

    result = generate_resume_content(prompt)

    return {
        "cover_letter": result.strip()
    }