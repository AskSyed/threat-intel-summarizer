# Backend System Diagram

Diagrams are Mermaid; they render on GitHub and in the VS Code Markdown preview.

## 1. Component / deployment view

```mermaid
flowchart LR
    subgraph Client
        UI["Streamlit UI<br/>ui/streamlit-app/Home.py<br/>:8501"]
        CURL["curl / API client"]
    end

    subgraph API["FastAPI service (app/main.py) :8000"]
        HEALTH["GET /health"]
        RUN["POST /run-threat-job"]
        GRAPH["Compiled LangGraph<br/>(built once at import)"]
        RUN -->|"graph.ainvoke(initial_state)"| GRAPH
    end

    subgraph Config
        ENV[".env<br/>OPENAI_API_KEY, DATABASE_URL"]
        SETTINGS["pydantic-settings<br/>app/config/settings.py"]
        ENV --> SETTINGS
    end

    subgraph Sources["Data sources"]
        SAMPLE[("sample_feed.json<br/>(local file)")]
        REMOTE["Remote JSON feed<br/>(feed_url, via httpx)"]
    end

    LLM["OpenAI API<br/>gpt-4o, temperature 0"]
    DB[("Database<br/>STUB today: print + fake ID<br/>target: SQLAlchemy + SQL Server/Postgres")]

    UI -->|"HTTP"| HEALTH
    UI -->|"HTTP, 300s timeout"| RUN
    CURL --> RUN
    GRAPH --> SAMPLE
    GRAPH -.->|"if feed_url set"| REMOTE
    GRAPH -->|"classify + summarize"| LLM
    GRAPH -->|"persist_to_db"| DB
    SETTINGS --> GRAPH
```

## 2. LangGraph pipeline (the core of the backend)

```mermaid
flowchart TD
    S([START]) --> F["fetch_threat_feed<br/>async; HTTP or local JSON<br/>writes raw_feed"]
    F --> P["parse_and_normalize<br/>picks items[current_index]<br/>writes normalized_item, title, source, published_at"]
    P --> C["classify_threat<br/>LLM structured output<br/>(ThreatClassification)<br/>writes threat_type, severity"]
    C --> SU["summarize_threat<br/>LLM free text, cut to 590 chars<br/>+ regex CVE, keyword products,<br/>static recommended_action"]
    SU --> V["guardrails_validate<br/>Pydantic ThreatSummary<br/>+ no-URL rule<br/>writes validation_errors"]
    V --> R{{"validation_errors?"}}
    R -->|"empty: ok"| DBN["persist_to_db<br/>stub: print + fake T-timestamp ID<br/>appends to db_ids"]
    R -->|"non-empty: retry"| SU
    DBN --> E([END])
```

## 3. Request sequence

```mermaid
sequenceDiagram
    actor U as User
    participant UI as Streamlit
    participant API as FastAPI
    participant G as LangGraph
    participant L as OpenAI gpt-4o
    participant D as DB (stub)

    U->>UI: Click "Run threat job"
    UI->>API: GET /health (sidebar, every rerun)
    API-->>UI: {"status":"ok"}
    UI->>API: POST /run-threat-job
    API->>G: ainvoke({sample_path, current_index: 0})
    G->>G: fetch -> parse (item 0 only)
    G->>L: classify (structured output)
    L-->>G: threat_type, severity
    G->>L: summarize
    L-->>G: summary text
    G->>G: validate (Pydantic + no-URL)
    alt errors
        G->>L: summarize again (same prompt)
    else ok
        G->>D: persist (print + fake ID)
    end
    G-->>API: final state
    API-->>UI: {db_ids, validation_errors, threat_type, severity, title, summary}
    UI-->>U: metrics, summary, validation expander, raw JSON
```

## 4. Shared state (`ThreatState`, a TypedDict)

```mermaid
flowchart LR
    subgraph In["Input"]
        a1[feed_url]
        a2[sample_path]
        a3[current_index]
    end
    subgraph Mid["Produced by nodes"]
        b1[raw_feed]
        b2[normalized_item]
        b3[title / source / published_at]
        b4[threat_type / severity]
        b5[summary / affected_products / recommended_action / cve_id]
        b6[validation_errors]
        b7[db_ids]
    end
    In --> b1 --> b2 --> b3
    b2 --> b4 --> b5 --> b6 --> b7
```
