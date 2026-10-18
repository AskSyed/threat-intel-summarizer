import os

import httpx
import streamlit as st

DEFAULT_API_URL = os.getenv("API_URL", "http://localhost:8000")
HEALTH_TIMEOUT_SECONDS = 3.0
# The threat job calls the LLM for every feed item, so it can take a while.
RUN_TIMEOUT_SECONDS = 300.0

SEVERITY_BADGE_COLORS = {
    "low": "green",
    "medium": "orange",
    "high": "red",
    "critical": "red",
}


def check_backend(api_url: str) -> tuple[bool, str]:
    try:
        response = httpx.get(f"{api_url}/health", timeout=HEALTH_TIMEOUT_SECONDS)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        return False, str(exc)
    return True, "Backend is reachable"


def run_threat_job(api_url: str) -> dict:
    response = httpx.post(f"{api_url}/run-threat-job", timeout=RUN_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


def render_sidebar() -> tuple[str, bool]:
    with st.sidebar:
        st.header("Settings")
        api_url = st.text_input("Backend URL", value=DEFAULT_API_URL).rstrip("/")
        online, message = check_backend(api_url)
        if online:
            st.success("Backend online")
        else:
            st.error("Backend offline")
            st.caption(f"Start it with `uvicorn app.main:app --reload`.\n\n{message}")
    return api_url, online


def render_result(result: dict) -> None:
    st.subheader(result.get("title") or "Threat summary")

    severity = (result.get("severity") or "unknown").lower()
    col_type, col_severity, col_stored = st.columns(3)
    col_type.metric("Threat type", result.get("threat_type") or "—")
    col_severity.metric("Severity", severity.title())
    col_stored.metric("Stored records", len(result.get("db_ids") or []))
    st.badge(severity.upper(), color=SEVERITY_BADGE_COLORS.get(severity, "gray"))

    st.markdown("**Summary**")
    st.write(result.get("summary") or "_No summary returned._")

    errors = result.get("validation_errors") or []
    if errors:
        with st.expander(f"Validation errors ({len(errors)})", expanded=True):
            for error in errors:
                st.warning(error)
    else:
        st.caption("No validation errors.")

    with st.expander("Raw response"):
        st.json(result)


def main():
    st.set_page_config(
        page_title="Threat Intelligence Summarizer",
        page_icon="🛡️",
        layout="wide",
    )
    st.title("Threat Intelligence Summarizer")
    st.write(
        "Run the threat pipeline on the sample feed. Each item is fetched, "
        "classified, summarized, validated and stored by the backend."
    )

    api_url, online = render_sidebar()

    if st.button("Run threat job", type="primary", disabled=not online):
        with st.spinner("Running the threat pipeline. This can take a minute..."):
            try:
                result = run_threat_job(api_url)
            except httpx.HTTPStatusError as exc:
                st.error(f"Backend returned {exc.response.status_code}: {exc.response.text}")
            except httpx.HTTPError as exc:
                st.error(f"Could not reach the backend: {exc}")
            else:
                st.session_state["last_result"] = result

    if "last_result" in st.session_state:
        render_result(st.session_state["last_result"])


main()
