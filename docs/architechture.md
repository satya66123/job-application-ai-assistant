# Job Application AI Assistant - Architecture Documentation

## System Overview

The Job Application AI Assistant follows a modular API-first architecture designed for maintainability, scalability, and local GenAI integration.

Primary objectives:

- modular design
- reusable services
- frontend/backend separation
- local LLM inference
- deployment readiness
- production-style structure

---

# High-Level Architecture

```text
+------------------------------------------------------+
|                  User / Browser                      |
+------------------------------------------------------+
                         |
                         v
+------------------------------------------------------+
|                 Streamlit Frontend UI                |
|------------------------------------------------------|
| - Resume Upload (PDF/DOCX/TXT)                       |
| - Resume Preview                                     |
| - Job Description Input                              |
| - Task Selector                                      |
| - Model Selector                                     |
| - ATS Dashboard                                      |
| - Career AI Chat                                     |
| - Download Outputs                                   |
| - Session Memory                                     |
+------------------------------------------------------+
                         |
                         v
+------------------------------------------------------+
|                 FastAPI Backend APIs                 |
|------------------------------------------------------|
| POST /generate-resume                                |
| POST /generate-cover-letter                          |
| POST /generate-interview-questions                   |
| POST /ats-score                                      |
| POST /chat-assistant                                 |
+------------------------------------------------------+
                         |
                         v
+------------------------------------------------------+
|                   Service Layer                      |
|------------------------------------------------------|
| openai_service.py                                    |
| file_parser.py                                       |
+------------------------------------------------------+
                         |
                         v
+------------------------------------------------------+
|                    Prompt Layer                      |
|------------------------------------------------------|
| prompts.py                                           |
| - Resume Prompt                                      |
| - Cover Letter Prompt                                |
| - Interview Prompt                                   |
| - ATS Prompt                                         |
| - Chat Prompt                                        |
+------------------------------------------------------+
                         |
                         v
+------------------------------------------------------+
|                Ollama Local LLM Layer                |
|------------------------------------------------------|
| llama3                                               |
| mistral                                              |
| phi3                                                 |
| deepseek-coder                                       |
| llama3:instruct                                      |
| llama3:8b                                            |
+------------------------------------------------------+
```

---

# Folder Architecture

```text
job-application-ai-assistant/
│
├── app/
│   │
│   ├── models/
│   │   └── request_models.py
│   │
│   ├── prompts/
│   │   └── prompts.py
│   │
│   ├── routes/
│   │   └── resume_routes.py
│   │
│   ├── services/
│   │   ├── openai_service.py
│   │   └── file_parser.py
│   │
│   ├── main.py
│   └── ui.py
│
├── docs/
│
├── k8s/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Component Responsibilities

## Frontend Layer

File:

```text
app/ui.py
```

Responsibilities:

- user interaction
- file uploads
- model selection
- task selection
- job description capture
- output rendering
- downloads
- session memory
- chat interface

Technology:

- Streamlit

---

## Backend API Layer

File:

```text
app/main.py
app/routes/resume_routes.py
```

Responsibilities:

- API routing
- request handling
- endpoint orchestration
- response formatting
- ATS parsing

Technology:

- FastAPI
- Uvicorn

---

## Validation Layer

File:

```text
app/models/request_models.py
```

Responsibilities:

- request schema validation
- input structure enforcement

Technology:

- Pydantic

---

## Prompt Layer

File:

```text
app/prompts/prompts.py
```

Responsibilities:

- centralized prompt engineering
- AI task separation
- reusable prompt templates

Prompts:

- resume prompt
- cover letter prompt
- interview prompt
- ATS prompt
- chat prompt

---

## Service Layer

Files:

```text
app/services/openai_service.py
app/services/file_parser.py
```

Responsibilities:

- Ollama communication
- model routing
- timeout handling
- connection handling
- PDF parsing
- DOCX parsing
- TXT parsing

---

## AI Inference Layer

Technology:

- Ollama

Supported models:

```text
llama3:latest
mistral:latest
phi3:latest
deepseek-coder:latest
llama3:instruct
llama3:8b
```

Responsibilities:

- local inference
- text generation
- task-specific reasoning

---

# API Architecture

## Endpoint Overview

### Resume API

```text
POST /generate-resume
```

Flow:

```text
UI → FastAPI → Prompt Layer → Ollama → Response Cleanup → UI
```

Output:

- ATS-friendly bullet points

---

### Cover Letter API

```text
POST /generate-cover-letter
```

Flow:

```text
UI → FastAPI → Prompt Layer → Ollama → UI
```

Output:

- professional cover letter

---

### Interview Questions API

```text
POST /generate-interview-questions
```

Flow:

```text
UI → FastAPI → Prompt Layer → Ollama → Output Cleanup → UI
```

Output:

- interview questions

---

### ATS API

```text
POST /ats-score
```

Flow:

```text
UI → FastAPI → Prompt Layer → Ollama → ATS Parser → Structured JSON → UI
```

Output:

- match %
- missing keywords
- suggestions

---

### Career Chat API

```text
POST /chat-assistant
```

Flow:

```text
UI → FastAPI → Chat Prompt → Ollama → AI Response → UI
```

Output:

- conversational AI response

---

# Request Lifecycle

## Resume Generation Example

Step 1:
User uploads resume

Step 2:
Resume text extracted

Step 3:
User enters job description

Step 4:
User selects model

Step 5:
UI sends JSON request

Example:

```json
{
  "resume": "...",
  "jobDescription": "...",
  "modelName": "llama3:latest"
}
```

Step 6:
FastAPI validates request

Step 7:
Prompt formatted

Step 8:
Ollama API invoked

Step 9:
LLM generates response

Step 10:
Backend cleans output

Step 11:
UI displays result

---

# Chat Flow

```text
User Message
    ↓
Resume Context
    ↓
Job Description Context
    ↓
Prompt Template
    ↓
Ollama Model
    ↓
AI Response
    ↓
Session Memory
    ↓
UI Rendering
```

---

# Session Memory Architecture

Using:

```python
st.session_state
```

Stores:

- chat history
- generated history

Purpose:

- preserve state
- avoid UI resets
- improve UX

---

# Error Handling Architecture

Handled scenarios:

## Ollama Down

Detection:

```python
ConnectionError
```

Response:

```text
Could not connect to Ollama
```

---

## Timeout

Detection:

```python
requests timeout
```

Response:

```text
Request timed out
```

---

## Empty File Extraction

Detection:

```python
not resume.strip()
```

Response:

```text
Could not extract resume text
```

---

## API Failure

Handled in frontend:

```python
st.error()
```

---

# Deployment Architecture

## Docker

Architecture:

```text
Docker Container
    ├── FastAPI
    └── Streamlit
```

Benefits:

- portability
- reproducibility
- local deployment

---

## Docker Compose

Purpose:

- one-command startup

Command:

```bash
docker-compose up --build
```

---

## Kubernetes

Resources:

- Namespace
- ConfigMap
- Deployment
- Service
- Ingress-ready

Architecture:

```text
User
 ↓
NodePort Service
 ↓
Deployment
 ↓
Pod
 ├── FastAPI
 └── Streamlit
```

---

# Scalability Considerations

Current MVP limitations:

- local model dependency
- single replica deployment
- in-memory session state
- no database persistence

Scalable future:

- Redis
- PostgreSQL
- Celery
- horizontal scaling
- load balancing
- cloud inference

---

# Security Considerations

Current:

- local deployment
- no authentication

Future:

- JWT auth
- API keys
- HTTPS
- RBAC
- secrets management

---

# Design Decisions

## Why API-first?

Benefits:

- frontend decoupling
- easier testing
- reusable APIs

---

## Why modular?

Benefits:

- maintainability
- separation of concerns
- easier enhancements

---

## Why local LLM?

Benefits:

- privacy
- zero API cost
- offline inference

---

# Architecture Status

Current architecture maturity:

MVP Complete

Deployment readiness:

- Local: Yes
- Docker: Yes
- Kubernetes: Yes

Portfolio readiness:

Yes