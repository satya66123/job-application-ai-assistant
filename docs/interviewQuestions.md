# Job Application AI Assistant - Interview Questions

## Project Overview Questions

### 1. What is this project about?

Answer:

This project is a local GenAI-powered Job Application AI Assistant built using Python, FastAPI, Streamlit, Ollama, Docker, and Kubernetes.

It helps users with:

- ATS-friendly resume optimization
- cover letter generation
- interview question generation
- ATS score analysis
- AI-powered career chat assistance

It uses local LLMs via Ollama, avoiding dependency on paid cloud APIs.

---

### 2. Why did you build this project?

Answer:

I wanted to build a practical end-to-end GenAI application that solves real job application problems.

The goal was to combine:

- backend API engineering
- frontend UI development
- local LLM integration
- prompt engineering
- containerization
- deployment readiness

This project demonstrates both software engineering and applied GenAI skills.

---

### 3. What problem does this solve?

Answer:

Job seekers often struggle with:

- tailoring resumes for job descriptions
- generating cover letters
- preparing interviews
- understanding ATS compatibility
- improving application quality

This project automates those workflows using AI.

---

# Architecture Questions

### 4. Explain your architecture.

Answer:

Architecture follows a modular layered design:

Frontend:
- Streamlit UI

Backend:
- FastAPI REST APIs

Service Layer:
- Ollama integration
- file parsing

Prompt Layer:
- prompt templates

AI Layer:
- local LLM inference

Deployment:
- Docker + Kubernetes

This separation improves maintainability and scalability.

---

### 5. Why FastAPI?

Answer:

FastAPI was chosen because:

- high performance
- async-friendly
- automatic Swagger documentation
- clean API development
- strong Python ecosystem support
- ideal for REST AI services

---

### 6. Why Streamlit?

Answer:

Streamlit enables rapid frontend development for AI applications.

Benefits:

- quick UI creation
- native Python
- interactive widgets
- file upload support
- chat components
- minimal frontend overhead

---

### 7. Why Ollama?

Answer:

Ollama enables local LLM execution.

Benefits:

- no API cost
- offline capability
- privacy
- multi-model support
- simple REST API interface

This aligns with local-first GenAI architecture.

---

# AI / GenAI Questions

### 8. Which models are supported?

Answer:

Supported local models:

- llama3:latest
- mistral:latest
- phi3:latest
- deepseek-coder:latest
- llama3:instruct
- llama3:8b

---

### 9. Why multiple models?

Answer:

Different models serve different purposes:

Llama:
strong general reasoning and writing

Mistral:
balanced performance and speed

Phi:
lightweight and fast

DeepSeek:
technical/code-focused reasoning

This gives flexibility based on task requirements.

---

### 10. How does prompt engineering work here?

Answer:

Prompt templates are centralized in:

```text
app/prompts/prompts.py
```

Separate prompts exist for:

- resume generation
- cover letters
- interview questions
- ATS analysis
- career chat

This improves modularity and maintainability.

---

### 11. What is local GenAI?

Answer:

Local GenAI means inference happens on the developer's machine instead of cloud APIs.

Benefits:

- privacy
- no token cost
- offline usage
- control over models

This project uses Ollama for local inference.

---

# Backend Questions

### 12. Explain your API endpoints.

Answer:

Endpoints:

```text
POST /generate-resume
POST /generate-cover-letter
POST /generate-interview-questions
POST /ats-score
POST /chat-assistant
```

Each endpoint handles a specific AI workflow.

---

### 13. How is request validation handled?

Answer:

Pydantic models validate API payloads.

File:

```text
app/models/request_models.py
```

Validation includes:

- resume text
- job description
- model selection
- user chat message

---

### 14. How is error handling implemented?

Answer:

Handled scenarios:

- Ollama unavailable
- timeout
- API failures
- empty file extraction
- invalid outputs

Graceful error responses improve stability.

---

### 15. How is ATS parsing handled?

Answer:

ATS responses are parsed into structured output:

- match percentage
- missing keywords
- suggestions

Fallback logic handles inconsistent LLM formatting.

---

# Frontend Questions

### 16. What frontend features exist?

Answer:

Frontend includes:

- model selector
- task selector
- resume upload
- resume preview
- job description input
- chat interface
- ATS metrics
- tabs
- downloads
- session history

---

### 17. Why use session state?

Answer:

Streamlit reruns scripts on interaction.

Session state preserves:

- chat history
- generated outputs

Without it, context would reset.

---

### 18. How are downloads implemented?

Answer:

Using:

```python
st.download_button()
```

Supports exporting:

- resume bullets
- cover letters
- interview questions
- ATS reports

---

# File Processing Questions

### 19. How is PDF parsing handled?

Answer:

Using:

```python
PyPDF2
```

Pages are read and extracted into text.

---

### 20. DOCX parsing?

Answer:

Using:

```python
python-docx
```

Paragraph text is extracted.

---

### 21. TXT parsing?

Answer:

Plain UTF-8 decoding.

---

# DevOps Questions

### 22. Why Docker?

Answer:

Docker provides reproducible environments.

Benefits:

- portability
- dependency consistency
- deployment readiness

---

### 23. Why Docker Compose?

Answer:

Simplifies multi-service startup.

Single command:

```bash
docker-compose up --build
```

---

### 24. Why Kubernetes?

Answer:

Kubernetes provides orchestration:

- scaling
- config management
- deployment abstraction
- service discovery

Portfolio-wise, it demonstrates production awareness.

---

### 25. Kubernetes resources used?

Answer:

Created:

- namespace
- configmap
- deployment
- service
- ingress-ready setup

---

# Design Questions

### 26. Why modular architecture?

Answer:

Separation of concerns:

models:
validation

prompts:
prompt engineering

routes:
API endpoints

services:
business logic

ui:
frontend

Improves maintainability.

---

### 27. Why API-first architecture?

Answer:

Benefits:

- frontend/backend separation
- easier scaling
- reusable APIs
- testing via Swagger

---

# Performance Questions

### 28. What performance concerns exist?

Answer:

Potential issues:

- local model inference latency
- heavy prompt sizes
- PDF parsing overhead
- concurrent requests

Mitigations:

- timeout handling
- lightweight models
- modular service design

---

# Improvement Questions

### 29. Future enhancements?

Answer:

Planned:

- RAG
- vector DB
- authentication
- user accounts
- saved history
- cloud deployment
- CI/CD
- recruiter dashboard
- batch processing

---

### 30. Biggest challenge?

Answer:

Main challenges:

- local LLM integration
- ATS output normalization
- Streamlit session state handling
- multi-model routing
- Docker + Kubernetes compatibility

---

# HR Questions

### 31. What did you learn?

Answer:

Learned:

- practical GenAI integration
- prompt engineering
- API design
- Streamlit frontend
- Docker
- Kubernetes
- deployment architecture

---

### 32. Why is this portfolio-worthy?

Answer:

Because it combines:

- backend engineering
- frontend engineering
- AI integration
- deployment
- real-world use case

This is more than a demo—it is a deployable MVP.