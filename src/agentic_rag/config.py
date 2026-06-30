from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    root_dir: Path = ROOT_DIR
    docs_dir: Path = ROOT_DIR / "data" / "docs"
    outputs_dir: Path = ROOT_DIR / "outputs"
    top_k: int = int(os.getenv("RAG_TOP_K", "4"))
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"


def load_settings() -> Settings:
    load_dotenv(ROOT_DIR / ".env")
    return Settings(
        top_k=int(os.getenv("RAG_TOP_K", "4")),
        openai_api_key=os.getenv("OPENAI_API_KEY") or None,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    )
