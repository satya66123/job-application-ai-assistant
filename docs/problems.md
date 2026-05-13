# Job Application AI Assistant - Problems & Challenges

## Project Challenges

This document captures real engineering challenges faced during development and how they were solved.

---

# Problem 1 — Local LLM Connectivity

## Issue

Backend needed to communicate with Ollama local models.

Initial challenge:

- API endpoint configuration
- connection failures
- inconsistent local availability

Symptoms:

- connection refused
- backend request failures

---

## Root Cause

Ollama service not running or incorrect API endpoint.

---

## Solution

Configured service layer:

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
```

Added:

- connection error handling
- timeout handling

---

# Problem 2 — Port Conflict

## Issue

Ollama failed to start.

Error:

```text
listen tcp 127.0.0.1:11434: bind:
Only one usage of each socket address is normally permitted.
```

---

## Root Cause

Existing Ollama instance already running.

---

## Solution

Reuse existing service instead of starting duplicate instance.

---

# Problem 3 — FastAPI Import Error

## Issue

Streamlit UI failed.

Error:

```text
ModuleNotFoundError: No module named 'app'
```

---

## Root Cause

Incorrect import path when launching Streamlit.

---

## Solution

Updated imports:

```python
from services.file_parser import ...
```

instead of package-relative import mismatch.

---

# Problem 4 — Swagger Method Error

## Issue

Browser request returned:

```json
{
  "detail": "Method Not Allowed"
}
```

---

## Root Cause

Using GET in browser for POST endpoint.

---

## Solution

Use Swagger UI POST requests.

---

# Problem 5 — Inconsistent LLM Output

## Issue

LLMs returned inconsistent formatting.

Examples:

- intro text
- markdown bullets
- numbered outputs
- noisy formatting

---

## Impact

Parsing failures.

Broken UI rendering.

---

## Solution

Added cleanup logic:

- strip bullets
- remove intro text
- normalize output

---

# Problem 6 — ATS Parsing Instability

## Issue

ATS response formatting varied by model.

Examples:

```text
Match Percentage:
```

vs

```text
Match Score:
```

---

## Impact

Parsing failures.

---

## Solution

Added fallback parser logic.

Supported multiple formats.

---

# Problem 7 — File Upload Parsing

## Issue

Need support for multiple resume formats.

Challenges:

- PDF parsing
- DOCX parsing
- TXT parsing

---

## Solution

Implemented:

PDF:

```python
PyPDF2
```

DOCX:

```python
python-docx
```

TXT:

UTF-8 parsing

---

# Problem 8 — Empty Resume Extraction

## Issue

Blank or unreadable files caused failures.

---

## Solution

Validation:

```python
if not resume.strip():
```

Display extraction error.

---

# Problem 9 — Streamlit Session Reset

## Issue

Streamlit reruns scripts on every interaction.

Lost:

- chat history
- generated outputs

---

## Solution

Implemented:

```python
st.session_state
```

Tracked:

- chat history
- generated history

---

# Problem 10 — Long Running Requests

## Issue

Heavy LLM requests caused hanging UI.

---

## Solution

Added request timeout:

```python
timeout=180
```

---

# Problem 11 — Docker + Ollama Networking

## Issue

Container could not reach host Ollama.

---

## Root Cause

Docker networking isolation.

---

## Solution

Configured:

```python
host.docker.internal
```

---

# Problem 12 — Kubernetes Deployment Planning

## Issue

Need orchestration-ready deployment.

---

## Solution

Created manifests:

- namespace
- configmap
- deployment
- service

---

# Problem 13 — Multi-Model Support

## Issue

Need dynamic model switching.

---

## Solution

Frontend model selector + backend model routing.

---

# Problem 14 — Chat Context Handling

## Issue

Career AI chat required contextual responses.

Needed:

- resume context
- JD context
- user prompt

---

## Solution

Chat prompt template with contextual injection.

---

# Problem 15 — Production-style Structure

## Issue

Need maintainable architecture.

---

## Solution

Modular separation:

- models
- prompts
- routes
- services
- frontend

---

# Lessons Learned

Key learnings:

- local LLM integration
- prompt engineering
- API design
- Streamlit state management
- Docker networking
- Kubernetes deployment basics
- modular architecture
- production-style project planning

---

# Final Outcome

All identified major issues resolved.

Project status:

Completed MVP