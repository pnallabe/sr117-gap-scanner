"""
backend/services/scorer.py
==========================
SR 11-7 domain scoring engine.

The 12 SR 11-7 control domains, each with 3 questions (0/1.5/3 points each).
Adapted and extended from credit-risk-platform/compliance/health_score.py
and compliance/exam_packet_builder.py.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal


# ---------------------------------------------------------------------------
# Domain definitions
# ---------------------------------------------------------------------------

DOMAIN_WEIGHTS: dict[str, float] = {
    "model_inventory": 1.0,
    "model_development_docs": 1.0,
    "validation_independence": 1.3,
    "conceptual_soundness": 1.0,
    "ongoing_monitoring": 1.3,
    "change_management": 1.0,
    "outcomes_analysis": 1.0,
    "use_policy_governance": 1.0,
    "third_party_oversight": 1.0,
    "data_quality_governance": 1.0,
    "fair_lending_controls": 1.3,
    "board_oversight": 1.0,
}

DOMAIN_NAMES: dict[str, str] = {
    "model_inventory": "Model Inventory & Classification",
    "model_development_docs": "Model Development Documentation",
    "validation_independence": "Model Validation Independence",
    "conceptual_soundness": "Conceptual Soundness Review",
    "ongoing_monitoring": "Ongoing Monitoring & Performance Tracking",
    "change_management": "Model Change Management",
    "outcomes_analysis": "Outcomes Analysis & Back-testing",
    "use_policy_governance": "Model Use Policy & Governance",
    "third_party_oversight": "Third-Party / Vendor Model Oversight",
    "data_quality_governance": "Data Quality & Data Governance",
    "fair_lending_controls": "Fair Lending / Disparate Impact Controls",
    "board_oversight": "Board & Senior Management Oversight",
}

# Questions per domain — order matches frontend
DOMAIN_QUESTION_IDS: dict[str, list[str]] = {
    "model_inventory": ["mi_1", "mi_2", "mi_3"],
    "model_development_docs": ["mdd_1", "mdd_2", "mdd_3"],
    "validation_independence": ["vi_1", "vi_2", "vi_3"],
    "conceptual_soundness": ["cs_1", "cs_2", "cs_3"],
    "ongoing_monitoring": ["om_1", "om_2", "om_3"],
    "change_management": ["cm_1", "cm_2", "cm_3"],
    "outcomes_analysis": ["oa_1", "oa_2", "oa_3"],
    "use_policy_governance": ["upg_1", "upg_2", "upg_3"],
    "third_party_oversight": ["tpo_1", "tpo_2", "tpo_3"],
    "data_quality_governance": ["dqg_1", "dqg_2", "dqg_3"],
    "fair_lending_controls": ["flc_1", "flc_2", "flc_3"],
    "board_oversight": ["bo_1", "bo_2", "bo_3"],
}

ANSWER_POINTS: dict[str, float] = {
    "yes": 3.0,
    "partial": 1.5,
    "no": 0.0,
}

REMEDIATION_BLURBS: dict[str, str] = {
    "model_inventory": (
        "An incomplete or unclassified model inventory is one of the first findings examiners document under SR 11-7 §4.1. "
        "Without a risk-tiered inventory, your institution cannot demonstrate proportionate oversight. "
        "ILOL's Model Governance Accelerator provides a pre-built inventory schema, risk-tier classification rubric, and attestation workflow that can be operationalized in 30 days."
    ),
    "model_development_docs": (
        "Incomplete or missing MDDs account for over 60% of SR 11-7 findings in recent OCC exam cycles. "
        "Without adequate documentation, models cannot be independently validated or audited. "
        "ILOL provides MDD templates aligned to SR 11-7 §4.2 and automated documentation completeness checks integrated into your SDLC."
    ),
    "validation_independence": (
        "Lack of validation independence is cited in over 70% of formal enforcement actions related to SR 11-7. "
        "Regulators require a demonstrable organizational separation between builders and validators. "
        "ILOL's Validation Independence Framework includes org design guidance, validation charter templates, and finding-to-remediation tracking workflows."
    ),
    "conceptual_soundness": (
        "Conceptual soundness reviews are frequently missing or superficial, particularly for vendor models where documentation is limited. "
        "Examiners are increasingly requiring conceptual challenges even for third-party models. "
        "ILOL provides a Conceptual Soundness Playbook with domain-specific challenge frameworks for credit scoring, fraud, and stress testing models."
    ),
    "ongoing_monitoring": (
        "Ongoing monitoring is one of the three most-cited gaps in 2025–2026 FDIC and OCC enforcement actions. "
        "Without automated performance tracking and escalation workflows, models can degrade undetected. "
        "ILOL's Monitoring Operations Center provides pre-built monitoring templates, alerting integrations, and breach escalation workflows."
    ),
    "change_management": (
        "Undocumented or un-revalidated model changes are a direct SR 11-7 violation and a common trigger for Matters Requiring Attention (MRAs). "
        "Without a formal change policy, any modification — including vendor updates — creates regulatory exposure. "
        "ILOL's Change Management Toolkit includes materiality assessment rubrics, re-validation triggers, and approval workflow templates."
    ),
    "outcomes_analysis": (
        "Outcomes analysis and back-testing remain underpracticed at most mid-market lenders, creating blind spots in model risk exposure. "
        "Without back-testing, deteriorating model performance goes undetected until losses accumulate. "
        "ILOL provides automated outcomes analysis pipelines and back-testing templates calibrated to your loss outcomes and credit model types."
    ),
    "use_policy_governance": (
        "An absent or outdated MRM policy is the foundational gap that prevents all other SR 11-7 controls from maturing. "
        "Examiners consider policy adequacy before evaluating any operational control. "
        "ILOL's Policy Accelerator includes a Board-ready MRM Policy template, risk appetite statement language, and governance charter for the Model Risk Committee."
    ),
    "third_party_oversight": (
        "'We rely on the vendor' is no longer an acceptable response — institutions are accountable for understanding and validating all models they use. "
        "Vendor model oversight is a rapidly escalating examiner focus area. "
        "ILOL's Vendor Model Governance Package includes due diligence templates, SR 11-7-aligned contract language, and ongoing monitoring protocols for third-party models."
    ),
    "data_quality_governance": (
        "Poor data quality is increasingly listed as a contributing factor in model risk findings. "
        "SR 11-7 requires institutions to demonstrate that model inputs are reliable and representative. "
        "ILOL's Data Quality Framework includes input data profiling, automated anomaly detection, and data governance controls aligned to SR 11-7 §5.3 and BCBS 239."
    ),
    "fair_lending_controls": (
        "Fair lending and disparate impact controls are the most enforcement-active SR 11-7 domain in 2025–2026, "
        "with joint CFPB/DOJ actions referencing model governance failures. "
        "ILOL's Fair Lending Assurance Suite provides pre-built disparate impact testing, proxy detection, and examiner-ready AIA documentation."
    ),
    "board_oversight": (
        "Board-level model risk oversight is the governance capstone of SR 11-7 §6.0. "
        "Examiners now routinely interview Board members on model risk awareness and expect documented reporting cadence. "
        "ILOL provides Board reporting templates, MRC charter language, and executive briefing materials that translate technical model risk into Board-appropriate governance language."
    ),
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class DomainScore:
    slug: str
    name: str
    raw_score: float        # 0–9
    max_raw: float          # 9.0
    pct: float              # 0–100
    band: Literal["RED", "AMBER", "GREEN"]
    weight: float
    remediation_blurb: str


@dataclass
class SR117Score:
    institution_name: str
    email: str
    asset_size_bucket: str   # "<$500M" | "$500M–$2B" | "$2B–$10B"
    primary_role: str
    domain_scores: dict[str, DomainScore]
    overall_score: float
    overall_band: Literal["RED", "AMBER", "GREEN"]
    top_3_gaps: list[str]
    exam_readiness_statement: str
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Scoring logic
# ---------------------------------------------------------------------------

def _get_band(pct: float) -> Literal["RED", "AMBER", "GREEN"]:
    if pct < 40:
        return "RED"
    if pct < 70:
        return "AMBER"
    return "GREEN"


def _overall_band(score: float) -> Literal["RED", "AMBER", "GREEN"]:
    if score < 50:
        return "RED"
    if score < 75:
        return "AMBER"
    return "GREEN"


def _exam_readiness_statement(band: str, top_gaps: list[str], institution: str) -> str:
    gap_names = [DOMAIN_NAMES.get(g, g) for g in top_gaps[:2]]
    gaps_str = " and ".join(gap_names)
    if band == "RED":
        return (
            f"{institution} has critical SR 11-7 control gaps — particularly in {gaps_str} — "
            "that present material regulatory exposure requiring immediate remediation before your next exam cycle."
        )
    if band == "AMBER":
        return (
            f"{institution} has moderate SR 11-7 gaps in {gaps_str} that would likely generate "
            "Matters Requiring Attention (MRAs) in an OCC or FDIC model risk examination."
        )
    return (
        f"{institution} demonstrates a largely mature SR 11-7 program; "
        f"targeted improvements in {gaps_str} would bring you to full examiner-ready status."
    )


def score_assessment(
    institution_name: str,
    email: str,
    asset_size_bucket: str,
    primary_role: str,
    answers: dict[str, str],  # question_id -> "yes" | "partial" | "no"
) -> SR117Score:
    """
    Core scoring function. Accepts raw question answers and returns a full SR117Score.
    Adapted from compliance/health_score.py weighted scoring pattern.
    """
    domain_scores: dict[str, DomainScore] = {}
    weighted_sum = 0.0
    max_weighted = 0.0

    for slug, q_ids in DOMAIN_QUESTION_IDS.items():
        weight = DOMAIN_WEIGHTS[slug]
        raw = sum(ANSWER_POINTS.get(answers.get(qid, "no"), 0.0) for qid in q_ids)
        max_raw = float(len(q_ids) * 3)
        pct = (raw / max_raw) * 100.0

        weighted_sum += (raw / max_raw) * 3.0 * weight
        max_weighted += 3.0 * weight

        domain_scores[slug] = DomainScore(
            slug=slug,
            name=DOMAIN_NAMES[slug],
            raw_score=raw,
            max_raw=max_raw,
            pct=round(pct, 1),
            band=_get_band(pct),
            weight=weight,
            remediation_blurb=REMEDIATION_BLURBS[slug],
        )

    overall = (weighted_sum / max_weighted) * 100.0
    band = _overall_band(overall)
    top_3 = sorted(domain_scores.keys(), key=lambda s: domain_scores[s].pct)[:3]
    statement = _exam_readiness_statement(band, top_3, institution_name)

    return SR117Score(
        institution_name=institution_name,
        email=email,
        asset_size_bucket=asset_size_bucket,
        primary_role=primary_role,
        domain_scores=domain_scores,
        overall_score=round(overall, 1),
        overall_band=band,
        top_3_gaps=top_3,
        exam_readiness_statement=statement,
    )
