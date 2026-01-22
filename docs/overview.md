# Overview

AI Risk Scanner is a local-first security analytics project that ingests user activity events and computes explainable risk scores.

## Key capabilities (MVP)
- Event ingestion via REST API (`POST /events`)
- Persistent storage (SQLite)
- Explainable risk scoring (rules + behavioral detection)
- Risk endpoints for dashboards:
  - `GET /risk/summary`
  - `GET /risk/users`
  - `GET /risk/events`

## How to run (Windows)
1. Open PowerShell
2. Run: `.\ops\run\run_dev.ps1`
3. API will be available at:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - Health: `http://127.0.0.1:8000/health`

## Test quickly (Swagger)
1. Open `http://127.0.0.1:8000/docs`
2. Call `POST /events` 5–10 times with different users
3. Check `GET /risk/summary` and `GET /risk/users`
