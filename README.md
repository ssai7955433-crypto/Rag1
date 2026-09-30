# Sai Stores E-commerce Product Advisor

A local shopping assistant that searches product descriptions and customer reviews, then recommends and compares products using the shopper's stated budget, use case, and priorities. It uses local embeddings and Ollama; Qwen is preferred, with Llama as fallback.

## Run locally

From the `Rag1` folder, use Python 3.11 or newer and an installed/running Ollama service:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

The current Ollama tags `qwen2.5:3b`, `llama3.2:3b`, and `llama3.2:latest` are supported. The app selects Qwen first. If you need to install one, use `ollama pull qwen2.5:3b` or `ollama pull llama3.2:3b`. The app does not automatically pull an Ollama model. The Sentence Transformers embedding model is downloaded the first time unless already cached.

## Try it

1. Open the local Streamlit URL, usually http://localhost:8501.
2. Select **Explore the Sai Stores sample catalog**, or import a store catalog in the sidebar.
3. Add a use case, budget, and priorities in the sidebar, then ask for a recommendation or comparison.
4. Expand **Catalog evidence** to inspect the exact product/review passages and similarity scores used.

The included sample catalog is fictional demo data. It contains six products with sample descriptions, ratings, and reviews.

## Catalog input

The app accepts:

- **CSV:** one product per row; common fields include `product_name` or `title`, `sku`, `brand`, `category`, `price`, `currency`, `availability`, `average_rating`, `description`, `features`, and `reviews` or `review_body`.
- **JSON:** a list of product objects, one product object, or an object with a `products` list. Nested features/reviews are converted into searchable text.
- **PDF/DOCX:** useful for product brochures or curated review summaries; tabular CSV/JSON feeds usually give better product-level citations.

For a live shopping site, export the catalog and review feed to CSV/JSON and upload them. A production integration can replace the upload path with a Shopify, WooCommerce, or store-specific API adapter that maps catalog and review records into the same product fields. No store API credentials or live-site connection are configured in this demo.

## How recommendations work

```text
Catalog + reviews -> normalize -> chunk per product -> local embeddings
                   -> cosine similarity -> matching products -> Ollama answer
```

The app combines the shopper's question with optional use case, budget, and priority fields for retrieval. It then sends only the top matching passages to Ollama. The model is instructed not to invent prices, specifications, availability, ratings, or review claims, and to explain why a product matches. This is retrieval-augmented generation: the LLM only sees the catalog evidence retrieved for that turn, not the entire store catalog.

Cosine similarity is `(a · b) / (||a|| ||b||)` and compares the direction of the question and product vectors. Top-K and minimum relevance can be adjusted in the sidebar. Sources show the imported file, product row (for structured feeds), chunk identifier, and similarity score.

## Project files

```text
Rag1/
├── app.py
├── core/
│   ├── document_loader.py  # PDF, DOCX, CSV, and JSON imports
│   ├── text_cleaner.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── model_selector.py
│   ├── ollama_client.py
│   └── rag_pipeline.py
├── data/sai_stores_demo_catalog.csv
├── tests/
├── ui/styles.py
└── requirements.txt
```

## Example questions

- Find me a lightweight laptop for college under $900.
- Which headphones have noise cancellation and good reviews?
- Compare the best-rated products under $100.
- I need a light daypack for campus. What do customers mention about it?

## Tests

```powershell
python -m pytest
```

Tests cover catalog parsing, text cleanup, chunking, cosine retrieval, and Qwen/Llama selection. They do not call Ollama or download the embedding model.

## Limits and safety

Catalogs and chat are held in the current Streamlit session and are not persisted. This is a local demo, not a production storefront: it has no customer accounts, checkout, inventory synchronization, store API credentials, or production security controls. Product descriptions and reviews are untrusted data and are treated as reference material, not instructions. Verify current price, inventory, and return policy on the actual Sai Stores storefront before purchase.