from typing import Dict, Any
from app.node_models.threat_classification import ThreatClassification
from app.nodes.llm import llm, threat_analysis_prompt

# def classify_threat(state: Dict[str, Any]) -> Dict[str, Any]:
#     """Very simple keyword-based classifier placeholder."""
#     desc = (state.get("normalized_item") or {}).get("description", "") or ""
#     lower = desc.lower()

#     if "ransomware" in lower:
#         threat_type = "Ransomware"
#         severity = "High"
#     elif "remote code execution" in lower or "rce" in lower:
#         threat_type = "RCE"
#         severity = "Critical"
#     elif "phishing" in lower or "credential" in lower:
#         threat_type = "Phishing"
#         severity = "Medium"
#     else:
#         threat_type = "Other"
#         severity = "Medium"

#     state.update({"threat_type": threat_type, "severity": severity})
#     return state

structured_llm = llm.with_structured_output(ThreatClassification)
structured_llm_with_system_prompt = threat_analysis_prompt | structured_llm

def classify_threat(state: Dict[str, Any]) -> Dict[str, Any]:
    """Classify threat using LLM based on normalized description."""
    normalized_item = state.get("normalized_item", {})
    description = normalized_item.get("description", "")

    prompt = f"""
    Based on the following threat description, classify the threat type and assign a severity level.

    Threat Description:
    {description}

    Classify the threat into one of the following types: Ransomware, Remote Code Execution (RCE), Phishing, or Other.
    Assign a severity level: Critical, High, Medium, Low.

    Provide your response in the format:
    Threat Type: <type>
    Severity: <level>
    """

    # response = response = structured_llm.invoke({"input": prompt})

    # threat_type = "Other"
    # severity = "Medium"

    # for line in response.splitlines():
    #     if line.startswith("Threat Type:"):
    #         threat_type = line.split(":", 1)[1].strip()
    #     elif line.startswith("Severity:"):
    #         severity = line.split(":", 1)[1].strip()
    # state.update({"threat_type": threat_type, "severity": severity})

    # Invoke returns a ThreatClassification object, not text
    response = structured_llm_with_system_prompt.invoke({"input": prompt})
    state.update({
        "threat_type": response.threat_type,
        "severity": response.severity
    })
    
    return state