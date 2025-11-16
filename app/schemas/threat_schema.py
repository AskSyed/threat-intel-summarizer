from typing import List, Optional
from pydantic import BaseModel, Field


class ThreatSummary(BaseModel):
    title: str = Field(max_length=250)
    threat_type: str = Field(description="e.g. Malware, Ransomware, RCE, Phishing, Other")
    severity: str = Field(description="Low, Medium, High, Critical")
    summary: str = Field(min_length=40, max_length=600)
    affected_products: List[str] = []
    recommended_action: str = Field(min_length=20, max_length=400)
    cve_id: Optional[str] = None
    source: Optional[str] = None
    published_at: Optional[str] = None
