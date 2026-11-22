"""Patrones prohibidos en mensajes de commit públicos (misma lista que scripts/check-unpushed)."""
from __future__ import annotations

import re

FORBIDDEN_IN_COMMIT_TEXT = (
    re.compile(r"ADR-\d+", re.I),
    re.compile(r"\bHHP\b"),
    re.compile(r"\bOPSEC\b", re.I),
    re.compile(r"oss-gem|oss-safe", re.I),
    re.compile(r"\.procontext"),
    re.compile(r"WS-HCP-HUB|MINIPROMPT", re.I),
    re.compile(r"hcp-skills", re.I),
    re.compile(r"Fase\s+\d", re.I),
    re.compile(r"network-security-scanner", re.I),
)


def test_example_neutral_commit_passes():
    text = "feat(ui): learning tab with lessons and scan context\n\nAdd Aprendizaje tab."
    assert not any(p.search(text) for p in FORBIDDEN_IN_COMMIT_TEXT)


def test_example_internal_commit_would_fail():
    bad = "fix(opsec): remove hub path for oss-gem scan\n\nADR-002 Fase 2."
    assert any(p.search(bad) for p in FORBIDDEN_IN_COMMIT_TEXT)