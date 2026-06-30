from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.agentic_rag.graph import ask

QUESTIONS_PATH = ROOT / "evaluation" / "questions.json"
OUTPUTS = ROOT / "outputs"


def main() -> None:
    OUTPUTS.mkdir(exist_ok=True)
    questions = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    results = []

    for item in questions:
        state = ask(item["question"], thread_id=f"eval-{item['id']}")
        docs = state.get("documents", [])
        avg_score = round(sum(doc["score"] for doc in docs) / max(len(docs), 1), 4)
        results.append(
            {
                **item,
                "answer": state.get("answer", ""),
                "sources": state.get("sources", []),
                "elapsed_ms": state.get("elapsed_ms", 0),
                "iterations": state.get("iterations", 0),
                "retrieval_avg_score": avg_score,
                "top_document": docs[0]["source"] if docs else None,
                "grade": state.get("grade", {}),
            }
        )

    (OUTPUTS / "evaluation_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_markdown_report(results)
    print(f"Evaluation terminee: {OUTPUTS / 'evaluation_results.json'}")


def write_markdown_report(results: list[dict]) -> None:
    simple = [r for r in results if r["type"] == "simple"]
    complexe = [r for r in results if r["type"] == "complexe"]
    avg_time = sum(r["elapsed_ms"] for r in results) / len(results)
    avg_score = sum(r["retrieval_avg_score"] for r in results) / len(results)
    lines = [
        "# Resultats d'evaluation",
        "",
        f"- Questions simples: {len(simple)}",
        f"- Questions complexes: {len(complexe)}",
        f"- Temps moyen: {avg_time:.2f} ms",
        f"- Score moyen de recuperation: {avg_score:.4f}",
        "",
        "| ID | Type | Temps ms | Score docs | Iterations | Sources |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for result in results:
        sources_text = ", ".join(result["sources"])
        lines.append(
            "| {id} | {type} | {elapsed_ms:.2f} | {retrieval_avg_score:.4f} | "
            "{iterations} | {sources_text} |".format(
                **result,
                sources_text=sources_text,
            )
        )
    lines.extend(
        [
            "",
            "## Analyse",
            "",
            "Le systeme repond correctement aux questions directes lorsque les mots de la question sont proches du corpus. Les questions complexes mobilisent plusieurs documents et montrent l'interet du graphe : evaluation de la pertinence, reformulation si necessaire, puis generation avec sources.",
            "",
            "Les limites principales sont la vectorisation TF-IDF, moins semantique que des embeddings denses, et le generateur local extractif utilise en absence de cle API. Une version de production devrait ajouter un modele LLM distant, un reranker et une evaluation humaine.",
        ]
    )
    (OUTPUTS / "evaluation_report.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
