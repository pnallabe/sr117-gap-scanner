"""Tests for the SR 11-7 scoring engine."""
from __future__ import annotations

import pytest
from services.scorer import score_assessment, DOMAIN_QUESTION_IDS


def _all_yes_answers() -> dict[str, str]:
    answers: dict[str, str] = {}
    for q_ids in DOMAIN_QUESTION_IDS.values():
        for q in q_ids:
            answers[q] = "yes"
    return answers


def _all_no_answers() -> dict[str, str]:
    answers: dict[str, str] = {}
    for q_ids in DOMAIN_QUESTION_IDS.values():
        for q in q_ids:
            answers[q] = "no"
    return answers


def test_all_yes_gives_green():
    score = score_assessment("Test Bank", "test@test.com", "<$500M", "CRO", _all_yes_answers())
    assert score.overall_band == "GREEN"
    assert score.overall_score == pytest.approx(100.0, abs=1.0)
    for ds in score.domain_scores.values():
        assert ds.band == "GREEN"
        assert ds.pct == pytest.approx(100.0, abs=0.1)


def test_all_no_gives_red():
    score = score_assessment("Test Bank", "test@test.com", "<$500M", "CRO", _all_no_answers())
    assert score.overall_band == "RED"
    assert score.overall_score == pytest.approx(0.0, abs=0.1)
    for ds in score.domain_scores.values():
        assert ds.band == "RED"
        assert ds.pct == pytest.approx(0.0, abs=0.1)


def test_mixed_scores():
    answers = _all_yes_answers()
    # Force fair_lending_controls to all no
    answers["flc_1"] = "no"
    answers["flc_2"] = "no"
    answers["flc_3"] = "no"
    score = score_assessment("Mixed Bank", "mixed@test.com", "$500M–$2B", "MRM", answers)
    assert score.domain_scores["fair_lending_controls"].band == "RED"
    assert "fair_lending_controls" in score.top_3_gaps


def test_top_3_gaps_sorted():
    """top_3_gaps should be the 3 lowest-scoring domains."""
    answers = _all_yes_answers()
    # Degrade 3 domains
    for q in ["vi_1", "vi_2", "vi_3"]:
        answers[q] = "no"
    for q in ["om_1", "om_2", "om_3"]:
        answers[q] = "no"
    for q in ["flc_1", "flc_2", "flc_3"]:
        answers[q] = "partial"
    score = score_assessment("Gap Bank", "gap@test.com", "$2B–$10B", "CCO", answers)
    assert "validation_independence" in score.top_3_gaps
    assert "ongoing_monitoring" in score.top_3_gaps


def test_amber_band_boundary():
    # All partial → 50% per domain → AMBER overall
    answers = {q: "partial" for qs in DOMAIN_QUESTION_IDS.values() for q in qs}
    score = score_assessment("Amber Bank", "amber@test.com", "<$500M", "Other", answers)
    assert score.overall_band == "AMBER"
    assert 50.0 <= score.overall_score < 75.0


def test_12_domains_scored():
    score = score_assessment("Full Bank", "f@f.com", "<$500M", "CRO", _all_yes_answers())
    assert len(score.domain_scores) == 12


def test_weighted_domains_have_correct_weights():
    score = score_assessment("W Bank", "w@w.com", "<$500M", "CRO", _all_yes_answers())
    assert score.domain_scores["validation_independence"].weight == 1.3
    assert score.domain_scores["ongoing_monitoring"].weight == 1.3
    assert score.domain_scores["fair_lending_controls"].weight == 1.3
    assert score.domain_scores["model_inventory"].weight == 1.0
