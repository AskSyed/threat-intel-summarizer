from fastapi import FastAPI
from app.flows import build_threat_flow

app = FastAPI(title="Threat Intelligence Summarizer")

flow = build_threat_flow()
graph = flow.compile()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/run-threat-job")
async def run_threat_job():
    initial_state = {
        "sample_path": "app/sample_data/sample_feed.json",
        "current_index": 0,
    }
    final_state = await graph.ainvoke(initial_state)
    return {
        "db_ids": final_state.get("db_ids", []),
        "validation_errors": final_state.get("validation_errors", []),
        "threat_type": final_state.get("threat_type"),
        "severity": final_state.get("severity"),
        "title": final_state.get("title"),
        "summary": final_state.get("summary")
    }
