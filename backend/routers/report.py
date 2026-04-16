"""backend/routers/report.py — POST /report (async PDF + email + lead store)"""
from __future__ import annotations

import asyncio
import logging
import os
import uuid
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr

from services.scorer import score_assessment
from services.pdf_generator import generate_pdf
from services.lead_store import store_lead
from services.email_sender import send_report_email

logger = logging.getLogger(__name__)
router = APIRouter()

_GCP_BUCKET = os.getenv("GCP_BUCKET_NAME", "sr117-reports")
_GCP_PROJECT = os.getenv("GCP_PROJECT_ID", "")


def _upload_to_gcs(pdf_bytes: bytes, filename: str) -> str:
    """Upload PDF to GCS and return public URL (or signed URL)."""
    try:
        from google.cloud import storage  # type: ignore
        client = storage.Client(project=_GCP_PROJECT)
        bucket = client.bucket(_GCP_BUCKET)
        blob = bucket.blob(filename)
        blob.upload_from_string(pdf_bytes, content_type="application/pdf")
        return f"https://storage.googleapis.com/{_GCP_BUCKET}/{filename}"
    except Exception as exc:
        logger.warning("GCS upload failed: %s", exc)
        return f"local://{filename}"


def _process_report(
    institution_name: str,
    email: str,
    asset_size_bucket: str,
    primary_role: str,
    answers: dict[str, str],
) -> None:
    """Background task: score → PDF → GCS → lead store → email."""
    try:
        score = score_assessment(institution_name, email, asset_size_bucket, primary_role, answers)
        pdf_bytes = generate_pdf(score)

        report_id = str(uuid.uuid4())
        filename = f"{report_id}_{institution_name.replace(' ', '_')}.pdf"
        report_url = _upload_to_gcs(pdf_bytes, filename)

        store_lead(score, report_url)
        send_report_email(score, pdf_bytes)
        logger.info("Report pipeline complete for %s", email)
    except Exception:
        logger.exception("Report pipeline failed for %s", email)


class ReportRequest(BaseModel):
    institution_name: str
    email: EmailStr
    asset_size_bucket: str
    primary_role: str
    answers: dict[str, str]


class ReportResponse(BaseModel):
    status: str
    message: str


@router.post("/report", response_model=ReportResponse)
async def create_report(req: ReportRequest, background_tasks: BackgroundTasks) -> Any:
    """
    Trigger async PDF generation, lead storage, and email delivery.
    Returns immediately — non-blocking on the frontend.
    """
    background_tasks.add_task(
        _process_report,
        institution_name=req.institution_name,
        email=req.email,
        asset_size_bucket=req.asset_size_bucket,
        primary_role=req.primary_role,
        answers=req.answers,
    )
    return ReportResponse(
        status="accepted",
        message=f"Your SR 11-7 Gap Report is being generated and will be emailed to {req.email} within 30 seconds.",
    )
