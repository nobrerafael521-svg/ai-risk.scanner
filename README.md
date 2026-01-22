# AI Risk Scanner 🔐

AI Risk Scanner is a **local-first security analytics platform** that ingests user activity events and computes **explainable risk scores** in real time.

The project is designed as an **enterprise-style MVP**, focusing on clarity, clean architecture and practical security use cases (SOC / internal monitoring).

---

## 🚀 Features

- Event ingestion via REST API (FastAPI)
- Persistent storage (SQLite)
- Explainable risk scoring (rule-based + behavioral detection)
- Detection of suspicious activity patterns
- Risk aggregation per user
- Interactive dashboard (KPIs, table, chart)
- Local-first (no paid APIs, no cloud dependency)

---

## 🧠 How it works (high level)

1. Systems send activity events (login attempts, file access, etc.)
2. Events are stored in a local database
3. A scoring engine assigns risk points based on:
   - Failed logins
   - Sensitive resource access
   - Abnormal burst activity
4. Risk is aggregated per user
5. Results are exposed via API and visualized in a dashboard

---

## 🏗️ Architecture

frontend/ → Dashboard (HTML, CSS, JS)
backend/
├─ app/
│ ├─ routes/ → API endpoints (events, risk, health)
│ ├─ core/ → Risk scoring & behavioral detection
│ ├─ data/ → Database, models, CRUD
│ └─ main.py → FastAPI app + CORS
└─ requirements.txt
ops/
└─ run/ → Dev scripts (backend + frontend)

yaml
Copiar código

Design principles:
- Clean separation of concerns
- Explainable logic (no black-box ML)
- Easy upgrade path to ML-based detection
- Enterprise-ready structure

---

## ▶️ How to run (Windows)

### 1️⃣ Start the backend
```powershell
.\ops\run\run_dev.ps1
Backend will be available at:

API docs: http://127.0.0.1:8000/docs

Health: http://127.0.0.1:8000/health

2️⃣ Start the frontend
Open a second terminal and run:

powershell
Copiar código
.\ops\run\run_frontend.ps1
Open in browser:

cpp
Copiar código
http://127.0.0.1:5500
🧪 Add demo data
Use Swagger (/docs) → POST /events

Example:

json
Copiar código
{
  "user_id": "user1",
  "event_type": "login_failed",
  "source_ip": "192.168.1.10",
  "success": false
}
Add multiple events to see:

KPIs update

Risk scores increase

Chart and table populate

📊 Dashboard
The dashboard provides:

Total events

Total users

High-risk users

Risk table with explanations

Top risk users chart

Designed to resemble a real security analytics product, not a demo page.

🔒 Use cases
Internal security monitoring

SOC training / demos

Behavioral risk analysis

Portfolio project for security / backend roles

🔮 Future improvements
ML-based anomaly detection

Risk levels (Low / Medium / High)

Authentication & RBAC

PDF / JSON risk reports

Time-series analytics

Real-time streaming ingestion