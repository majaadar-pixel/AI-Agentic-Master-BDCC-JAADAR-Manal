# Repository Guidelines

## Project Structure & Module Organization

This repository contains an Agentic RAG project built with LangGraph.

- `src/agentic_rag/`: application code, including graph orchestration, document store, tools, CLI, and LLM fallback logic.
- `data/docs/`: Markdown knowledge base used for retrieval.
- `evaluation/questions.json`: 10 simple and 10 complex evaluation questions.
- `scripts/`: utility scripts for evaluation, graph visualization, and PDF report generation.
- `outputs/`: generated evaluation results and graph files.
- `rapport_final.md` and `rapport_final.pdf`: final individual report.

Keep new runtime code under `src/agentic_rag/`. Keep generated artifacts in `outputs/` unless they are final deliverables.

## Build, Test, and Development Commands

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run a single question through the CLI:

```powershell
python -m src.agentic_rag.cli "Qu'est-ce qu'un systeme RAG ?"
```

Run the full evaluation:

```powershell
python scripts/run_evaluation.py
```

Generate the graph visualization:

```powershell
python scripts/visualize_graph.py
```

Generate the PDF report:

```powershell
python scripts/generate_report_pdf.py
```

Check Python syntax:

```powershell
python -m compileall src scripts
```

## Coding Style & Naming Conventions

Use Python 3.12-compatible code with 4-space indentation. Prefer type hints and small functions with explicit responsibilities. Module and function names should use `snake_case`; classes should use `PascalCase`. Keep comments concise and only add them where they clarify non-obvious graph or retrieval behavior.

## Testing Guidelines

There is no dedicated unit test suite yet. Use `python -m compileall src scripts` for syntax checks and `python scripts/run_evaluation.py` for functional validation. When adding tests later, place them under `tests/` and name files `test_*.py`.

## Commit & Pull Request Guidelines

No Git history is available in this workspace, so use clear conventional-style commit messages such as `feat: add retrieval reranking` or `fix: handle empty corpus`. Pull requests should include a short summary, commands run, generated output changes, and screenshots only when UI or graph rendering changes.

## Security & Configuration Tips

Do not commit `.env` or API keys. Use `.env.example` as the template. The project runs without an OpenAI key using the local extractive fallback; set `OPENAI_API_KEY` only when testing LLM-backed generation.
