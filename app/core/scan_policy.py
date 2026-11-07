"""Validación de objetivos de escaneo y política de alcance (fail-closed).

Referencias de diseño (HCP public skills, sin copiar lógica GPL):
- verification/ai-output-verification § Security
- 10-security/red-team-auditor (superficie subprocess / SSRF lateral)
- 10-security/secure-bash-scripting (defensa en profundidad)
"""
from __future__ import annotations

import os
import re
from ipaddress import ip_address, ip_network

from app.core.config import is_demo_mode
from app.core.user_prefs import is_allow_public_scan, is_scan_authorized

# Mínimo /20 → máximo ~4096 direcciones por CIDR
_MIN_PREFIXLEN = 20
_MAX_NMAP_TARGETS = 64
_INTERFACE_RE = re.compile(r"^[a-zA-Z0-9._-]{1,32}$")
_HOSTNAME_RE = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9.-]{0,62})?$")

_PRIVATE_V4 = (
    ip_network("10.0.0.0/8"),
    ip_network("172.16.0.0/12"),
    ip_network("192.168.0.0/16"),
    ip_network("169.254.0.0/16"),
    ip_network("127.0.0.0/8"),
)


class ScanPolicyError(ValueError):
    """Entrada o alcance rechazado antes de tocar la red."""


def require_scan_authorization() -> None:
    """Escaneo real (no demo) exige reconocimiento explícito de autorización."""
    if is_demo_mode():
        return
    if is_scan_authorized():
        return
    raise PermissionError(
        "Escaneo en red real bloqueado: activa la autorización en "
        "Configuración → Seguridad o confirma en el diálogo al escanear."
    )


def _assert_private_or_allowed(net: ip_network) -> None:
    if is_demo_mode():
        return
    if is_allow_public_scan():
        return
    if any(net.subnet_of(p) or net == p for p in _PRIVATE_V4):
        return
    raise ScanPolicyError(
        "Solo redes privadas/locales por defecto. "
        "Si tienes permiso para otro alcance: NEDSCANNER_ALLOW_PUBLIC=1"
    )


def validate_ipv4_cidr(target: str) -> str:
    raw = (target or "").strip()
    if not raw:
        raise ScanPolicyError("Especifique un CIDR IPv4")
    if any(c in raw for c in ";|&$`<>\"\n\r\t"):
        raise ScanPolicyError("Caracteres no permitidos en el objetivo")
    try:
        net = ip_network(raw, strict=False)
    except ValueError as exc:
        raise ScanPolicyError(f"CIDR inválido: {exc}") from exc
    if net.version != 4:
        raise ScanPolicyError("Solo IPv4 en esta versión")
    if net.prefixlen < _MIN_PREFIXLEN:
        raise ScanPolicyError(f"Rango demasiado amplio (usa máscara /{_MIN_PREFIXLEN} o más específica)")
    _assert_private_or_allowed(net)
    require_scan_authorization()
    return str(net)


def validate_ipv4_address(ip: str) -> str:
    raw = (ip or "").strip()
    if any(c in raw for c in ";|&$`<>\"\n\r\t"):
        raise ScanPolicyError("IP inválida")
    try:
        addr = ip_address(raw)
    except ValueError as exc:
        raise ScanPolicyError(f"IP inválida: {exc}") from exc
    if addr.version != 4:
        raise ScanPolicyError("Solo IPv4")
    if not is_demo_mode() and not is_allow_public_scan():
        private = any(addr in p for p in _PRIVATE_V4)
        if not private:
            raise ScanPolicyError("IP fuera de rangos privados/locales")
    return str(addr)


def validate_nmap_targets(raw: str) -> str:
    text = (raw or "").strip()
    if not text:
        raise ScanPolicyError("Especifique un objetivo para Nmap")
    if any(c in text for c in ";|&$`<>\"\n\r\t"):
        raise ScanPolicyError("Caracteres no permitidos en el objetivo")
    parts = [p.strip() for p in text.split(",") if p.strip()]
    if len(parts) > _MAX_NMAP_TARGETS:
        raise ScanPolicyError(f"Máximo {_MAX_NMAP_TARGETS} objetivos por escaneo")
    out: list[str] = []
    for part in parts:
        if "/" in part:
            out.append(validate_ipv4_cidr(part))
        elif re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", part):
            out.append(validate_ipv4_address(part))
        elif _HOSTNAME_RE.fullmatch(part):
            if is_demo_mode():
                out.append(part)
            else:
                raise ScanPolicyError(
                    "Hostnames solo en modo demo; use IPs o CIDR en escaneo real"
                )
        else:
            raise ScanPolicyError(f"Objetivo no permitido: {part!r}")
    require_scan_authorization()
    return ",".join(out)


def validate_interface(name: str | None) -> str | None:
    if not name or name == "default":
        return None
    iface = name.strip()
    if not _INTERFACE_RE.fullmatch(iface):
        raise ScanPolicyError("Nombre de interfaz inválido")
    return iface


def validate_inventory_ip(ip: str) -> str:
    """Inventario: no exige autorización de escaneo."""
    raw = (ip or "").strip()
    if any(c in raw for c in ";|&$`<>\"\n\r\t"):
        raise ScanPolicyError("IP inválida para inventario")
    try:
        addr = ip_address(raw)
    except ValueError as exc:
        raise ScanPolicyError(f"IP inválida: {exc}") from exc
    if addr.version != 4:
        raise ScanPolicyError("Solo IPv4 en inventario")
    return str(addr)
