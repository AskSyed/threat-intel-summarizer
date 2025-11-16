from typing import List, Dict, Any, Optional, TypedDict


class ThreatState(TypedDict, total=False):
    """State schema for threat intelligence processing."""
    feed_url: Optional[str]
    sample_path: str
    raw_feed: Dict[str, Any]
    current_index: int
    normalized_item: Dict[str, Any]
    title: str
    description: str
    source: str
    published_at: str
    threat_type: str
    severity: str
    summary: str
    affected_products: List[str]
    recommended_action: str
    cve_id: Optional[str]
    validation_errors: Optional[List[str]]