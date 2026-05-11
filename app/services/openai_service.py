import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "llama3:latest"


def generate_resume_content(prompt):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "No response generated")

    except Exception as e:
        return f"Error generating response: {str(e)}"