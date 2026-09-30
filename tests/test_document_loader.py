import json

from core.document_loader import load_document


def test_csv_catalog_extracts_product_description_and_reviews():
    csv_text = (
        "title,sku,price,description,review_body\n"
        'EchoBuds,EB-1,79.99,"Wireless noise cancelling earbuds","Comfortable fit and clear calls"\n'
    )

    document = load_document(csv_text.encode("utf-8"), "products.csv")

    assert document.source_type == "csv_catalog"
    assert document.page_count == 1
    assert "Product: EchoBuds" in document.text
    assert "Description: Wireless noise cancelling earbuds" in document.text
    assert "Customer reviews: Comfortable fit and clear calls" in document.text


def test_json_products_list_is_parsed():
    payload = {"products": [{"name": "Trail Pack", "features": ["20 L", "lightweight"], "reviews": [{"text": "Roomy"}]}]}

    document = load_document(json.dumps(payload).encode("utf-8"), "products.json")

    assert document.source_type == "json_catalog"
    assert document.page_count == 1
    assert "Trail Pack" in document.text
    assert "20 L; lightweight" in document.text
    assert "Roomy" in document.text
