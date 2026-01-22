# Architecture

This project follows a clean, layered architecture designed for clarity, scalability and enterprise readiness.

## High-level architecture

Frontend (Dashboard)
→ REST API (FastAPI)
→ Risk Engine (Scoring + Behavioral Detection)
→ Persistence Layer (SQLite via SQLAlchemy)

## Components

### API Layer (FastAPI)
- Receives events via REST endpoints
- Exposes risk and analytics endpoints
- Stateless and local-first

Key modules:
- `routes/events.py`
- `routes/risk.py`
- `routes/health.py`

### Risk Engine
Located in `app/core/`

Responsibilities:
- Rule-based risk scoring
- Behavioral detection (temporal patterns, burst activity)
- Explainable output (reasons per score)

Main modules:
- `scoring.py`
- `detection.py`

### Persistence Layer
Located in `app/data/`

Responsibilities:
- SQLite database
- ORM models
- CRUD operations
- Decoupled from API logic

Main modules:
- `database.py`
- `models.py`
- `crud.py`

### Execution & Ops
Located in `ops/run/`

Responsibilities:
- Local development execution
- Environment setup
- Dependency installation

## Design principles
- Local-first (no paid APIs, no external services)
- Explainable risk (no black-box ML in MVP)
- Enterprise-oriented structure
- Easy upgrade path to ML-based detection

## Future extensions
- ML anomaly detection
- Risk normalization (Low / Medium / High)
- Historical baselines per user
- Report export (PDF / JSON)
- Authentication & RBAC
