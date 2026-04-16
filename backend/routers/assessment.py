"""backend/routers/assessment.py — POST /assess"""
from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, field_validator

from services.scorer import score_assessment

logger = logging.getLogger(__name__)
router = APIRouter()


class AssessmentRequest(BaseModel):
    institution_name: str
    email: EmailStr
    asset_size_bucket: str
    primary_role: str
    answers: dict[str, str]  # question_id -> "yes" | "partial" | "no"

    @field_validator("asset_size_bucket")
    @classmethod
    def validate_bucket(cls, v: str) -> str:
        valid = {"<$500M", "$500M–$2B", "$2B–$10B"}
        if v not in valid:
            raise ValueError(f"asset_size_bucket must be one of {valid}")
        return v

    @field_validator("answers")
    @classmethod
    def validate_answers(cls, v: dict[str, str]) -> dict[str, str]:
        valid_values = {"yes", "partial", "no"}
        for k, val in v.items():
            if val not in valid_values:
                raise ValueError(f"Answer for '{k}' must be yes/partial/no, got '{val}'")
        return v


class DomainScoreOut(BaseModel):
    slug: str
    name: str
    pct: float
    band: str
    weight: float


class AssessmentResponse(BaseModel):
    institution_name: str
    email: str
    overall_score: float
    overall_band: str
    top_3_gaps: list[str]
    exam_readiness_statement: str
    domain_scores: list[DomainScoreOut]
    generated_at: str


@router.post("/assess", response_model=AssessmentResponse)
async def assess(req: AssessmentRequest) -> Any:
    """
    Score a submitted SR 11-7 assessment and return results.
    The PDF is generated asynchronously via /report.
    """
    try:
        result = score_assessment(
            institution_name=req.institution_name,
            email=req.email,
            asset_size_bucket=req.asset_size_bucket,
            primary_role=req.primary_role,
            answers=req.answers,
        )
    except Exception as exc:
        logger.exception("Scoring failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return AssessmentResponse(
        institution_name=result.institution_name,
        email=result.email,
        overall_score=result.overall_score,
        overall_band=result.overall_band,
        top_3_gaps=result.top_3_gaps,
        exam_readiness_statement=result.exam_readiness_statement,
        domain_scores=[
            DomainScoreOut(
                slug=ds.slug,
                name=ds.name,
                pct=ds.pct,
                band=ds.band,
                weight=ds.weight,
            )
            for ds in result.domain_scores.values()
        ],
        generated_at=result.generated_at.isoformat(),
    )
