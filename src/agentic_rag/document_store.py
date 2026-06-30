from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class DocumentChunk:
    id: str
    source: str
    text: str


@dataclass(frozen=True)
class SearchResult:
    chunk: DocumentChunk
    score: float


def _split_text(text: str, max_words: int = 120, overlap: int = 25) -> list[str]:
    words = re.findall(r"\S+", text)
    if not words:
        return []
    chunks: list[str] = []
    step = max_words - overlap
    for start in range(0, len(words), step):
        part = words[start : start + max_words]
        if part:
            chunks.append(" ".join(part))
        if start + max_words >= len(words):
            break
    return chunks


class DocumentStore:
    def __init__(self, docs_dir: Path) -> None:
        self.docs_dir = docs_dir
        self.chunks = self._load_chunks()
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            ngram_range=(1, 2),
            stop_words=list(FRENCH_STOP_WORDS),
        )
        self.matrix = self.vectorizer.fit_transform([chunk.text for chunk in self.chunks])

    def _load_chunks(self) -> list[DocumentChunk]:
        chunks: list[DocumentChunk] = []
        for path in sorted(self.docs_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for index, chunk_text in enumerate(_split_text(text)):
                chunks.append(
                    DocumentChunk(
                        id=f"{path.stem}-{index + 1}",
                        source=path.name,
                        text=chunk_text,
                    )
                )
        if not chunks:
            raise ValueError(f"Aucun document trouve dans {self.docs_dir}")
        return chunks

    def search(self, query: str, top_k: int = 4) -> list[SearchResult]:
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).ravel()
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [
            SearchResult(chunk=self.chunks[i], score=float(scores[i]))
            for i in top_indices
            if scores[i] > 0
        ]


FRENCH_STOP_WORDS = {
    "a",
    "au",
    "aux",
    "avec",
    "ce",
    "ces",
    "dans",
    "de",
    "des",
    "du",
    "elle",
    "en",
    "et",
    "eux",
    "il",
    "je",
    "la",
    "le",
    "les",
    "leur",
    "lui",
    "ma",
    "mais",
    "me",
    "meme",
    "mes",
    "moi",
    "mon",
    "ne",
    "nos",
    "notre",
    "nous",
    "on",
    "ou",
    "par",
    "pas",
    "pour",
    "qu",
    "que",
    "qui",
    "sa",
    "se",
    "ses",
    "son",
    "sur",
    "ta",
    "te",
    "tes",
    "toi",
    "ton",
    "tu",
    "un",
    "une",
    "vos",
    "votre",
    "vous",
}
