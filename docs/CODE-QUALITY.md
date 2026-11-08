# Calidad de código — NEDScanner

Checklist para revisiones locales antes de release o PR.

## Checklist

### Seguridad

- [x] Política de escaneo (`scan_policy.py`) fail-closed
- [x] Autorización UI + `~/.nedscaner/preferences.json`
- [x] Exportaciones solo bajo `$HOME` (`safe_io.py`)
- [x] Inventario JSON atómico, permisos restrictivos
- [x] Tests unitarios pytest (`tests/`: `scan_policy`, adaptadores demo, `user_prefs`)
- [x] Logs: recorte de objetivos y stderr (`app/core/log_redact.py`); archivo `~/.nedscaner.log` local

### Mantenibilidad

- [x] Capa `core/` sin PyQt (adaptadores + política + prefs)
- [x] Estilo confianza compartido (`trust_style.py`)
- [x] Diálogo de autorización aislado (`scan_authorization.py`)
- [x] Configuración modular en `app/ui/settings/*` (orquestador fino en `settings_tab.py`)
- [x] Tipos `Protocol` para adaptadores (`app/ports.py`)

### Robustez

- [x] Errores de política → mensaje en UI (no crash silencioso)
- [x] Demo cache invalidable en tests (`config.is_demo_mode.cache_clear`)
- [x] Límites ICMP (/24, 64 hosts) y CIDR mínimo /20
- [x] Timeout global por escaneo Nmap (`nmap_adapter` + preferencias)
- [x] Cierre ordenado de `ThreadPoolExecutor` al salir (`MainWindow.closeEvent`)

### Legibilidad

- [x] Módulos cortos con docstring de propósito en `core/`
- [x] Nombres de pestañas y estados alineados con dominio (Conocido/Desconocido)
- [x] `ARCHITECTURE.md` en raíz (hexagonal)

## Comando de verificación

```bash
pip install -r requirements-dev.txt   # una vez
./scripts/verify-local.sh           # incluye pytest -q tests/
pytest -q tests/                    # solo tests
```

## Revisión manual sugerida

1. Diff de la feature: ¿pasa por `scan_policy` y autorización?
2. ¿Nuevos subprocess sin `shell=True` y con timeout?
3. Ejecutar `verify-local.sh` en limpio antes de merge.
