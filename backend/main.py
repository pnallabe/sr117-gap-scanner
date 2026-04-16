"""
backend/main.py
===============
SR 11-7 Gap Scanner — FastAPI application entry point.
"""
from __future__ import annotations

import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.assessment import router as assessment_router
from routers.report import router as report_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")

app = FastAPI(
    title="SR 11-7 Gap Scanner API",
    description="Backend for the SR 11-7 Model Risk Management self-assessment tool.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow Vercel frontend origin
_ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,https://scanner.ilol.ai",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assessment_router, prefix="/api/v1", tags=["Assessment"])
app.include_router(report_router, prefix="/api/v1", tags=["Report"])


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "sr117-gap-scanner-api"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
