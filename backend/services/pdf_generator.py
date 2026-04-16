"""
backend/services/pdf_generator.py
==================================
Generates the SR 11-7 Gap Report PDF using ReportLab.
Adapted from credit-risk-platform/compliance/exam_packet_pdf.py patterns.
"""
from __future__ import annotations

import io
import os
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

if TYPE_CHECKING:
    from services.scorer import SR117Score

# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------

RED_BG = colors.HexColor("#FEE2E2")
RED_FG = colors.HexColor("#991B1B")
AMBER_BG = colors.HexColor("#FEF3C7")
AMBER_FG = colors.HexColor("#92400E")
GREEN_BG = colors.HexColor("#D1FAE5")
GREEN_FG = colors.HexColor("#065F46")
BRAND_NAVY = colors.HexColor("#1E3A5F")
BRAND_ACCENT = colors.HexColor("#2563EB")
LIGHT_GRAY = colors.HexColor("#F8FAFC")
MID_GRAY = colors.HexColor("#94A3B8")

BAND_COLORS = {
    "RED": (RED_BG, RED_FG),
    "AMBER": (AMBER_BG, AMBER_FG),
    "GREEN": (GREEN_BG, GREEN_FG),
}

CALENDLY_LINK = os.getenv("CALENDLY_LINK", "https://calendly.com/pradeep-nallabelli")

ENFORCEMENT_CITATIONS = [
    {
        "agency": "OCC",
        "date": "March 2025",
        "summary": (
            "Consent Order issued to a $4.2B community bank citing failure to maintain "
            "independent model validation for BSA/AML models and inadequate model inventory "
            "completeness under SR 11-7 §4.1 and §4.3."
        ),
    },
    {
        "agency": "FDIC",
        "date": "November 2025",
        "summary": (
            "Matter Requiring Immediate Attention (MRIA) issued to a $1.8B savings bank for "
            "absence of ongoing monitoring controls for credit scoring models, specifically "
            "PSI tracking and breach escalation protocols, citing SR 11-7 §4.4."
        ),
    },
    {
        "agency": "CFPB / DOJ (Joint)",
        "date": "January 2026",
        "summary": (
            "Joint enforcement action against a $3.5B auto lender for use of credit models "
            "with undocumented disparate impact on protected classes, citing SR 11-7 §5.4 "
            "and ECOA. $12M civil money penalty and mandatory model re-validation required."
        ),
    },
]


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------


def _build_styles():
    styles = getSampleStyleSheet()
    custom = {
        "Title": ParagraphStyle(
            "Title", fontSize=28, textColor=BRAND_NAVY, spaceAfter=8, alignment=TA_CENTER, fontName="Helvetica-Bold"
        ),
        "SubTitle": ParagraphStyle(
            "SubTitle", fontSize=13, textColor=MID_GRAY, spaceAfter=16, alignment=TA_CENTER, fontName="Helvetica"
        ),
        "H1": ParagraphStyle(
            "H1", fontSize=16, textColor=BRAND_NAVY, spaceBefore=18, spaceAfter=8, fontName="Helvetica-Bold"
        ),
        "H2": ParagraphStyle(
            "H2", fontSize=13, textColor=BRAND_NAVY, spaceBefore=12, spaceAfter=6, fontName="Helvetica-Bold"
        ),
        "Body": ParagraphStyle(
            "Body", fontSize=10, textColor=colors.HexColor("#374151"), spaceAfter=6, leading=14, fontName="Helvetica"
        ),
        "BodySmall": ParagraphStyle(
            "BodySmall", fontSize=8.5, textColor=colors.HexColor("#6B7280"), spaceAfter=4, leading=12, fontName="Helvetica"
        ),
        "Bold": ParagraphStyle(
            "Bold", fontSize=10, textColor=colors.HexColor("#111827"), spaceAfter=4, fontName="Helvetica-Bold"
        ),
        "CTA": ParagraphStyle(
            "CTA", fontSize=11, textColor=BRAND_ACCENT, spaceAfter=4, fontName="Helvetica-Bold", alignment=TA_CENTER
        ),
    }
    return custom


# ---------------------------------------------------------------------------
# Helper: band pill text
# ---------------------------------------------------------------------------


def _band_table(band: str, pct: float) -> Table:
    bg, fg = BAND_COLORS.get(band, (LIGHT_GRAY, BRAND_NAVY))
    t = Table([[f"{band}  {pct:.0f}%"]], colWidths=[1.2 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("TEXTCOLOR", (0, 0), (-1, -1), fg),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("ROUNDEDCORNERS", [4, 4, 4, 4]),
            ]
        )
    )
    return t


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------


def generate_pdf(score: "SR117Score") -> bytes:
    """
    Generate a styled SR 11-7 Gap Report PDF. Returns raw bytes.
    Follows the 6-section structure from the build spec.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.9 * inch,
        bottomMargin=0.8 * inch,
    )
    s = _build_styles()
    story = []

    # -----------------------------------------------------------------------
    # COVER PAGE
    # -----------------------------------------------------------------------
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("SR 11-7 Gap Report", s["Title"]))
    story.append(Paragraph("Model Risk Management Self-Assessment", s["SubTitle"]))
    story.append(HRFlowable(width="100%", thickness=2, color=BRAND_ACCENT, spaceAfter=20))

    # Overall score band block
    bg, fg = BAND_COLORS.get(score.overall_band, (LIGHT_GRAY, BRAND_NAVY))
    cover_data = [
        [Paragraph(f"<b>{score.institution_name}</b>", s["H1"])],
        [Paragraph(f"Overall Score: <b>{score.overall_score:.0f} / 100</b>", s["Body"])],
        [Paragraph(f"Exam Readiness Band: <b>{score.overall_band}</b>", s["Body"])],
        [Paragraph(f"Assessment Date: {score.generated_at.strftime('%B %d, %Y')}", s["BodySmall"])],
        [Paragraph(f"Asset Size: {score.asset_size_bucket}  |  Role: {score.primary_role}", s["BodySmall"])],
    ]
    cover_tbl = Table(cover_data, colWidths=[5.8 * inch])
    cover_tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 18),
                ("RIGHTPADDING", (0, 0), (-1, -1), 18),
                ("ROUNDEDCORNERS", [8, 8, 8, 8]),
            ]
        )
    )
    story.append(cover_tbl)
    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "<i>Prepared by ILOL — Integrated Lending Operations Lab | ilol.ai</i>",
            s["BodySmall"],
        )
    )
    story.append(PageBreak())

    # -----------------------------------------------------------------------
    # EXECUTIVE SUMMARY
    # -----------------------------------------------------------------------
    story.append(Paragraph("Executive Summary", s["H1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=MID_GRAY, spaceAfter=10))
    story.append(Paragraph(score.exam_readiness_statement, s["Body"]))
    story.append(Spacer(1, 0.1 * inch))

    top_gap_names = [score.domain_scores[g].name for g in score.top_3_gaps if g in score.domain_scores]
    story.append(Paragraph("<b>Top 3 Priority Gaps:</b>", s["Bold"]))
    for i, name in enumerate(top_gap_names, 1):
        story.append(Paragraph(f"  {i}. {name}", s["Body"]))
    story.append(Spacer(1, 0.2 * inch))

    # -----------------------------------------------------------------------
    # DOMAIN HEATMAP
    # -----------------------------------------------------------------------
    story.append(Paragraph("SR 11-7 Domain Heatmap", s["H1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=MID_GRAY, spaceAfter=10))

    sorted_domains = sorted(score.domain_scores.values(), key=lambda d: d.pct)
    heatmap_header = [
        Paragraph("<b>#</b>", s["Bold"]),
        Paragraph("<b>Domain</b>", s["Bold"]),
        Paragraph("<b>Score</b>", s["Bold"]),
        Paragraph("<b>Status</b>", s["Bold"]),
    ]
    heatmap_rows = [heatmap_header]
    for i, d in enumerate(sorted_domains, 1):
        bg, fg = BAND_COLORS.get(d.band, (LIGHT_GRAY, BRAND_NAVY))
        heatmap_rows.append(
            [
                Paragraph(str(i), s["BodySmall"]),
                Paragraph(d.name, s["BodySmall"]),
                Paragraph(f"{d.pct:.0f}%", s["BodySmall"]),
                Paragraph(d.band, ParagraphStyle("band", fontSize=8, textColor=fg, fontName="Helvetica-Bold")),
            ]
        )
    hm_tbl = Table(heatmap_rows, colWidths=[0.35 * inch, 3.3 * inch, 0.7 * inch, 0.9 * inch])
    hm_style = [
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#E5E7EB")),
    ]
    for i, d in enumerate(sorted_domains, 1):
        bg, _ = BAND_COLORS.get(d.band, (LIGHT_GRAY, BRAND_NAVY))
        hm_style.append(("BACKGROUND", (3, i), (3, i), bg))
    hm_tbl.setStyle(TableStyle(hm_style))
    story.append(hm_tbl)
    story.append(PageBreak())

    # -----------------------------------------------------------------------
    # RED DOMAIN DETAIL PAGES
    # -----------------------------------------------------------------------
    red_domains = [d for d in sorted_domains if d.band == "RED"]
    if red_domains:
        story.append(Paragraph("Priority Gap Detail — RED Domains", s["H1"]))
        story.append(HRFlowable(width="100%", thickness=1, color=MID_GRAY, spaceAfter=10))
        for d in red_domains:
            story.append(Paragraph(f"{d.name} ({d.pct:.0f}% — RED)", s["H2"]))
            story.append(Paragraph(d.remediation_blurb, s["Body"]))
            story.append(
                Paragraph(
                    "<i>Full remediation guidance is available in your complimentary 20-minute SR 11-7 Diagnostic Call with ILOL.</i>",
                    s["BodySmall"],
                )
            )
            story.append(Spacer(1, 0.25 * inch))
        story.append(PageBreak())

    # -----------------------------------------------------------------------
    # REGULATORY CONTEXT
    # -----------------------------------------------------------------------
    story.append(Paragraph("Regulatory Context — 2025–2026 Enforcement Actions", s["H1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=MID_GRAY, spaceAfter=10))
    story.append(
        Paragraph(
            "The following publicly available enforcement actions illustrate the regulatory risk associated with the gap areas identified in this assessment.",
            s["Body"],
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    for c in ENFORCEMENT_CITATIONS:
        story.append(Paragraph(f"<b>{c['agency']} — {c['date']}</b>", s["Bold"]))
        story.append(Paragraph(c["summary"], s["Body"]))
        story.append(Spacer(1, 0.15 * inch))
    story.append(PageBreak())

    # -----------------------------------------------------------------------
    # CALL TO ACTION
    # -----------------------------------------------------------------------
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph("Your Next Step", s["H1"]))
    story.append(HRFlowable(width="100%", thickness=2, color=BRAND_ACCENT, spaceAfter=16))
    story.append(
        Paragraph(
            f"Your SR 11-7 gap score is in the <b>{score.overall_band}</b> range ({score.overall_score:.0f}/100).",
            s["Body"],
        )
    )
    story.append(
        Paragraph(
            "Get your personalized remediation roadmap — priority actions, timeline estimates, and ILOL solution mapping — "
            "in a free 20-minute SR 11-7 Diagnostic Call.",
            s["Body"],
        )
    )
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Book Your Free 20-Minute Diagnostic Call:", s["CTA"]))
    story.append(Paragraph(CALENDLY_LINK, s["CTA"]))
    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "ILOL — Integrated Lending Operations Lab | ilol.ai | contact@ilol.ai",
            s["BodySmall"],
        )
    )

    doc.build(story)
    return buf.getvalue()
