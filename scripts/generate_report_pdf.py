from __future__ import annotations

import json
import re
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
REPORT_MD = ROOT / "rapport_final.md"
RESULTS_JSON = ROOT / "outputs" / "evaluation_results.json"
REPORT_PDF = ROOT / "rapport_final.pdf"


def clean_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> None:
    styles = getSampleStyleSheet()
    story = []
    content = REPORT_MD.read_text(encoding="utf-8").splitlines()

    for line in content:
        if not line.strip():
            story.append(Spacer(1, 8))
            continue
        if line.startswith("# "):
            story.append(Paragraph(clean_inline(line[2:]), styles["Title"]))
        elif line.startswith("## "):
            story.append(Paragraph(clean_inline(line[3:]), styles["Heading2"]))
        else:
            story.append(Paragraph(clean_inline(line), styles["BodyText"]))

    if RESULTS_JSON.exists():
        results = json.loads(RESULTS_JSON.read_text(encoding="utf-8"))
        avg_time = sum(r["elapsed_ms"] for r in results) / len(results)
        avg_score = sum(r["retrieval_avg_score"] for r in results) / len(results)
        story.append(Spacer(1, 12))
        story.append(Paragraph("Synthese chiffree", styles["Heading2"]))
        story.append(
            Paragraph(
                clean_inline(
                    f"Evaluation executee sur {len(results)} questions. "
                    f"Temps moyen: {avg_time:.2f} ms. "
                    f"Score moyen de recuperation: {avg_score:.4f}."
                ),
                styles["BodyText"],
            )
        )

    doc = SimpleDocTemplate(
        str(REPORT_PDF),
        pagesize=A4,
        rightMargin=42,
        leftMargin=42,
        topMargin=42,
        bottomMargin=42,
    )
    doc.build(story)
    print(f"Rapport PDF genere: {REPORT_PDF}")


if __name__ == "__main__":
    main()
