from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class RetrievalResult:
    chunk_id: str
    score: float
    text: str
    source: str
    source_type: str | None
    page: int | None


def top_k_retrieval(
    query_vector: np.ndarray,
    chunk_vectors: list[np.ndarray],
    chunks: list[dict],
    top_k: int = 4,
    threshold: float = 0.25,
) -> list[RetrievalResult]:
    if not chunk_vectors or not chunks or top_k <= 0:
        return []

    query_norm = float(np.linalg.norm(query_vector))
    if query_norm == 0:
        return []

    ranked: list[tuple[int, float]] = []
    for index, vector in enumerate(chunk_vectors[: len(chunks)]):
        vector_norm = float(np.linalg.norm(vector))
        if vector_norm == 0:
            continue
        score = float(np.dot(query_vector, vector) / (query_norm * vector_norm))
        if np.isfinite(score):
            ranked.append((index, score))

    ranked.sort(key=lambda pair: pair[1], reverse=True)
    results: list[RetrievalResult] = []
    selected_texts: list[str] = []
    for index, score in ranked:
        if score < threshold:
            continue
        item = chunks[index]
        text = item["text"]
        if any(text in previous or previous in text for previous in selected_texts):
            continue
        results.append(
            RetrievalResult(
                chunk_id=item["chunk_id"],
                score=score,
                text=text,
                source=item["source"],
                source_type=item.get("source_type"),
                page=item.get("page"),
            )
        )
        selected_texts.append(text)
        if len(results) >= top_k:
            break
    return results
