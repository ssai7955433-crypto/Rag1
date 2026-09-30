from core.chunker import chunk_text
from core.text_cleaner import clean_text


def test_chunk_text_preserves_source_page_and_respects_size():
    text = "First paragraph. " * 15 + "\n\n" + "Second paragraph. " * 15
    chunks = chunk_text(text, chunk_size=100, chunk_overlap=20, source_name="hr.pdf", page_number=3)

    assert len(chunks) > 1
    assert all(len(chunk.text) <= 100 for chunk in chunks)
    assert all(chunk.source == "hr.pdf" and chunk.page == 3 for chunk in chunks)
    assert chunks[0].chunk_id == "hr.pdf-chunk-1"


def test_clean_text_removes_control_chars_and_extra_whitespace():
    assert clean_text("  Paid\tleave\x00 is available.  ") == "Paid leave is available."
