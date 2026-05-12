import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_resume_content(prompt, model_name):

    payload = {
        "model": model_name,
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