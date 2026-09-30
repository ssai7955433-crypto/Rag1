from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingEngine:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, device="cpu")

    def encode_many(self, texts: list[str]) -> list[np.ndarray]:
        if not texts:
            return []
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return [np.asarray(vector, dtype=np.float32) for vector in vectors]

    def encode(self, text: str) -> np.ndarray:
        return self.encode_many([text])[0]
