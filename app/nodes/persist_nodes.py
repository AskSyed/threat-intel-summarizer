from typing import Dict, Any, List
from datetime import datetime
from app.schemas import ThreatSummary


def persist_to_db(state: Dict[str, Any]) -> Dict[str, Any]:
    """Stub persistence – prints to console and stores fake IDs."""
    summary = ThreatSummary(
        title=state.get("title", ""),
        threat_type=state.get("threat_type", ""),
        severity=state.get("severity", ""),
        summary=state.get("summary", ""),
        affected_products=state.get("affected_products", []),
        recommended_action=state.get("recommended_action", ""),
        cve_id=state.get("cve_id"),
        source=state.get("source"),
        published_at=state.get("published_at"),
    )
    fake_id = f"T-{int(datetime.utcnow().timestamp())}"
    print("Persisting threat summary:", summary.model_dump())
    print("Assigned ID:", fake_id)
    ids: List[str] = state.get("db_ids", [])
    ids.append(fake_id)
    state["db_ids"] = ids
    return state
