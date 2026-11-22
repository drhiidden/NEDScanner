#!/usr/bin/env sh
# Commits pendientes de push: asunto + cuerpo adoptante-neutro (oss gem gate).
set -e
cd "$(dirname "$0")/.."
UPSTREAM="${1:-origin/master}"
if ! git rev-parse --verify "$UPSTREAM" >/dev/null 2>&1; then
  echo "check-unpushed-commit-messages: sin $UPSTREAM; omitido"
  exit 0
fi
AHEAD="$(git rev-list --count "$UPSTREAM"..HEAD 2>/dev/null || echo 0)"
if [ "$AHEAD" = "0" ]; then
  echo "check-unpushed-commit-messages: nothing ahead of $UPSTREAM"
  exit 0
fi
export UPSTREAM
exec python3 - <<'PY'
import os
import re
import subprocess

upstream = os.environ["UPSTREAM"]
log = subprocess.check_output(
    ["git", "log", f"{upstream}..HEAD", "--format=%H%n%s%n%b%n---"],
    text=True,
)
chunks = [c.strip() for c in log.split("---") if c.strip()]
bad: list[str] = []
patterns = [
    (re.compile(r"ADR-\d+", re.I), "ADR interno"),
    (re.compile(r"\bHHP\b"), "sigla mantenedor (usar docs, no commit)"),
    (re.compile(r"\bOPSEC\b", re.I), "jerga OPSEC"),
    (re.compile(r"oss-gem|oss-safe", re.I), "herramienta hub"),
    (re.compile(r"\.procontext"), "ruta hub"),
    (re.compile(r"WS-HCP-HUB|HALETHEIA|MINIPROMPT", re.I), "contexto privado"),
    (re.compile(r"hcp-skills", re.I), "ruta skills hub"),
    (re.compile(r"Fase\s+\d|phase\s+\d", re.I), "fase integración interna"),
    (re.compile(r"network-security-scanner", re.I), "narrativa merge repos"),
    (re.compile(r"\bnss\b", re.I), "abrev. repo archivado"),
]
for chunk in chunks:
    lines = chunk.splitlines()
    if not lines:
        continue
    sha, subj = lines[0][:7], lines[1] if len(lines) > 1 else ""
    body = "\n".join(lines[2:]) if len(lines) > 2 else ""
    text = f"{subj}\n{body}"
    for pat, label in patterns:
        if pat.search(text):
            bad.append(f"{sha} ({subj!r}): {label} — {pat.pattern}")
            break
if bad:
    print("Commits con metadatos no adoptante (reescribe antes de push):", file=__import__("sys").stderr)
    for line in bad:
        print(f"  {line}", file=__import__("sys").stderr)
    raise SystemExit(1)
print(f"check-unpushed-commit-messages: OK ({len(chunks)} commit(s) ahead)")
PY