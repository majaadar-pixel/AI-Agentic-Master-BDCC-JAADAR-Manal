from __future__ import annotations

import time
from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from .config import load_settings
from .document_store import DocumentStore
from .llm import AnswerGenerator
from .tools import build_context, compact_sources, grade_retrieval, retrieve_documents


class AgentState(TypedDict, total=False):
    question: str
    search_query: str
    documents: list[dict]
    grade: dict
    answer: str
    sources: list[str]
    iterations: int
    started_at: float
    elapsed_ms: float
    memory: list[dict]


def build_graph():
    settings = load_settings()
    settings.outputs_dir.mkdir(exist_ok=True)
    store = DocumentStore(settings.docs_dir)
    generator = AnswerGenerator(settings.openai_api_key, settings.openai_model)

    def plan(state: AgentState) -> AgentState:
        question = state["question"].strip()
        return {
            **state,
            "search_query": question,
            "iterations": state.get("iterations", 0),
            "started_at": state.get("started_at", time.perf_counter()),
            "memory": state.get("memory", []),
        }

    def retrieve(state: AgentState) -> AgentState:
        documents = retrieve_documents(store, state["search_query"], settings.top_k)
        return {**state, "documents": documents, "iterations": state.get("iterations", 0) + 1}

    def grade(state: AgentState) -> AgentState:
        return {**state, "grade": grade_retrieval(state.get("documents", []))}

    def rewrite(state: AgentState) -> AgentState:
        rewritten = generator.rewrite_query(state["question"])
        return {**state, "search_query": rewritten}

    def generate(state: AgentState) -> AgentState:
        docs = state.get("documents", [])
        sources = compact_sources(docs)
        context = build_context(docs)
        answer = generator.generate(state["question"], context, sources)
        return {**state, "answer": answer, "sources": sources}

    def finalize(state: AgentState) -> AgentState:
        elapsed_ms = (time.perf_counter() - state["started_at"]) * 1000
        memory = state.get("memory", []) + [
            {
                "question": state["question"],
                "answer": state.get("answer", ""),
                "sources": state.get("sources", []),
            }
        ]
        return {**state, "elapsed_ms": round(elapsed_ms, 2), "memory": memory}

    def route_after_grade(state: AgentState) -> str:
        if state.get("grade", {}).get("relevant"):
            return "generate"
        if state.get("iterations", 0) < 2:
            return "rewrite"
        return "generate"

    workflow = StateGraph(AgentState)
    workflow.add_node("plan", plan)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade", grade)
    workflow.add_node("rewrite", rewrite)
    workflow.add_node("generate", generate)
    workflow.add_node("finalize", finalize)

    workflow.set_entry_point("plan")
    workflow.add_edge("plan", "retrieve")
    workflow.add_edge("retrieve", "grade")
    workflow.add_conditional_edges(
        "grade",
        route_after_grade,
        {"generate": "generate", "rewrite": "rewrite"},
    )
    workflow.add_edge("rewrite", "retrieve")
    workflow.add_edge("generate", "finalize")
    workflow.add_edge("finalize", END)

    return workflow.compile(checkpointer=MemorySaver())


def ask(question: str, thread_id: str = "default") -> AgentState:
    graph = build_graph()
    config = {"configurable": {"thread_id": thread_id}}
    return graph.invoke({"question": question}, config=config)
