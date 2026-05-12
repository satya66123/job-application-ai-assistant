import streamlit as st
import requests

from services.file_parser import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt
)

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Job Application AI Assistant",
    layout="wide"
)

st.title("🚀 Job Application AI Assistant")
st.write("AI-powered career assistant using local Ollama models")

model_name = st.selectbox(
    "Choose AI Model",
    [
        "llama3:latest",
        "mistral:latest",
        "phi3:latest",
        "deepseek-coder:latest",
        "llama3:instruct",
        "llama3:8b"
    ]
)

uploaded_file = st.file_uploader(
    "Upload Resume (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"]
)

resume = ""

if uploaded_file:

    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension == "pdf":
        resume = extract_text_from_pdf(uploaded_file)

    elif file_extension == "docx":
        resume = extract_text_from_docx(uploaded_file)

    elif file_extension == "txt":
        resume = extract_text_from_txt(uploaded_file)

    st.success("Resume uploaded successfully")

else:
    resume = st.text_area(
        "Paste Resume",
        height=250,
        placeholder="Paste your resume content here..."
    )

job_description = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste job description here..."
)

task = st.selectbox(
    "Choose Action",
    [
        "Generate Resume Points",
        "Generate Cover Letter",
        "Generate Interview Questions",
        "ATS Score Checker"
    ]
)

if st.button("Generate"):

    if not resume:
        st.warning("Please upload or paste your resume")
        st.stop()

    if not job_description:
        st.warning("Please paste job description")
        st.stop()

    payload = {
        "resume": resume,
        "jobDescription": job_description,
        "modelName": model_name
    }

    endpoint_map = {
        "Generate Resume Points": "/generate-resume",
        "Generate Cover Letter": "/generate-cover-letter",
        "Generate Interview Questions": "/generate-interview-questions",
        "ATS Score Checker": "/ats-score"
    }

    endpoint = endpoint_map[task]

    with st.spinner("Generating response..."):

        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload
        )

    if response.status_code == 200:

        data = response.json()

        st.success("Generated successfully!")

        if task == "Generate Resume Points":

            st.subheader("Generated Resume Points")

            for point in data["generated_resume_points"]:
                st.write(f"• {point}")

        elif task == "Generate Cover Letter":

            st.subheader("Generated Cover Letter")
            st.write(data["cover_letter"])

        elif task == "Generate Interview Questions":

            st.subheader("Interview Questions")

            for question in data["interview_questions"]:
                st.write(f"• {question}")

        elif task == "ATS Score Checker":

            st.subheader("ATS Match Score")
            st.metric("Match Percentage", data["match_percentage"])

            st.subheader("Missing Keywords")

            if data["missing_keywords"]:
                for keyword in data["missing_keywords"]:
                    st.write(f"• {keyword}")
            else:
                st.success("No major missing keywords found")

            st.subheader("Improvement Suggestions")

            if data["improvement_suggestions"]:
                for suggestion in data["improvement_suggestions"]:
                    st.write(f"• {suggestion}")
            else:
                st.success("Resume looks strong")

    else:
        st.error("API request failed")