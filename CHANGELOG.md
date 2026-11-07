# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

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
- `scripts/verify-local.sh`: smoke OPSEC + adaptadores (modo demo, sin CI remoto).
- `docs/NETPWN-PARITY-ROADMAP.md` y `DISCLAIMER.md` (iteración 1.0+).

### Fixed

- Bucle qasync al cerrar la app (`main.py`) y escaneos async con `@asyncSlot` en descubrimiento.

### Changed

- README: modo demo, roadmap NetPwn (solo patrones MIT), nota pre-push con `verify-local.sh`.

## [1.0.0] - 2026-11-07

### Added

- Descubrimiento ARP/ICMP con Scapy y modo demo (`NEDSCANNER_DEMO=1` / `--demo`).
- Arquitectura hexagonal: `discovery_adapter`, modelos de host, datos demo centralizados.

## [0.1.0] - histórico

- GUI PyQt6 inicial: pestañas Wi‑Fi, Nmap, descubrimiento y resultados (prototipo).

[1.0.1]: https://github.com/drhiidden/NEDScanner/compare/b1b41f0...aa58d41
[1.0.0]: https://github.com/drhiidden/NEDScanner/compare/5a17c53...11c8456
[0.1.0]: https://github.com/drhiidden/NEDScanner/releases/tag/v0.1.0
