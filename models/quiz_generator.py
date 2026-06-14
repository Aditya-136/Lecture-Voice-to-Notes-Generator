import random


def generate_quiz(text: str, num_questions: int = 5) -> list[dict]:
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 20]

    if not sentences:
        return []

    selected = random.sample(sentences, min(num_questions, len(sentences)))
    quiz = []

    for sentence in selected:
        words = sentence.split()
        if len(words) <= 5:
            continue

        answer = random.choice(words)
        question = sentence.replace(answer, "_____", 1)
        quiz.append({"question": question, "answer": answer})

    return quiz
