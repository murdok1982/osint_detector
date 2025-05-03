import requests

def analyze_with_gpt(text):
    payload = {"input": text}
    headers = {
        "Content-Type": "application/json"
    }
    # Usa tu método real de autenticación aquí si aplica
    response = requests.post("https://chat.openai.com/backend-api/gpts/g-chGmGnQUG-behavioral-pattern-detector", json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("analysis", "unknown")
    return "error"
