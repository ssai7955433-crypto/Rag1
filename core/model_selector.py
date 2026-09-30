from __future__ import annotations

import requests

OLLAMA_URL = "http://localhost:11434"


def detect_ollama_models() -> tuple[bool, list[str]]:
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        response.raise_for_status()
        payload = response.json()
        return True, [item["name"] for item in payload.get("models", []) if item.get("name")]
    except (requests.RequestException, ValueError):
        return False, []


def choose_model(models: list[str]) -> tuple[str | None, str | None]:
    qwen = [name for name in models if "qwen" in name.lower()]
    if qwen:
        return qwen[0], "Qwen"
    llama = [name for name in models if "llama" in name.lower()]
    if llama:
        return llama[0], "Llama"
    return None, None


def get_model_recommendation() -> tuple[str, str]:
    connected, models = detect_ollama_models()
    if not connected:
        return "Ollama unavailable", "Not connected"
    model_name, family = choose_model(models)
    if model_name:
        return model_name, family or "Unknown"
    return "No Qwen/Llama model installed", "No supported model"
