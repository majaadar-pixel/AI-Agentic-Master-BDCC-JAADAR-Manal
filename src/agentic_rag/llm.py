from __future__ import annotations

import re


class AnswerGenerator:
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini") -> None:
        self.api_key = api_key
        self.model = model
        self._chat_model = None
        if api_key:
            try:
                from langchain_openai import ChatOpenAI

                self._chat_model = ChatOpenAI(model=model, temperature=0.1, api_key=api_key)
            except Exception:
                self._chat_model = None

    def generate(self, question: str, context: str, sources: list[str]) -> str:
        if self._chat_model is not None:
            prompt = (
                "Tu es un assistant RAG. Reponds en francais uniquement avec les "
                "informations du contexte. Cite les sources en fin de reponse.\n\n"
                f"Question: {question}\n\nContexte:\n{context}\n\nReponse:"
            )
            response = self._chat_model.invoke(prompt)
            return str(response.content)
        return self._local_answer(question, context, sources)

    def _local_answer(self, question: str, context: str, sources: list[str]) -> str:
        cleaned_context = re.sub(r"\[[^\]]+\]", " ", context)
        cleaned_context = re.sub(r"#+\s*", "", cleaned_context)
        sentences = re.split(r"(?<=[.!?])\s+", cleaned_context.replace("\n", " "))
        terms = {
            token.lower()
            for token in re.findall(r"[A-Za-zÀ-ÿ0-9]{4,}", question)
            if token.lower() not in LOCAL_STOP_WORDS
        }
        ranked = sorted(
            sentences,
            key=lambda sentence: sum(1 for term in terms if term in sentence.lower()),
            reverse=True,
        )
        selected = [s for s in ranked[:4] if s.strip()]
        if not selected:
            return (
                "Je ne trouve pas assez d'information dans le corpus pour repondre "
                "de maniere fiable."
            )
        answer = " ".join(selected)
        return f"{answer}\n\nSources: {', '.join(sources)}"

    def rewrite_query(self, question: str) -> str:
        keywords = re.findall(r"[A-Za-zÀ-ÿ0-9]{4,}", question.lower())
        filtered = [word for word in keywords if word not in LOCAL_STOP_WORDS]
        if not filtered:
            return question
        return " ".join(dict.fromkeys(filtered + ["rag", "langgraph", "evaluation"]))


LOCAL_STOP_WORDS = {
    "avec",
    "dans",
    "comment",
    "pourquoi",
    "quels",
    "quelle",
    "elles",
    "sont",
    "etre",
    "faire",
    "d'une",
    "d'un",
    "leur",
    "plus",
    "moins",
    "entre",
    "systeme",
    "projet",
}
