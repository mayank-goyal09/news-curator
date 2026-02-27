import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

def ollama_generate_json(prompt: str, schema: dict | None = None) -> dict:
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    payload["format"] = schema if schema is not None else "json"

    print("Ollama request: sending...")
    r = requests.post(OLLAMA_URL, json=payload, timeout=(10, 180))
    print(f"Ollama request: status={r.status_code}")

    r.raise_for_status()
    return r.json()
