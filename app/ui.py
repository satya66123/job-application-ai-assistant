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

# ---------------- SESSION STATE ----------------

DEFAULT_SESSION_VALUES = {
    "chat_history": [],
    "generated_history": [],
    "jwt_token": None,
    "current_user": None
}

for key, value in DEFAULT_SESSION_VALUES.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- API HELPERS ----------------

def get_auth_headers():
    return {
        "Authorization": f"Bearer {st.session_state.jwt_token}"
    }


def register_user(full_name, email, password):
    payload = {
        "full_name": full_name,
        "email": email,
        "password": password
    }

    return requests.post(
        f"{API_URL}/auth/register",
        json=payload,
        timeout=30
    )


def login_user(email, password):
    payload = {
        "email": email,
        "password": password
    }

    return requests.post(
        f"{API_URL}/auth/login",
        json=payload,
        timeout=30
    )

def delete_uploaded_document(document_id):
    return requests.delete(
        f"{API_URL}/rag/documents/{document_id}",
        headers=get_auth_headers(),
        timeout=30
    )

def fetch_current_user(token):
    return requests.get(
        f"{API_URL}/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=30
    )


def fetch_saved_outputs():
    return requests.get(
        f"{API_URL}/history/outputs",
        headers=get_auth_headers(),
        timeout=30
    )


def fetch_saved_chat():
    return requests.get(
        f"{API_URL}/history/chat",
        headers=get_auth_headers(),
        timeout=30
    )


def fetch_uploaded_documents():
    return requests.get(
        f"{API_URL}/rag/documents",
        headers=get_auth_headers(),
        timeout=30
    )


def fetch_saved_ats():
    return requests.get(
        f"{API_URL}/history/ats",
        headers=get_auth_headers(),
        timeout=30
    )


def upload_knowledge(
    filename,
    document_text,
    collection_name
):
    payload = {
        "filename": filename,
        "document_text": document_text,
        "collection_name": collection_name
    }

    return requests.post(
        f"{API_URL}/rag/upload-knowledge",
        json=payload,
        headers=get_auth_headers(),
        timeout=300
    )

def rag_chat(
    question,
    model_name,
    chat_history,
    collection_name
):

    payload = {
        "question": question,
        "modelName": model_name,
        "chat_history": chat_history,
        "collection_name": collection_name
    }

    return requests.post(
        f"{API_URL}/rag/chat",
        json=payload,
        headers=get_auth_headers(),
        timeout=300
    )


# ---------------- AUTH ----------------

st.sidebar.title("🔐 Authentication")

if st.session_state.jwt_token is None:

    auth_option = st.sidebar.radio(
        "Choose",
        ["Login", "Register"]
    )

    if auth_option == "Register":

        st.sidebar.subheader("Create Account")

        reg_name = st.sidebar.text_input("Full Name")
        reg_email = st.sidebar.text_input("Email")
        reg_password = st.sidebar.text_input(
            "Password",
            type="password"
        )

        if st.sidebar.button("Register"):

            if not reg_name or not reg_email or not reg_password:
                st.sidebar.warning("All fields are required")
                st.stop()

            try:
                response = register_user(
                    reg_name,
                    reg_email,
                    reg_password
                )

                if response.status_code == 200:
                    st.sidebar.success("Registration successful")
                else:
                    try:
                        st.sidebar.error(
                            response.json().get("detail", "Registration failed")
                        )
                    except:
                        st.sidebar.error("Registration failed")

            except requests.exceptions.RequestException as e:
                st.sidebar.error(str(e))

    else:

        st.sidebar.subheader("Login")

        login_email = st.sidebar.text_input("Login Email")
        login_password = st.sidebar.text_input(
            "Login Password",
            type="password"
        )

        if st.sidebar.button("Login"):

            if not login_email or not login_password:
                st.sidebar.warning("Email and password required")
                st.stop()

            try:
                response = login_user(
                    login_email,
                    login_password
                )

                if response.status_code == 200:

                    token_data = response.json()

                    st.session_state.jwt_token = token_data["access_token"]

                    me_response = fetch_current_user(
                        st.session_state.jwt_token
                    )

                    if me_response.status_code == 200:
                        st.session_state.current_user = me_response.json()

                    st.rerun()

                else:
                    st.sidebar.error("Invalid credentials")

            except requests.exceptions.RequestException as e:
                st.sidebar.error(str(e))

    st.stop()

# ---------------- LOGGED IN ----------------

st.sidebar.success(
    f"Logged in as {st.session_state.current_user['full_name']}"
)

if st.sidebar.button("Logout"):
    st.session_state.jwt_token = None
    st.session_state.current_user = None
    st.session_state.chat_history = []
    st.session_state.generated_history = []
    st.rerun()


# ---------------- MAIN UI ----------------

st.title("🚀 Job Application AI Assistant")
st.caption("AI-powered career assistant using Ollama + FastAPI + RAG")

st.sidebar.title("⚙ Settings")

model_name = st.sidebar.selectbox(
    "Choose AI Model",
    [
        "deepseek-coder:latest",
        "llama3:latest",
        "mistral:latest",
        "llama3:instruct",
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
        "Career AI Chat",
        "RAG Knowledge Upload",
        "RAG Chat"
    ]
)

st.sidebar.info("Supported resume uploads: PDF / DOCX / TXT")

if st.sidebar.button("🗑 Clear Session History"):
    st.session_state.chat_history = []
    st.session_state.generated_history = []
    st.rerun()


# ---------------- SAVED HISTORY ----------------

st.sidebar.subheader("📜 Saved History")

try:

    outputs_response = fetch_saved_outputs()

    if outputs_response.status_code == 200:
        outputs = outputs_response.json()

        for idx, item in enumerate(outputs[:10], 1):
            with st.sidebar.expander(
                f"{idx}. {item['output_type']}"
            ):
                st.write(item["content"][:1000])

    ats_response = fetch_saved_ats()

    if ats_response.status_code == 200:
        ats_reports = ats_response.json()

        for idx, report in enumerate(ats_reports[:5], 1):
            with st.sidebar.expander(
                f"ATS {idx} - {report['match_score']}"
            ):
                st.write(report["report"][:1000])

    chat_response = fetch_saved_chat()

    if chat_response.status_code == 200:
        chats = chat_response.json()

        for idx, chat in enumerate(chats[:5], 1):
            with st.sidebar.expander(f"Chat {idx}"):
                st.write("Q: " + chat["message"])
                st.write("A: " + chat["response"])

except requests.exceptions.RequestException:
    st.sidebar.info("No saved history yet")


st.sidebar.subheader("📂 Uploaded Knowledge Documents")

try:
    docs_response = fetch_uploaded_documents()

    if docs_response.status_code == 200:
        docs = docs_response.json()

        if docs:

            for doc in docs[:10]:

                col1, col2 = st.sidebar.columns([4, 1])

                with col1:
                    st.write(f"📄 {doc['filename']}")

                with col2:
                    if st.button(
                        "🗑",
                        key=f"delete_{doc['id']}"
                    ):
                        delete_response = delete_uploaded_document(
                            doc["id"]
                        )

                        if delete_response.status_code == 200:
                            st.rerun()

        else:
            st.sidebar.info("No uploaded documents")

except requests.exceptions.RequestException:
    st.sidebar.info("Documents unavailable")
# ---------------- RAG KNOWLEDGE UPLOAD ----------------

if task == "RAG Knowledge Upload":

    st.subheader("📚 Upload Knowledge Base")
    collection_name = st.selectbox(
        "Select Collection",
        [
            "General",
            "Java",
            "Cloud",
            "HR",
            "Resume",
            "Company Docs"
        ]
    )

    rag_uploaded_file = st.file_uploader(
        "Upload PDF / DOCX / TXT",
        type=["pdf", "docx", "txt"],
        key="rag_upload"
    )

    rag_text = ""

    filename = "manual_knowledge.txt"

    if rag_uploaded_file:

        filename = rag_uploaded_file.name
        ext = filename.split(".")[-1].lower()

        try:
            if ext == "pdf":
                rag_text = extract_text_from_pdf(rag_uploaded_file)

            elif ext == "docx":
                rag_text = extract_text_from_docx(rag_uploaded_file)

            elif ext == "txt":
                rag_text = extract_text_from_txt(rag_uploaded_file)

            if rag_text.strip():
                st.success(f"Extracted content from {filename}")

                with st.expander("Preview Extracted Knowledge"):
                    st.text(rag_text[:3000])

        except Exception as e:
            st.error(f"File parsing failed: {str(e)}")

    else:

        rag_text = st.text_area(
            "Or paste knowledge manually",
            height=300
        )

    if st.button("Upload Knowledge"):

        if not rag_text.strip():
            st.warning("Upload a file or paste knowledge first")
            st.stop()

        try:
            with st.spinner("Chunking + embedding + storing..."):

                response = upload_knowledge(
                    filename,
                    rag_text,
                    collection_name
                )

            data = response.json()


            if "error" in data:
                st.warning(data["error"])

            elif response.status_code == 200:
                st.success(
                    f"Knowledge uploaded successfully | Chunks: {data.get('chunks_created', 0)}"
                )

            else:
                st.error(response.text)

        except requests.exceptions.RequestException as e:
            st.error(str(e))

    st.stop()

# ---------------- RAG CHAT ----------------

if task == "RAG Chat":

    st.subheader("🧠 RAG Knowledge Chat")

    rag_question = st.text_input(
        "Ask a question from uploaded knowledge"
    )

    chat_collection = st.selectbox(
        "Search Collection",
        [
            "General",
            "Java",
            "Cloud",
            "HR",
            "Resume",
            "Company Docs"
        ]
    )

    if st.button("Ask RAG"):

        if not rag_question.strip():
            st.warning("Enter a question")
            st.stop()

        try:
            with st.spinner("Retrieving relevant knowledge..."):

                response = rag_chat(
                    rag_question,
                    model_name,
                    st.session_state.chat_history,
                    chat_collection
                )

            if response.status_code == 200:

                data = response.json()

                st.success("Answer generated")

                answer = data["answer"]
                sources1 = data.get("sources", [])

                st.session_state.chat_history.append({
                    "role": "user",
                    "content": rag_question
                })

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

                st.write(answer)

                if sources1:
                    st.markdown("### 📚 Sources")

                    for source in sources1:
                        st.write(f"📄 {source}")

            else:
                st.error(response.text)

        except requests.exceptions.RequestException as e:
            st.error(str(e))

    st.stop()


# ---------------- STANDARD TOOLS ----------------

STANDARD_TASKS = [
    "Generate Resume Points",
    "Generate Cover Letter",
    "Generate Interview Questions",
    "ATS Score Checker"
]

if task in STANDARD_TASKS:
    # ---------------- INPUTS ----------------

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

            ext = uploaded_file.name.split(".")[-1].lower()

            if ext == "pdf":
                resume = extract_text_from_pdf(uploaded_file)

            elif ext == "docx":
                resume = extract_text_from_docx(uploaded_file)

            elif ext == "txt":
                resume = extract_text_from_txt(uploaded_file)

            if not resume.strip():
                st.error("Could not extract resume text")
                st.stop()

            st.success("Resume uploaded successfully")

            with st.expander("Preview Resume"):
                st.text(resume[:3000])

        else:
            resume = st.text_area(
                "Paste Resume",
                height=400
            )

    with right_col:

        st.subheader("Job Description")

        job_description = st.text_area(
            "Paste Job Description",
            height=400
        )

    st.divider()

    if st.button("🚀 Generate", use_container_width=True):

        if not resume.strip():
            st.warning("Please provide resume")
            st.stop()

        if not job_description.strip():
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

        try:
            with st.spinner("Generating response..."):

                response = requests.post(
                    f"{API_URL}{endpoint}",
                    json=payload,
                    headers=get_auth_headers(),
                    timeout=300
                )

            if response.status_code != 200:
                st.error(response.text)
                st.stop()

            data = response.json()

            if "error" in data:
                st.error(data["error"])
                st.stop()

            if task == "Generate Resume Points":

                st.subheader("Generated Resume Points")

                output = ""

                for point in data["generated_resume_points"]:
                    st.write(f"• {point}")
                    output += f"• {point}\n"

                st.session_state.generated_history.append({
                    "type": "Resume Points",
                    "content": output
                })

                st.download_button(
                    "Download Resume Points",
                    output,
                    "resume_points.txt"
                )

            elif task == "Generate Cover Letter":

                cover_letter = data["cover_letter"]

                st.text_area(
                    "Generated Cover Letter",
                    cover_letter,
                    height=400
                )

                st.session_state.generated_history.append({
                    "type": "Cover Letter",
                    "content": cover_letter
                })

                st.download_button(
                    "Download Cover Letter",
                    cover_letter,
                    "cover_letter.txt"
                )

            elif task == "Generate Interview Questions":

                st.subheader("Interview Questions")

                output = ""

                for question in data["interview_questions"]:
                    st.write(f"• {question}")
                    output += f"• {question}\n"

                st.session_state.generated_history.append({
                    "type": "Interview Questions",
                    "content": output
                })

                st.download_button(
                    "Download Interview Questions",
                    output,
                    "interview_questions.txt"
                )

            elif task == "ATS Score Checker":

                st.subheader("ATS Analysis")

                st.metric(
                    "Match Percentage",
                    data["match_percentage"]
                )

                report = f"ATS Score: {data['match_percentage']}\n\n"

                st.subheader("Missing Keywords")

                if data["missing_keywords"]:
                    for keyword in data["missing_keywords"]:
                        st.write(f"• {keyword}")
                        report += f"Missing Keyword: {keyword}\n"
                else:
                    st.success("No missing keywords detected")

                st.subheader("Improvement Suggestions")

                if data["improvement_suggestions"]:
                    for suggestion in data["improvement_suggestions"]:
                        st.write(f"• {suggestion}")
                        report += f"Suggestion: {suggestion}\n"
                else:
                    st.success("No major suggestions")

                st.session_state.generated_history.append({
                    "type": "ATS Report",
                    "content": report
                })

                st.download_button(
                    "Download ATS Report",
                    report,
                    "ats_report.txt"
                )

        except requests.exceptions.RequestException as e:
            st.error(str(e))


# ---------------- CAREER AI CHAT ----------------

if task == "Career AI Chat":

    st.subheader("💬 Career AI Chat")

    if not resume.strip():
        st.warning("Please provide resume")
        st.stop()

    if not job_description.strip():
        st.warning("Please provide job description")
        st.stop()

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input(
        "Ask career-related questions..."
    )

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

        try:
            with st.spinner("Thinking..."):

                response = requests.post(
                    f"{API_URL}/chat-assistant",
                    json=payload,
                    headers=get_auth_headers(),
                    timeout=600
                )

            if response.status_code != 200:
                st.error(response.text)
                st.stop()

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

        except requests.exceptions.RequestException as e:
            st.error(str(e))