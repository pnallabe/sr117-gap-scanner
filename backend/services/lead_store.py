"""
backend/services/lead_store.py
================================
Stores lead data to Supabase (postgres) or falls back to a local JSON file for dev.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from services.scorer import SR117Score

_SUPABASE_URL = os.getenv("SUPABASE_URL", "")
_SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
_LOCAL_STORE = Path(__file__).parent.parent / "data" / "leads.json"


def _supabase_available() -> bool:
    return bool(_SUPABASE_URL and _SUPABASE_KEY)


def _save_local(payload: dict[str, Any]) -> None:
    _LOCAL_STORE.parent.mkdir(parents=True, exist_ok=True)
    leads: list = []
    if _LOCAL_STORE.exists():
        try:
            leads = json.loads(_LOCAL_STORE.read_text())
        except Exception:
            leads = []
    leads.append(payload)
    _LOCAL_STORE.write_text(json.dumps(leads, indent=2, default=str))
    logger.info("Lead saved locally → %s", _LOCAL_STORE)


def store_lead(score: "SR117Score", report_url: str) -> None:
    """Persist the lead to Supabase or local fallback."""
    payload: dict[str, Any] = {
        "email": score.email,
        "institution": score.institution_name,
        "asset_size": score.asset_size_bucket,
        "primary_role": score.primary_role,
        "overall_score": score.overall_score,
        "overall_band": score.overall_band,
        "top_3_gaps": score.top_3_gaps,
        "domain_scores_json": {
            slug: {
                "pct": ds.pct,
                "band": ds.band,
                "raw": ds.raw_score,
            }
            for slug, ds in score.domain_scores.items()
        },
        "report_url": report_url,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }

    if _supabase_available():
        try:
            from supabase import create_client  # type: ignore
            client = create_client(_SUPABASE_URL, _SUPABASE_KEY)
            client.table("gap_scanner_leads").insert(payload).execute()
            logger.info("Lead stored in Supabase for %s", score.email)
            return
        except Exception as exc:
            logger.warning("Supabase write failed, falling back to local: %s", exc)

    _save_local(payload)
