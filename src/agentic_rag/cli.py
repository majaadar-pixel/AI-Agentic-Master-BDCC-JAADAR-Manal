from __future__ import annotations

import argparse

from .graph import ask


def main() -> None:
    parser = argparse.ArgumentParser(description="Interroger l'agent RAG LangGraph.")
    parser.add_argument("question", help="Question a poser au systeme")
    args = parser.parse_args()

    result = ask(args.question)
    print(result["answer"])
    print()
    print(f"Sources: {', '.join(result.get('sources', []))}")
    print(f"Temps: {result.get('elapsed_ms')} ms")


if __name__ == "__main__":
    main()
