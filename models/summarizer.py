from transformers import pipeline

_summarizer = None

def _load_model():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )
    return _summarizer


def generate_summary(text: str) -> str:
    if len(text) < 50:
        return text

    model = _load_model()
    result = model(text, max_length=150, min_length=50, do_sample=False)
    return result[0]["summary_text"]
