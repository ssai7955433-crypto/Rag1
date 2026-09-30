import numpy as np

from core.retriever import top_k_retrieval


def test_cosine_ranks_relevant_chunk_and_applies_threshold():
    chunks = [
        {"chunk_id": "policy-1", "source": "policy.pdf", "page": 2, "text": "Paid leave is requested in the HR portal."},
        {"chunk_id": "it-1", "source": "it.docx", "page": None, "text": "Contact IT for a laptop issue."},
    ]
    vectors = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]

    results = top_k_retrieval(np.array([0.9, 0.1]), vectors, chunks, top_k=1, threshold=0.5)

    assert len(results) == 1
    assert results[0].chunk_id == "policy-1"
    assert results[0].score > 0.9
    assert results[0].page == 2


def test_zero_query_vector_returns_no_results():
    chunks = [{"chunk_id": "c1", "source": "handbook.pdf", "page": 1, "text": "Policy text"}]
    assert top_k_retrieval(np.zeros(2), [np.ones(2)], chunks) == []
