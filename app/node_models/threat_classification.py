from pydantic import BaseModel

# Define the expected output structure
class ThreatClassification(BaseModel):
    threat_type: str  # Ransomware, RCE, Phishing, Other
    severity: str     # Critical, High, Medium, Low