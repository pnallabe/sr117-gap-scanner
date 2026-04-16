"""
backend/services/email_sender.py
==================================
Sends the scored PDF report via Resend (primary) or SendGrid (fallback).
"""
from __future__ import annotations

import base64
import logging
import os
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from services.scorer import SR117Score

_RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
_SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
_FROM_EMAIL = os.getenv("FROM_EMAIL", "reports@ilol.ai")
_CALENDLY_LINK = os.getenv("CALENDLY_LINK", "https://calendly.com/ilol/sr-117-diagnostic")


def _send_via_resend(to: str, subject: str, html: str, pdf_bytes: bytes, filename: str) -> None:
    import resend  # type: ignore
    resend.api_key = _RESEND_API_KEY
    resend.Emails.send(
        {
            "from": _FROM_EMAIL,
            "to": [to],
            "subject": subject,
            "html": html,
            "attachments": [
                {
                    "filename": filename,
                    "content": list(pdf_bytes),
                }
            ],
        }
    )
    logger.info("Email sent via Resend to %s", to)


def _send_via_sendgrid(to: str, subject: str, html: str, pdf_bytes: bytes, filename: str) -> None:
    from sendgrid import SendGridAPIClient  # type: ignore
    from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition  # type: ignore

    message = Mail(
        from_email=_FROM_EMAIL,
        to_emails=to,
        subject=subject,
        html_content=html,
    )
    encoded = base64.b64encode(pdf_bytes).decode()
    attachment = Attachment(
        FileContent(encoded),
        FileName(filename),
        FileType("application/pdf"),
        Disposition("attachment"),
    )
    message.attachment = attachment
    sg = SendGridAPIClient(_SENDGRID_API_KEY)
    sg.send(message)
    logger.info("Email sent via SendGrid to %s", to)


def send_report_email(score: "SR117Score", pdf_bytes: bytes) -> None:
    """Send the PDF report to the lead's email address."""
    subject = f"Your SR 11-7 Gap Report — {score.institution_name}"
    filename = f"SR117_Gap_Report_{score.institution_name.replace(' ', '_')}.pdf"

    band_color = {"RED": "#EF4444", "AMBER": "#F59E0B", "GREEN": "#10B981"}.get(score.overall_band, "#6B7280")

    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <div style="background: #1E3A5F; padding: 24px; border-radius: 8px 8px 0 0;">
        <h1 style="color: white; margin: 0; font-size: 20px;">SR 11-7 Gap Report</h1>
        <p style="color: #94A3B8; margin: 4px 0 0;">Integrated Lending Operations Lab</p>
      </div>
      <div style="padding: 24px; background: #F8FAFC; border: 1px solid #E5E7EB;">
        <p style="font-size: 16px; color: #111827;">Hi {score.institution_name} team,</p>
        <p style="color: #374151;">Your SR 11-7 Model Risk self-assessment has been scored. Here are your results:</p>
        
        <div style="background: white; border-left: 4px solid {band_color}; padding: 16px; margin: 16px 0; border-radius: 4px;">
          <p style="font-size: 22px; font-weight: bold; color: {band_color}; margin: 0;">{score.overall_score:.0f} / 100 — {score.overall_band}</p>
          <p style="color: #6B7280; margin: 4px 0 0; font-size: 13px;">{score.exam_readiness_statement}</p>
        </div>
        
        <p style="color: #374151;"><strong>Top 3 priority gaps:</strong></p>
        <ol style="color: #374151;">
          {''.join(f'<li>{score.domain_scores[g].name}</li>' for g in score.top_3_gaps if g in score.domain_scores)}
        </ol>
        
        <p style="color: #374151;">Your full scored report is attached as a PDF.</p>
        
        <div style="background: #EFF6FF; border: 1px solid #BFDBFE; padding: 16px; border-radius: 8px; margin: 20px 0; text-align: center;">
          <p style="font-weight: bold; color: #1E40AF; margin: 0 0 8px;">Get your personalized remediation roadmap</p>
          <p style="color: #374151; font-size: 13px; margin: 0 0 12px;">Book a free 20-minute SR 11-7 Diagnostic Call with an ILOL model risk advisor.</p>
          <a href="{_CALENDLY_LINK}" style="background: #2563EB; color: white; padding: 10px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">Book My Free Diagnostic Call →</a>
        </div>
        
        <p style="color: #9CA3AF; font-size: 12px; margin-top: 24px;">ILOL — Integrated Lending Operations Lab | ilol.ai</p>
      </div>
    </div>
    """

    if _RESEND_API_KEY:
        _send_via_resend(score.email, subject, html, pdf_bytes, filename)
    elif _SENDGRID_API_KEY:
        _send_via_sendgrid(score.email, subject, html, pdf_bytes, filename)
    else:
        logger.warning("No email provider configured. Skipping email send for %s", score.email)
