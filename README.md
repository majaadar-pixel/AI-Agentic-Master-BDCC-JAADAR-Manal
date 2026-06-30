# Agentic RAG avec LangGraph

Projet d'evaluation finale : conception et evaluation d'un systeme RAG agentique base sur LangGraph.

Le systeme repond a des questions en francais a partir d'un petit corpus Markdown local. Il combine une recherche documentaire TF-IDF, un graphe agentique LangGraph, une evaluation de pertinence, une reecriture de requete si necessaire et une generation de reponse avec sources.

## Fonctionnalites

- Chargement d'un corpus Markdown depuis `data/docs/`.
- Decoupage des documents en chunks avec recouvrement.
- Recherche semantique locale avec `TfidfVectorizer` et similarite cosinus.
- Graphe LangGraph avec etapes `plan`, `retrieve`, `grade`, `rewrite`, `generate` et `finalize`.
- Memoire conversationnelle via `MemorySaver`.
- Generation de reponse avec OpenAI si `OPENAI_API_KEY` est configuree.
- Fallback local extractif lorsque aucune cle API n'est fournie.
- Evaluation automatique sur 20 questions.
- Generation d'une visualisation Mermaid du graphe.
- Generation du rapport final en PDF.

## Structure du projet

```text
.
|-- data/docs/                  # Corpus documentaire Markdown
|-- evaluation/questions.json   # Questions simples et complexes d'evaluation
|-- outputs/                    # Resultats et graphes generes
|-- scripts/                    # Scripts d'evaluation, visualisation et PDF
|-- src/agentic_rag/            # Code applicatif principal
|   |-- cli.py                  # Interface en ligne de commande
|   |-- config.py               # Configuration et variables d'environnement
|   |-- document_store.py       # Indexation, chunking et recherche TF-IDF
|   |-- graph.py                # Graphe LangGraph
|   |-- llm.py                  # Generation OpenAI ou fallback local
|   `-- tools.py                # Outils de retrieval et synthese
|-- rapport_final.md            # Rapport individuel
|-- rapport_final.pdf           # Rapport PDF genere
|-- requirements.txt            # Dependances Python
`-- .env.example                # Exemple de configuration
```

## Prerequis

- Python 3.12 ou compatible.
- PowerShell sous Windows.
- Une cle OpenAI est optionnelle. Sans cle, le projet utilise le fallback local extractif.

## Installation

Creer et activer un environnement virtuel :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installer les dependances :

```powershell
pip install -r requirements.txt
```

Creer le fichier d'environnement local :

```powershell
copy .env.example .env
```

Pour utiliser un LLM OpenAI, renseigner `OPENAI_API_KEY` dans `.env`. Sinon, laisser la variable vide.

## Utilisation

Executer une question depuis la CLI :

```powershell
python -m src.agentic_rag.cli "Qu'est-ce qu'un systeme RAG ?"
```

Autre exemple :

```powershell
python -m src.agentic_rag.cli "Comment LangGraph ameliore-t-il un systeme RAG ?"
```

## Evaluation

Lancer l'evaluation complete :

```powershell
python scripts/run_evaluation.py
```

Les resultats sont generes dans `outputs/`, notamment :

- `outputs/evaluation_results.json`
- `outputs/evaluation_report.md`

## Visualisation du graphe

Generer la representation du graphe LangGraph :

```powershell
python scripts/visualize_graph.py
```

Sorties attendues :

- `outputs/graph.mmd`
- `outputs/graph.html`

## Rapport PDF

Generer le rapport final PDF :

```powershell
python scripts/generate_report_pdf.py
```

Le fichier produit est `rapport_final.pdf`.

## Verification

Verifier la syntaxe Python :

```powershell
python -m compileall src scripts
```

Validation fonctionnelle recommandee :

```powershell
python scripts/run_evaluation.py
```

## Configuration

Les principales variables d'environnement sont definies dans `.env.example`.

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```

Si `OPENAI_API_KEY` est absent, `src/agentic_rag/llm.py` utilise une generation locale extractive. Ce mode permet de tester le projet sans service externe.

## Notes de developpement

- Ajouter le code applicatif dans `src/agentic_rag/`.
- Ajouter les nouveaux documents de connaissance dans `data/docs/`.
- Conserver les artefacts generes dans `outputs/`.
- Ne pas versionner `.env`, les caches Python, les environnements virtuels ou les cles API.
