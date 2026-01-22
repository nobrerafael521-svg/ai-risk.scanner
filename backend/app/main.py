from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.health import router as health_router
from app.routes.envents import router as events_router
from app.routes.risk import router as risk_router

from app.data import init_db


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Risk Scanner API",
        version="1.0.0",
        description="Local-first API to ingest events and compute risk scores.",
    )

    # CORS (frontend on 5500 -> backend on 8000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5500",
            "http://localhost:5500",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Init DB tables
    init_db()

    # Routes
    app.include_router(health_router, tags=["Health"])
    app.include_router(events_router, prefix="/events", tags=["Events"])
    app.include_router(risk_router, prefix="/risk", tags=["Risk"])

    return app


app = create_app()
