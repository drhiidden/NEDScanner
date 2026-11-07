# Diseño de seguridad — NEDScanner

**Versión:** 1.0.6 · **Licencia:** MIT · **Alcance:** herramienta local de auditoría en red propia.

## Principios (alineados con HCP Skills)

| Principio | Implementación en código | Skill HCP (referencia pública) |
|-----------|--------------------------|--------------------------------|
| Fail-closed en entradas | `app/core/scan_policy.py` | `verification/ai-output-verification` |
| Sin shell injection | `subprocess_exec` con argv fijos (`nmcli`); Nmap vía API, objetivo validado | `10-security/secure-bash-scripting` |
| Alcance mínimo | CIDR máx `/20`, redes privadas por defecto | `red-team-auditor` (SSRF/lateral) |
| Autorización explícita | Diálogo UI + `~/.nedscaner/preferences.json` o env `NEDSCANNER_I_ACK_AUTHORIZED=1` | Uso responsable + `DISCLAIMER.md` |
| Datos locales protegidos | `safe_io.atomic_write_json`, permisos `0600` en `~/.nedscaner/` | `ide-security-auditor` (credenciales en disco) |
| OPSEC en repo | `scripts/verify-local.sh` | `git/oss-safe-publish` |

## Variables de entorno

| Variable | Efecto |
|----------|--------|
| `NEDSCANNER_DEMO=1` | Sin sockets raw; datos ficticios; política de red relajada |
| `NEDSCANNER_I_ACK_AUTHORIZED=1` | Atajo env; equivalente al checkbox en Configuración → Seguridad |
| `NEDSCANNER_ALLOW_PUBLIC=1` | Permite objetivos fuera de RFC1918/link-local (requiere permiso legal) |
| `NEDSCANNER_NMAP_TIMEOUT_S` | Anula el timeout global Nmap (30–3600 s; por defecto 300) |

## Superficie de ataque

1. **UI → adaptadores:** todo objetivo pasa por `scan_policy` antes de Scapy/Nmap/nmcli; Nmap cancela tras timeout configurable.
2. **Export JSON:** rutas validadas con `safe_export_path` (solo bajo `$HOME`).
3. **Inventario:** validación de IP/MAC; JSON atómico con tope de tamaño.
4. **Logs:** `~/.nedscaner.log` — puede contener IPs; no almacenar credenciales en código.

## Fuera de alcance (v1.x)

- Escaneo ofensivo (MITM, credenciales, poison) — explícitamente excluido (MIT).
- Sandboxing del proceso GUI (futuro: distribución AppImage con permisos mínimos).

## Checklist pre-release

```bash
./scripts/verify-local.sh
```

Incluye smoke de política + inventario. Antes de push: revisar `git diff` (sin secretos ni rutas internas de hub corporativo).
