from __future__ import annotations

import requests


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.base_url = base_url.rstrip("/")

    def generate(self, model: str, system: str, prompt: str, temperature: float = 0.2) -> str:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                "options": {"temperature": temperature},
            },
            timeout=180,
        )
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "")
