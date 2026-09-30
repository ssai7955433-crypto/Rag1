from core.model_selector import choose_model


def test_qwen_is_preferred_over_llama():
    models = ["llama3.2:latest", "llama3.2:3b", "qwen2.5:3b"]
    assert choose_model(models) == ("qwen2.5:3b", "Qwen")


def test_llama_is_selected_as_fallback():
    assert choose_model(["llama3.2:latest", "llama3.2:3b"]) == ("llama3.2:latest", "Llama")


def test_no_supported_model_is_reported():
    assert choose_model(["mistral:7b"]) == (None, None)
