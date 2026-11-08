# Diseño de seguridad — NEDScanner

**Versión:** 1.0.8 · **Licencia:** MIT · **Alcance:** herramienta local de auditoría en red propia.

## Principios

| Principio | Implementación en código |
|-----------|--------------------------|
| Fail-closed en entradas | `app/core/scan_policy.py` |
| Sin shell injection | `subprocess` con argv fijos (`nmcli`); Nmap vía API, objetivo validado |
| Alcance mínimo | CIDR máx `/20`, redes privadas por defecto |
| Autorización explícita | Diálogo UI + `~/.nedscaner/preferences.json` o env `NEDSCANNER_I_ACK_AUTHORIZED=1` |
| Datos locales protegidos | `safe_io.atomic_write_json`, permisos `0600` en `~/.nedscaner/` |
| Verificación antes de release | `scripts/verify-local.sh` + pytest |

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

Incluye smoke de política, adaptadores demo e inventario.
