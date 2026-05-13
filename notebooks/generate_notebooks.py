import os
import json

NOTEBOOK_DIR = "notebooks"

os.makedirs(NOTEBOOK_DIR, exist_ok=True)


def create_notebook(title, markdown_text, code_text, filename):
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [line + "\n" for line in markdown_text.split("\n")]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [line + "\n" for line in code_text.split("\n")]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.11"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    path = os.path.join(NOTEBOOK_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2)

    print(f"Created: {path}")


create_notebook(
    title="Ollama Model Testing",
    markdown_text="""
# Ollama Model Testing

Test local Ollama models.
""",
    code_text="""
import requests

models = [
    "llama3:latest",
    "mistral:latest",
    "phi3:latest",
    "deepseek-coder:latest"
]

for model in models:
    payload = {
        "model": model,
        "prompt": "Explain Python in one sentence",
        "stream": False
    }

    response = requests.post(
        "http://localhost:11434/api/generate",
        json=payload,
        timeout=120
    )

    print(model)
    print(response.json().get("response"))
    print("-" * 50)
""",
    filename="01_ollama_model_testing.ipynb"
)


create_notebook(
    title="Prompt Engineering Tests",
    markdown_text="""
# Prompt Engineering Tests

Experiment with prompts.
""",
    code_text="""
resume = "Python backend developer with FastAPI experience"
jd = "Need AI backend engineer with REST API skills"

prompt = f'''
Optimize this resume:

{resume}

for this job:

{jd}
'''

print(prompt)
""",
    filename="02_prompt_engineering_tests.ipynb"
)


create_notebook(
    title="Resume Generation Demo",
    markdown_text="""
# Resume Generation Demo
""",
    code_text="""
import requests

payload = {
    "resume": "Sample Python Developer Resume",
    "jobDescription": "Backend Python Developer with AI integration",
    "modelName": "llama3:latest",
    "userMessage": ""
}

response = requests.post(
    "http://localhost:8000/generate-resume",
    json=payload
)

print(response.json())
""",
    filename="03_resume_generation_demo.ipynb"
)


create_notebook(
    title="ATS Analysis Demo",
    markdown_text="""
# ATS Analysis Demo
""",
    code_text="""
import requests

payload = {
    "resume": "Sample resume",
    "jobDescription": "FastAPI Python backend developer",
    "modelName": "llama3:latest",
    "userMessage": ""
}

response = requests.post(
    "http://localhost:8000/ats-score",
    json=payload
)

print(response.json())
""",
    filename="04_ats_analysis_demo.ipynb"
)


create_notebook(
    title="Interview Questions Demo",
    markdown_text="""
# Interview Questions Demo
""",
    code_text="""
import requests

payload = {
    "resume": "Python backend engineer",
    "jobDescription": "AI backend engineer role",
    "modelName": "llama3:latest",
    "userMessage": ""
}

response = requests.post(
    "http://localhost:8000/generate-interview-questions",
    json=payload
)

print(response.json())
""",
    filename="05_interview_questions_demo.ipynb"
)


create_notebook(
    title="Career Chat Demo",
    markdown_text="""
# Career AI Chat Demo
""",
    code_text="""
import requests

payload = {
    "resume": "Python backend engineer",
    "jobDescription": "Backend AI engineer",
    "modelName": "llama3:latest",
    "userMessage": "How can I improve my resume?"
}

response = requests.post(
    "http://localhost:8000/chat-assistant",
    json=payload
)

print(response.json())
""",
    filename="06_chat_assistant_demo.ipynb"
)


create_notebook(
    title="File Parser Testing",
    markdown_text="""
# File Parser Testing
""",
    code_text="""
from app.services.file_parser import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt
)

print("Parser modules loaded successfully")
""",
    filename="07_file_parser_testing.ipynb"
)


create_notebook(
    title="FastAPI API Testing",
    markdown_text="""
# FastAPI API Testing
""",
    code_text="""
import requests

response = requests.get("http://localhost:8000/docs")

print(response.status_code)
""",
    filename="08_api_testing_fastapi.ipynb"
)


create_notebook(
    title="End to End Demo",
    markdown_text="""
# End to End Workflow Demo
""",
    code_text="""
steps = [
    "Upload resume",
    "Extract content",
    "Paste job description",
    "Generate ATS report",
    "Generate resume bullets",
    "Generate interview questions",
    "Use AI chat"
]

for step in steps:
    print(step)
""",
    filename="09_end_to_end_demo.ipynb"
)


create_notebook(
    title="Model Comparison",
    markdown_text="""
# Model Comparison
""",
    code_text="""
models = [
    "llama3:latest",
    "mistral:latest",
    "phi3:latest",
    "deepseek-coder:latest"
]

for model in models:
    print(f"Evaluate performance for: {model}")
""",
    filename="10_model_comparison.ipynb"
)


print("\\nAll notebooks generated successfully.")