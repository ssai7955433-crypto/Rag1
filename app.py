from __future__ import annotations

from pathlib import Path

import streamlit as st

from core.embeddings import EmbeddingEngine
from core.model_selector import get_model_recommendation
from core.rag_pipeline import RAGPipeline
from ui.styles import apply_theme

st.set_page_config(page_title="Sai Stores Product Advisor", page_icon="🛍️", layout="wide")


@st.cache_resource(show_spinner="Loading the local embedding model...")
def get_embedding_engine() -> EmbeddingEngine:
    return EmbeddingEngine()


def get_pipeline() -> RAGPipeline:
    if "knowledge_pipeline" not in st.session_state:
        st.session_state.knowledge_pipeline = RAGPipeline(get_embedding_engine())
    return st.session_state.knowledge_pipeline


def render_sources(sources: list[dict]) -> None:
    if not sources:
        return
    with st.expander(f"Catalog evidence · {len(sources)} matches"):
        for source in sources:
            page = source.get("page")
            if source.get("source_type") in {"csv_catalog", "json_catalog"}:
                location = f"Product row {page}" if page is not None else "Product record"
            else:
                location = f"Page {page}" if page is not None else "Catalog document"
            st.markdown(f"**{source['source']}** · {location} · similarity `{source['score']:.3f}`")
            st.caption(f"{source['chunk_id']} · {source['score']:.1%} catalog match")
            st.write(source["text"])


def main() -> None:
    apply_theme()
    if st.session_state.get("assistant_mode") != "sai-stores-product-advisor-v1":
        st.session_state.pop("knowledge_pipeline", None)
        st.session_state.pop("messages", None)
        st.session_state["uploader_generation"] = st.session_state.get("uploader_generation", 0) + 1
        st.session_state["assistant_mode"] = "sai-stores-product-advisor-v1"

    model_name, model_family = get_model_recommendation()
    model_ready = model_family in {"Qwen", "Llama"}

    st.markdown(
        f"""
        <header class="app-header">
          <div>
            <div class="eyebrow">SAI STORES · SHOPPING ASSISTANT</div>
            <h1>Sai Stores</h1>
            <p>Find the right product using catalog details and customer reviews.</p>
          </div>
          <div class="runtime-status">
            <span class="status-dot {'online' if model_ready else 'offline'}"></span>
            <div><strong>Ollama {'ready' if model_ready else 'needs setup'}</strong>
            <small>{model_name} · {model_family}</small></div>
          </div>
        </header>
        """,
        unsafe_allow_html=True,
    )

    pipeline = get_pipeline()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "uploader_generation" not in st.session_state:
        st.session_state.uploader_generation = 0

    with st.sidebar:
        st.markdown("### Product catalog")
        uploads = st.file_uploader(
            "Add catalog or review files",
            type=["csv", "json", "pdf", "docx"],
            accept_multiple_files=True,
            key=f"product_catalog_{st.session_state.uploader_generation}",
            help="Import a CSV/JSON product feed or upload a PDF/DOCX catalog or review summary.",
        )
        if uploads:
            for upload in uploads:
                try:
                    result = pipeline.process_uploaded_file(upload)
                    if result["status"] == "ok":
                        if result.get("items") and upload.name.lower().endswith((".csv", ".json")):
                            st.success(f"Loaded {result['items']} product records from {upload.name}")
                        else:
                            st.success(f"Indexed {upload.name} · {result['chunks']} passages")
                    elif result["status"] == "error":
                        st.warning(f"{upload.name}: {result['message']}")
                except Exception:
                    st.error(f"Could not process {upload.name}. Check that the catalog file is valid and contains product data.")

        st.markdown("---")
        st.markdown("### Your preferences")
        shopping_for = st.text_input("Shopping for", placeholder="e.g. college, commuting, home office")
        budget = st.text_input("Budget", placeholder="e.g. $100 or 5000 INR")
        priorities = st.text_input("What matters most?", placeholder="e.g. lightweight, battery life, comfort")
        st.markdown("---")
        st.markdown("### Recommendation settings")
        pipeline.config.top_k = st.slider("Passages to retrieve", 1, 10, 4)
        pipeline.config.threshold = st.slider("Minimum relevance", 0.0, 1.0, 0.25, step=0.01)
        pipeline.config.temperature = st.slider("Answer creativity", 0.0, 1.0, 0.2, step=0.05)
        st.caption("Only matching catalog products are used to form recommendations.")

        st.markdown("---")
        product_count = sum(document.get("item_count", 0) for document in pipeline.index.documents)
        st.markdown("### Loaded sources")
        st.markdown(f"**{product_count}** product rows · **{len(pipeline.index.chunks)}** searchable passages")
        for document in pipeline.index.documents:
            st.caption(f"{document['filename']} · {document['char_count']:,} characters")
        if pipeline.index.documents and st.button("Clear catalog and chat", use_container_width=True):
            st.session_state.knowledge_pipeline = RAGPipeline(get_embedding_engine())
            st.session_state.messages = []
            st.session_state.uploader_generation += 1
            st.rerun()

        st.markdown("---")
        st.caption("Catalog and chat stay in this browser session. This demo has no sign-in, checkout, or production security controls.")

    if not model_ready:
        st.warning(
            "Ollama could not find a supported local model. Start Ollama and install a model with "
            "`ollama pull qwen2.5:3b` or `ollama pull llama3.2:3b`. Qwen is preferred when both are installed."
        )

    metrics = st.columns(3)
    product_count = sum(document.get("item_count", 0) for document in pipeline.index.documents)
    metrics[0].metric("Product records", product_count)
    metrics[1].metric("Searchable passages", len(pipeline.index.chunks))
    metrics[2].metric("Answer model", model_name if model_ready else "Not configured")

    if not pipeline.index.documents:
        st.markdown(
            """
            <section class="welcome-panel">
              <div class="welcome-mark">S</div>
              <div><h2>Shopping, made more personal.</h2>
              <p>Load the sample catalog or add Sai Stores product descriptions and customer reviews.</p></div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        sample_path = Path(__file__).resolve().parent / "data" / "sai_stores_demo_catalog.csv"
        if sample_path.exists() and st.button("Explore the Sai Stores sample catalog", type="primary"):
            pipeline.process_document(sample_path.name, sample_path.read_bytes())
            st.rerun()
        st.info("Or import a CSV/JSON feed in the sidebar. Product records should include descriptions and review fields for best recommendations.")
        if not pipeline.index.documents:
            return

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message["role"] == "assistant":
                render_sources(message.get("sources", []))

    if not st.session_state.messages:
        st.markdown("#### Try asking")
        suggestions = [
            "Find me a lightweight laptop for college under $900.",
            "Which headphones have noise cancellation and good reviews?",
            "Compare the best-rated products under $100.",
        ]
        suggestion_columns = st.columns(3)
        suggested_question = None
        for column, suggestion in zip(suggestion_columns, suggestions):
            if column.button(suggestion, use_container_width=True):
                suggested_question = suggestion
    else:
        suggested_question = None

    question = st.chat_input("Ask for a product recommendation or comparison...")
    question = question or suggested_question
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Searching relevant passages..."):
                try:
                    preference_parts = []
                    if shopping_for.strip():
                        preference_parts.append(f"Shopping use: {shopping_for.strip()}")
                    if budget.strip():
                        preference_parts.append(f"Budget: {budget.strip()}")
                    if priorities.strip():
                        preference_parts.append(f"Priorities: {priorities.strip()}")
                    result = pipeline.answer_question(question, preferences="\n".join(preference_parts))
                except Exception:
                    result = {
                        "answer": "I couldn't complete that request. Check that Ollama is running and try again.",
                        "sources": [],
                    }
            st.write(result["answer"])
            render_sources(result.get("sources", []))
        st.session_state.messages.append(
            {"role": "assistant", "content": result["answer"], "sources": result.get("sources", [])}
        )
        st.rerun()


if __name__ == "__main__":
    main()
