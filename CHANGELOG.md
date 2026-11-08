# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [1.0.8] - 2026-11-08

### Changed

- Documentación adoptante: roadmap propio (`docs/ROADMAP.md`); eliminado doc de paridad con terceros.
- `DISCLAIMER.md` autocontenido; README sin referencias a otros proyectos.
- `docs/CODE-QUALITY.md` sin metodología externa; `test_opsec` acotado a fugas de rutas privadas.

## [1.0.7] - 2026-11-07

### Added

- `ARCHITECTURE.md`, `CONTRIBUTING.md`, `app/ports.py` (Protocol para adaptadores).
- `TROUBLESHOOTING.md`, `app/core/log_redact.py` + tests.

### Changed

- Cierre ordenado: `MainWindow.closeEvent` apaga pools de descubrimiento y Nmap.
- Logs Nmap/nmcli: objetivos y stderr recortados (menos PII en `~/.nedscaner.log`).

## [1.0.6] - 2026-11-07

### Added

- Timeout global de escaneo Nmap (`asyncio.wait_for`): preferencia `nmap_scan_timeout_s`, override `NEDSCANNER_NMAP_TIMEOUT_S`.
- Configuración → Herramientas: spinbox de timeout (30–3600 s).
- `tests/test_opsec.py` y `tests/test_known_inventory_smoke.py`; OPSEC adoptante vía pytest (no lógica duplicada en shell).

### Changed

- `app/ui/settings_tab.py` orquesta paneles en `app/ui/settings/` (general, herramientas, seguridad, avanzado, inventario).
- `scripts/verify-local.sh` delega solo en `pytest tests/` (Tier D mínimo).

## [1.0.5] - 2026-11-07

### Added

- Suite `tests/`: pytest para `scan_policy`, adaptadores en demo, `user_prefs`.
- `requirements-dev.txt`, `pytest.ini`; `verify-local.sh` ejecuta pytest sin `NEDSCANNER_DEMO`.

## [1.0.4] - 2026-11-07

### Added

- Diálogo de autorización al iniciar escaneo real; preferencias en `~/.nedscaner/preferences.json`.
- Configuración → Seguridad: checkboxes autorización y alcance público.
- Barra de estado con modo demo / autorizado / bloqueado.
- [docs/CODE-QUALITY.md](docs/CODE-QUALITY.md) (hcp-skills: review, verification, mantenibilidad).

### Changed

- `user_prefs` desacopla Qt de `scan_policy`; estilo confianza en `trust_style.py`.

## [1.0.3] - 2026-11-07

### Security

- `scan_policy`: validación CIDR/IP/objetivos Nmap; bloqueo de metacaracteres; redes privadas por defecto.
- Gate `NEDSCANNER_I_ACK_AUTHORIZED=1` para escaneo real; `NEDSCANNER_ALLOW_PUBLIC=1` opcional.
- Export JSON solo bajo `$HOME`; inventario con escritura atómica y permisos restrictivos.
- [docs/SECURITY-DESIGN.md](docs/SECURITY-DESIGN.md) mapeado a skills HCP (`ai-output-verification`, `red-team-auditor`, `secure-bash-scripting`).

## [1.0.2] - 2026-11-07

### Added

- Inventario conocido en `~/.nedscaner/known-devices.json` (hosts LAN + redes Wi‑Fi).
- Pestaña **Resultados**: historial de sesión real, alertas de desconocidos, export JSON, comparar 2 descubrimientos.
- **Descubrimiento**: columna Estado, resaltado naranja, «Marcar como conocida».
- **Configuración → Inventario**: edición manual del allowlist.

### Changed

- Wi‑Fi/Nmap: filas de redes no inventariadas resaltadas; historial Nmap con detalle de puertos.

## [1.0.1] - 2026-11-07

### Added

- Adaptadores demo/real para Wi‑Fi (`nmcli`) y escaneo Nmap (`python-nmap`).
- Export JSON y historial de sesión en descubrimiento; handoff descubrimiento → pestaña Nmap.
- `scripts/verify-local.sh`: smoke de adaptadores (modo demo).
- `docs/ROADMAP.md` y `DISCLAIMER.md`.

### Fixed

- Bucle qasync al cerrar la app (`main.py`) y escaneos async con `@asyncSlot` en descubrimiento.

### Changed

- README: modo demo, enlace a roadmap y guía de contribución.

## [1.0.0] - 2026-11-07

### Added

- Descubrimiento ARP/ICMP con Scapy y modo demo (`NEDSCANNER_DEMO=1` / `--demo`).
- Arquitectura hexagonal: `discovery_adapter`, modelos de host, datos demo centralizados.

## [0.1.0] - histórico

- GUI PyQt6 inicial: pestañas Wi‑Fi, Nmap, descubrimiento y resultados (prototipo).

[1.0.1]: https://github.com/drhiidden/NEDScanner/compare/b1b41f0...aa58d41
[1.0.0]: https://github.com/drhiidden/NEDScanner/compare/5a17c53...11c8456
[0.1.0]: https://github.com/drhiidden/NEDScanner/releases/tag/v0.1.0
