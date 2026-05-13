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

        return {
            "success": True,
            "response": data.get("response", "No response generated")
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out. Ollama model took too long."
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Could not connect to Ollama. Is Ollama running?"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }