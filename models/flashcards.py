def generate_flashcards(text: str, limit: int = 5) -> list[dict]:
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 20]
    cards = []

    for i, sentence in enumerate(sentences[:limit]):
        # Use position in text as a rough cue for what's being asked
        cue = f"Explain point {i + 1} from the lecture."
        cards.append({"question": cue, "answer": sentence})

    return cards
