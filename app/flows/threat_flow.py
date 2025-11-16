from app.node_models.threat_state import ThreatState
from langgraph.graph import StateGraph, START, END

from app.nodes import (
    fetch_threat_feed,
    parse_and_normalize,
    classify_threat,
    summarize_threat,
    guardrails_validate,
    persist_to_db,
)

def build_threat_flow() -> StateGraph:
    graph = StateGraph(ThreatState)

    graph.add_node("fetch_threat_feed", fetch_threat_feed)
    graph.add_node("parse_and_normalize", parse_and_normalize)
    graph.add_node("classify_threat", classify_threat)
    graph.add_node("summarize_threat", summarize_threat)
    graph.add_node("guardrails_validate", guardrails_validate)
    graph.add_node("persist_to_db", persist_to_db)

    graph.add_edge(START, "fetch_threat_feed")
    graph.add_edge("fetch_threat_feed", "parse_and_normalize")
    graph.add_edge("parse_and_normalize", "classify_threat")
    graph.add_edge("classify_threat", "summarize_threat")
    graph.add_edge("summarize_threat", "guardrails_validate")

    def validation_router(state: ThreatState) -> str:
        if state.get("validation_errors"):
            return "retry"
        return "ok"

    graph.add_conditional_edges(
        "guardrails_validate",
        validation_router,
        {"ok": "persist_to_db", "retry": "summarize_threat"},
    )

    graph.add_edge("persist_to_db", END)
    return graph
