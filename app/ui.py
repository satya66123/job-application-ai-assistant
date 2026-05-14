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
    page_icon="🚀",
    layout="wide"
)

# Session state initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "generated_history" not in st.session_state:
    st.session_state.generated_history = []

st.title("🚀 Job Application AI Assistant")
st.caption("AI-powered career assistant using local Ollama models")

# Sidebar
st.sidebar.title("⚙ Settings")

model_name = st.sidebar.selectbox(
    "Choose AI Model",
    [

        # Coding
        "deepseek-coder:latest",

        # General purpose
        "llama3:latest",
        "mistral:latest",
        "llama3:instruct",

        # Fast
        "phi3:latest",
        "llama3:8b"
    ]
)

task = st.sidebar.selectbox(
    "Choose Action",
    [
        "Generate Resume Points",
        "Generate Cover Letter",
        "Generate Interview Questions",
        "ATS Score Checker",
        "Career AI Chat"
    ]
)

st.sidebar.info("Supported uploads: PDF / DOCX / TXT")

# Clear history
if st.sidebar.button("🗑 Clear Session History"):
    st.session_state.chat_history = []
    st.session_state.generated_history = []
    st.rerun()

# Generated history viewer
if st.session_state.generated_history:

    st.sidebar.subheader("📜 Generated History")

    for idx, item in enumerate(
        reversed(st.session_state.generated_history),
        1
    ):
        with st.sidebar.expander(f"{idx}. {item['type']}"):
            st.write(item["content"][:1000])

# Layout
left_col, right_col = st.columns(2)

resume = ""
job_description = ""

with left_col:

    st.subheader("Resume Input")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file:

        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension == "pdf":
            resume = extract_text_from_pdf(uploaded_file)

        elif file_extension == "docx":
            resume = extract_text_from_docx(uploaded_file)

        elif file_extension == "txt":
            resume = extract_text_from_txt(uploaded_file)

        if not resume.strip():
            st.error("Could not extract resume text")
            st.stop()

        st.success("Resume uploaded successfully")

        with st.expander("Preview Extracted Resume"):
            st.text(resume[:3000])

    else:
        resume = st.text_area(
            "Paste Resume",
            height=400,
            placeholder="Paste resume content here..."
        )

with right_col:

    st.subheader("Job Description")

    job_description = st.text_area(
        "Paste Job Description",
        height=400,
        placeholder="Paste job description here..."
    )

st.divider()

# Standard tools
if task != "Career AI Chat":

    if st.button("🚀 Generate", use_container_width=True):

        if not resume:
            st.warning("Please upload or paste your resume")
            st.stop()

        if not job_description:
            st.warning("Please provide job description")
            st.stop()

        payload = {
            "resume": resume,
            "jobDescription": job_description,
            "modelName": model_name,
            "userMessage": ""
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
                json=payload,
                timeout=200
            )

        if response.status_code == 200:

            data = response.json()

            if "error" in data:
                st.error(data["error"])
                st.stop()

            st.success("Generation completed")

            if task == "Generate Resume Points":

                st.subheader("Generated Resume Points")

                output_text = ""

                for point in data["generated_resume_points"]:
                    st.write(f"• {point}")
                    output_text += f"• {point}\n"

                st.session_state.generated_history.append({
                    "type": "Resume Points",
                    "content": output_text
                })

                st.download_button(
                    "Download Resume Points",
                    output_text,
                    "resume_points.txt",
                    "text/plain"
                )

            elif task == "Generate Cover Letter":

                st.subheader("Generated Cover Letter")

                st.text_area(
                    "Cover Letter",
                    data["cover_letter"],
                    height=400
                )

                st.session_state.generated_history.append({
                    "type": "Cover Letter",
                    "content": data["cover_letter"]
                })

                st.download_button(
                    "Download Cover Letter",
                    data["cover_letter"],
                    "cover_letter.txt",
                    "text/plain"
                )

            elif task == "Generate Interview Questions":

                st.subheader("Interview Questions")

                output_text = ""

                for question in data["interview_questions"]:
                    st.write(f"• {question}")
                    output_text += f"• {question}\n"

                st.session_state.generated_history.append({
                    "type": "Interview Questions",
                    "content": output_text
                })

                st.download_button(
                    "Download Interview Questions",
                    output_text,
                    "interview_questions.txt",
                    "text/plain"
                )

            elif task == "ATS Score Checker":

                st.subheader("ATS Analysis")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Match Percentage", data["match_percentage"])

                ats_output = f"ATS Match Percentage: {data['match_percentage']}\n\n"

                with col2:
                    st.success("Analysis Complete")

                tab1, tab2 = st.tabs(
                    ["Missing Keywords", "Improvement Suggestions"]
                )

                with tab1:

                    if data["missing_keywords"]:
                        for keyword in data["missing_keywords"]:
                            st.write(f"• {keyword}")
                            ats_output += f"Missing Keyword: {keyword}\n"
                    else:
                        st.success("No major missing keywords")

                with tab2:

                    if data["improvement_suggestions"]:
                        for suggestion in data["improvement_suggestions"]:
                            st.write(f"• {suggestion}")
                            ats_output += f"Suggestion: {suggestion}\n"
                    else:
                        st.success("Resume looks strong")

                st.session_state.generated_history.append({
                    "type": "ATS Report",
                    "content": ats_output
                })

                st.download_button(
                    "Download ATS Report",
                    ats_output,
                    "ats_report.txt",
                    "text/plain"
                )

        else:
            st.error(f"API request failed: {response.text}")

# Chat mode
else:

    st.subheader("💬 Career AI Chat")

    if not resume:
        st.warning("Please upload or paste your resume for chat context")
        st.stop()

    if not job_description:
        st.warning("Please provide job description for chat context")
        st.stop()

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Ask career-related questions...")

    if user_input:

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        payload = {
            "resume": resume,
            "jobDescription": job_description,
            "modelName": model_name,
            "userMessage": user_input
        }

        with st.spinner("Thinking..."):

            response = requests.post(
                f"{API_URL}/chat-assistant",
                json=payload,
                timeout=600
            )

        if response.status_code == 200:

            data = response.json()

            if "error" in data:
                st.error(data["error"])
                st.stop()

            assistant_reply = data["assistant_response"]

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": assistant_reply
            })

            st.session_state.generated_history.append({
                "type": "Career Chat",
                "content": assistant_reply
            })

            with st.chat_message("assistant"):
                st.write(assistant_reply)

        else:
            st.error(f"Chat API failed: {response.text}")