from typing import Dict, Any, List
from app.schemas import ThreatSummary


def guardrails_validate(state: Dict[str, Any]) -> Dict[str, Any]:
    """Pydantic-based validation stub (replace with Guardrails)."""
    errors: List[str] = []
    try:
        ThreatSummary(
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
    except Exception as ex:  # noqa: BLE001
        errors.append(str(ex))

    summary = state.get("summary") or ""
    if "http://" in summary or "https://" in summary:
        errors.append("Summary must not contain URLs.")

    state["validation_errors"] = errors
    return state
