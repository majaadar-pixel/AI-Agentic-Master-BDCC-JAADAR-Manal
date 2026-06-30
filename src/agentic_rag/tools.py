from __future__ import annotations

from dataclasses import asdict

from .document_store import DocumentStore, SearchResult


def retrieve_documents(store: DocumentStore, query: str, top_k: int) -> list[dict]:
    results = store.search(query, top_k=top_k)
    return [serialize_result(result) for result in results]


def serialize_result(result: SearchResult) -> dict:
    return {
        "id": result.chunk.id,
        "source": result.chunk.source,
        "text": result.chunk.text,
        "score": round(result.score, 4),
    }


def grade_retrieval(documents: list[dict]) -> dict:
    if not documents:
        return {"relevant": False, "score": 0.0, "reason": "Aucun document recupere."}
    score = sum(float(doc["score"]) for doc in documents[:3]) / min(len(documents), 3)
    relevant = score >= 0.08 or float(documents[0]["score"]) >= 0.12
    reason = "Contexte suffisant." if relevant else "Scores faibles, recherche a reformuler."
    return {"relevant": relevant, "score": round(score, 4), "reason": reason}


def build_context(documents: list[dict]) -> str:
    return "\n\n".join(
        f"[{doc['source']} | score={doc['score']}]\n{doc['text']}" for doc in documents
    )


def compact_sources(documents: list[dict]) -> list[str]:
    sources: list[str] = []
    for doc in documents:
        if doc["source"] not in sources:
            sources.append(doc["source"])
    return sources
