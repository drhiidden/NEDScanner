"""Escrituras atómicas y rutas de exportación acotadas."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

_MAX_JSON_BYTES = 1_048_576


def nedscaner_home() -> Path:
    return Path(os.path.expanduser("~/.nedscaner")).resolve()


def safe_export_path(user_path: str) -> Path:
    """Exportaciones solo bajo $HOME (evita path traversal a /etc, etc.)."""
    if not user_path or len(user_path) > 4096:
        raise ValueError("Ruta de exportación inválida")
    dest = Path(user_path).expanduser().resolve()
    home = Path.home().resolve()
    try:
        dest.relative_to(home)
    except ValueError as exc:
        raise ValueError("Solo se permite exportar bajo tu directorio home") from exc
    return dest


def atomic_write_json(path: Path, data: dict[str, Any], *, max_bytes: int = _MAX_JSON_BYTES) -> None:
    path = path.expanduser().resolve()
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(parent, 0o700)
    except OSError:
        pass
    text = json.dumps(data, indent=2, ensure_ascii=False)
    payload = text.encode("utf-8")
    if len(payload) > max_bytes:
        raise ValueError("Archivo demasiado grande")
    tmp = path.with_name(path.name + f".{os.getpid()}.tmp")
    tmp.write_bytes(payload)
    os.chmod(tmp, 0o600)
    tmp.replace(path)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
