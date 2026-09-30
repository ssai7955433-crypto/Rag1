from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass
class Chunk:
    chunk_id: str
    text: str
    source: str
    page: int | None


def chunk_text(
    text: str,
    chunk_size: int = 650,
    chunk_overlap: int = 100,
    source_name: str = "document",
    page_number: int | None = None,
) -> list[Chunk]:
    if not text or chunk_size <= 0:
        return []
    overlap = min(max(0, chunk_overlap), chunk_size - 1)
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    normalized = "\n\n".join(paragraphs)
    chunks: list[Chunk] = []
    start = 0

    while start < len(normalized):
        end = min(start + chunk_size, len(normalized))
        if end < len(normalized):
            boundary = normalized.rfind("\n\n", start, end)
            if boundary > start + chunk_size // 2:
                end = boundary
            else:
                boundary = normalized.rfind(" ", start, end)
                if boundary > start + chunk_size // 2:
                    end = boundary
        part = normalized[start:end].strip()
        if part:
            chunks.append(Chunk(f"{source_name}-chunk-{len(chunks) + 1}", part, source_name, page_number))
        if end >= len(normalized):
            break
        start = max(start + 1, end - overlap)

    return chunks
