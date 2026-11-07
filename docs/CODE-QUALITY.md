# Calidad de código — NEDScanner

Checklist derivado de **hcp-skills** (público, MIT del proyecto). Sirve para revisiones antes de cada release.

## Skills de referencia

| Skill | Uso en este repo |
|-------|------------------|
| `verification/ai-output-verification` | Entradas validadas; smoke en `verify-local.sh` |
| `backend/code-review-enterprise` | Dimensiones seguridad / mantenibilidad / tests (tabla abajo) |
| `10-security/secure-bash-scripting` | Scripts con `set -e`, sin secretos en diff |
| `10-security/red-team-auditor` | Alcance de red, subprocess sin shell |
| `03-quality/resilience/ide-security-rules` | Trust loop: humano confirma escaneo real |

## Checklist (enterprise-lite)

### Seguridad

- [x] Política de escaneo (`scan_policy.py`) fail-closed
- [x] Autorización UI + `~/.nedscaner/preferences.json`
- [x] Exportaciones solo bajo `$HOME` (`safe_io.py`)
- [x] Inventario JSON atómico, permisos restrictivos
- [x] Tests unitarios pytest (`tests/`: `scan_policy`, adaptadores demo, `user_prefs`)
- [ ] Rotación / nivel log sin PII en producción — backlog

### Mantenibilidad

- [x] Capa `core/` sin PyQt (adaptadores + política + prefs)
- [x] Estilo confianza compartido (`trust_style.py`)
- [x] Diálogo de autorización aislado (`scan_authorization.py`)
- [x] Configuración modular en `app/ui/settings/*` (orquestador fino en `settings_tab.py`)
- [ ] Tipos `Protocol` para adaptadores — backlog

### Robustez

- [x] Errores de política → mensaje en UI (no crash silencioso)
- [x] Demo cache invalidable en tests (`config.is_demo_mode.cache_clear`)
- [x] Límites ICMP (/24, 64 hosts) y CIDR mínimo /20
- [x] Timeout global por escaneo Nmap (`nmap_adapter` + preferencias)
- [ ] Cierre ordenado de `ThreadPoolExecutor` al salir — backlog

### Legibilidad

- [x] Módulos cortos con docstring de propósito en `core/`
- [x] Nombres de pestañas y estados alineados con dominio (Conocido/Desconocido)
- [ ] `ARCHITECTURE.md` en raíz (hexagonal) — backlog v1.1

## Comando de verificación

```bash
pip install -r requirements-dev.txt   # una vez
./scripts/verify-local.sh           # incluye pytest -q tests/
pytest -q tests/                    # solo tests
```

## Próxima pasada recomendada

1. `@skill backend/code-review-enterprise` sobre diff completo v1.0.2→HEAD  
2. `@skill verification/ai-output-verification` tras cada feature UI  
3. Tipado `Protocol` en adaptadores y cierre explícito de executors al salir (v1.0.7)
