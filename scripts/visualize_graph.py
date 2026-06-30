from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"

MERMAID = """flowchart TD
    A[plan: analyser la question] --> B[retrieve: rechercher les documents]
    B --> C[grade: evaluer la pertinence]
    C -->|contexte suffisant| D[generate: produire la reponse]
    C -->|score faible et iteration < 2| E[rewrite: reformuler la requete]
    E --> B
    D --> F[finalize: ajouter sources, temps et memoire]
    F --> G([END])
"""

HTML = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Graphe Agentic RAG</title>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({{ startOnLoad: true }});
  </script>
</head>
<body>
  <pre class="mermaid">
{MERMAID}
  </pre>
</body>
</html>
"""


def main() -> None:
    OUTPUTS.mkdir(exist_ok=True)
    (OUTPUTS / "graph.mmd").write_text(MERMAID, encoding="utf-8")
    (OUTPUTS / "graph.html").write_text(HTML, encoding="utf-8")
    print(f"Graphe ecrit dans {OUTPUTS / 'graph.mmd'} et {OUTPUTS / 'graph.html'}")


if __name__ == "__main__":
    main()
