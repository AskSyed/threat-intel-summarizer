from typing import Dict, Any
import re
from app.nodes.llm import llm_with_system_prompt


# def summarize_threat(state: Dict[str, Any]) -> Dict[str, Any]:
#     """Simple template-based summary placeholder."""
#     norm = state.get("normalized_item") or {}
#     title = norm.get("title", "Untitled threat")
#     desc = norm.get("description", "") or ""

#     summary_text = (
#         f"{title}. {desc} "
#         f"This threat has been automatically classified as {state.get('threat_type')} "
#         f"with {state.get('severity')} severity. Organizations should review affected "
#         f"systems and apply available patches or mitigations."
#     )

#     affected_products = []
#     for product in ["Windows", "Linux", "Apache", "Exchange", "VPN", "Cisco", "Fortinet"]:
#         if product.lower() in desc.lower():
#             affected_products.append(product)

#     recommended_action = (
#         "Review vendor advisories, apply patches as soon as possible, "
#         "and monitor systems for related indicators of compromise."
#     )

#     m = re.search(r"CVE-\d{4}-\d+", desc)
#     cve_id = m.group(0) if m else None

#     state.update(
#         {
#             "summary": summary_text[:590],
#             "affected_products": affected_products,
#             "recommended_action": recommended_action,
#             "cve_id": cve_id,
#         }
#     )
#     return state

def summarize_threat(state: Dict[str, Any]) -> Dict[str, Any]:
    """Summarize threat using LLM based on normalized description and classification."""
    normalized_item = state.get("normalized_item", {})
    description = normalized_item.get("description", "")
    threat_type = state.get("threat_type", "Other")
    severity = state.get("severity", "Medium")

    prompt = f"""
    Summarize the following vulnerability or threat for an executive reader (100–150 words). 
    Base the summary on threat description and its classification.
    Focus on impact, affected systems, and mitigation steps.
    Output structured JSON according to the required schema.    

    Threat Description:
    {description}

    Threat Type: {threat_type}
    Severity: {severity}

    The summary should include key details about the threat, its potential impact, and recommended actions for mitigation. Limit the summary to 590 characters.
    """

    response = llm_with_system_prompt.invoke({"input": prompt})

    # Safely extract text from the LLM response. Different LangChain/LLM
    # runnables can return different shapes (dict, AIMessage-like object,
    # a result with .content, or a generations structure). Try several
    # common access patterns and fall back to str(response).
    summary_text = ""
    if isinstance(response, dict):
        summary_text = response.get("output") or response.get("text") or response.get("content", "")
    elif hasattr(response, "content"):
        # Common for Chat/AI message wrappers
        summary_text = getattr(response, "content") or ""
    elif hasattr(response, "message"):
        # Some wrappers expose a message object
        msg = getattr(response, "message")
        summary_text = getattr(msg, "content", "") if msg is not None else ""
    elif hasattr(response, "generations"):
        # LangChain-style generations: could be list[list[Generation]] or list[Generation]
        gens = getattr(response, "generations")
        try:
            first = gens[0]
            # handle nested list
            if isinstance(first, list) and first:
                first = first[0]
            if hasattr(first, "text"):
                summary_text = first.text or ""
            else:
                summary_text = str(first)
        except Exception:
            summary_text = ""
    else:
        # Last resort
        try:
            summary_text = str(response)
        except Exception:
            summary_text = ""

    affected_products = []
    for product in ["Windows", "Linux", "Apache", "Exchange", "VPN", "Cisco", "Fortinet"]:
        if product.lower() in description.lower():
            affected_products.append(product)

    recommended_action = (
        "Review vendor advisories, apply patches as soon as possible, "
        "and monitor systems for related indicators of compromise."
    )

    m = re.search(r"CVE-\d{4}-\d+", description)
    cve_id = m.group(0) if m else None

    state.update(
        {
            "summary": summary_text[:590],
            "affected_products": affected_products,
            "recommended_action": recommended_action,
            "cve_id": cve_id,
        }
    )
    return state