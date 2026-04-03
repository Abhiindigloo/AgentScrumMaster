# AgentScrumMaster

AI-powered Scrum facilitation agent built with FastAPI and Python 3.11.

## Phase 1 — Project Skeleton

This phase sets up the clean project foundation: FastAPI app, centralized config, structured logging, and base exception handling. No business logic yet.

## Project Structure

```
agentic_scrum_master/
├── app/
│   ├── main.py                 # FastAPI application factory + health endpoint
│   ├── core/
│   │   ├── config.py           # Centralized settings (pydantic-settings)
│   │   ├── logging_config.py   # Structured JSON/plain logging
│   │   └── exceptions.py       # Base exception hierarchy
│   ├── agents/                 # Agent implementations (future)
│   ├── services/               # Business logic layer (future)
│   ├── schemas/                # Pydantic request/response models (future)
│   ├── api/
│   │   └── routes/             # API route modules (future)
│   ├── models/                 # Domain entities (future)
│   ├── repositories/           # Data access layer (future)
│   └── utils/                  # Shared utilities (future)
├── tests/                      # Test suite (future)
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
└── README.md
```

## Setup

```bash
cd agentic_scrum_master
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Verify

```bash
curl http://localhost:8000/api/healthz
# {"status":"ok","app":"AgentScrumMaster","version":"0.1.0"}
```

## API Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
