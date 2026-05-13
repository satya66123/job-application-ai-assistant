from fastapi import APIRouter
from app.models.request_models import ResumeRequest
from app.prompts.prompts import (
    RESUME_PROMPT,
    COVER_LETTER_PROMPT,
    INTERVIEW_QUESTIONS_PROMPT,
    ATS_PROMPT,
    CHAT_PROMPT
)
from app.services.openai_service import generate_resume_content

router = APIRouter()


@router.post("/generate-resume")
def generate_resume(data: ResumeRequest):

    prompt = RESUME_PROMPT.format(
        resume=data.resume,
        job_description=data.jobDescription
    )

    result = generate_resume_content(prompt, data.modelName)

    if not result["success"]:
        return {"error": result["error"]}

    formatted_points = result["response"].split("\n")

    cleaned_points = []

    for point in formatted_points:

        point = point.strip()

        if not point:
            continue

        if "here are" in point.lower():
            continue

        point = point.replace("•", "").replace("-", "").strip()

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

    result = generate_resume_content(prompt, data.modelName)

    if not result["success"]:
        return {"error": result["error"]}

    return {
        "cover_letter": result["response"].strip()
    }


@router.post("/generate-interview-questions")
def generate_interview_questions(data: ResumeRequest):

    prompt = INTERVIEW_QUESTIONS_PROMPT.format(
        resume=data.resume,
        job_description=data.jobDescription
    )

    result = generate_resume_content(prompt, data.modelName)

    if not result["success"]:
        return {"error": result["error"]}

    formatted_questions = result["response"].split("\n")

    cleaned_questions = []

    for question in formatted_questions:

        question = question.strip()

        if not question:
            continue

        if "here are" in question.lower():
            continue

        question = question.replace("•", "").replace("-", "").strip()

        cleaned_questions.append(question)

    return {
        "interview_questions": cleaned_questions
    }


@router.post("/ats-score")
def ats_score(data: ResumeRequest):

    prompt = ATS_PROMPT.format(
        resume=data.resume,
        job_description=data.jobDescription
    )

    result = generate_resume_content(prompt, data.modelName)

    if not result["success"]:
        return {"error": result["error"]}

    lines = result["response"].split("\n")

    match_percentage = "Not detected"
    missing_keywords = []
    improvement_suggestions = []

    current_section = None

    for line in lines:

        line = line.strip()

        if not line:
            continue

        clean_line = line.replace("*", "").replace("#", "").strip()
        lower_line = clean_line.lower()

        if "match percentage" in lower_line or "match score" in lower_line:
            match_percentage = clean_line.split(":")[-1].strip()

        elif "missing keywords" in lower_line:
            current_section = "missing"

        elif "improvement suggestions" in lower_line:
            current_section = "suggestions"

        elif current_section == "missing":
            keyword = clean_line.replace("-", "").replace("•", "").strip()

            if keyword:
                missing_keywords.append(keyword)

        elif current_section == "suggestions":
            suggestion = clean_line.replace("-", "").replace("•", "").strip()

            if suggestion:
                if "." in suggestion[:3]:
                    suggestion = suggestion.split(".", 1)[1].strip()

                improvement_suggestions.append(suggestion)

    return {
        "match_percentage": match_percentage,
        "missing_keywords": missing_keywords,
        "improvement_suggestions": improvement_suggestions
    }


@router.post("/chat-assistant")
def chat_assistant(data: ResumeRequest):

    prompt = CHAT_PROMPT.format(
        resume=data.resume,
        job_description=data.jobDescription,
        user_message=data.userMessage
    )

    result = generate_resume_content(prompt, data.modelName)

    if not result["success"]:
        return {"error": result["error"]}

    return {
        "assistant_response": result["response"]
    }