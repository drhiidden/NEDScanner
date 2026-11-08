"""Docs públicos: sin rutas de contexto privado ajeno al adoptante."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
# Solo markdown orientado al público — no barrer app/ ni AGENTS (guía larga para contributors)
PUBLIC_MD = [
    ROOT / "README.md",
    ROOT / "ARCHITECTURE.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "TROUBLESHOOTING.md",
    ROOT / "CHANGELOG.md",
]
PUBLIC_MD.extend(ROOT.glob("docs/*.md"))

FORBIDDEN = (
    re.compile(r"\.procontext/"),
    re.compile(r"WS-HCP-HUB"),
    re.compile(r"MINIPROMPT"),
    re.compile(r"oss-gem-public-tree"),
    re.compile(r"/home/[a-z]+/projects/HALETHEIA"),
)


def _violations_in(text: str, path: Path) -> list[str]:
    rel = path.relative_to(ROOT)
    out: list[str] = []
    for pat in FORBIDDEN:
        for m in pat.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            out.append(f"{rel}:{line}:{m.group()}")
    return out


def test_public_markdown_has_no_private_context_leaks():
    hits: list[str] = []
    for path in PUBLIC_MD:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        hits.extend(_violations_in(text, path))
    assert not hits, "Rutas/contexto privado en docs públicos:\n" + "\n".join(hits[:30])


@pytest.mark.parametrize("script", list((ROOT / "scripts").glob("*.sh")))
def test_shell_scripts_avoid_dev_machine_abs_paths(script: Path):
    text = script.read_text(encoding="utf-8", errors="replace")
    assert not re.search(r"/home/[a-z]+/projects/HALETHEIA", text), (
        f"{script.name}: ruta de contexto privado"
    )
