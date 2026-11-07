# Roadmap paridad inspirada en [NetPwn](https://github.com/letox4/netpwn)

**Revisión:** 2026-11-07 · NetPwn `main` activo (push 2026-11-05, ⭐2).

## Licencia (crítico)

| Proyecto | Licencia |
|----------|----------|
| **NEDScanner** | MIT |
| **NetPwn** | GPL-3.0 |

No se copia código de NetPwn en este repo. Solo se reimplementan **patrones** (bus de eventos, modo demo, topología, higiene firewall) y módulos **defensivos** alineados con auditoría en red propia.

## Qué ya compartimos conceptualmente

| Área | NetPwn | NEDScanner hoy |
|------|--------|----------------|
| Discovery ARP | ✅ | ✅ v1.0 adapter (`discovery_adapter.py`) |
| Modo demo sin root | ✅ `--demo` | ✅ `NEDSCANNER_DEMO=1` / `--demo` |
| Wi-Fi escaneo | ✅ avanzado | 🟡 UI stub |
| Nmap / puertos | ✅ | 🟡 UI stub |
| Topología grafo | ✅ | ❌ roadmap v1.2 |
| MITM / creds / poison | ✅ ofensivo | ❌ **fuera de alcance MIT** (o producto GPL aparte) |
| PÁNICO / iptables etiquetados | ✅ | ❌ solo si añadimos módulos que toquen fw |
| Cámaras IP / ONVIF | ✅ | ❌ backlog homelab |

## Fases sugeridas

### v1.0 (esta iteración)

- Descubrimiento real ARP/ICMP vía Scapy
- Modo demo para WSL/CI sin capabilities
- DISCLAIMER explícito en README

### v1.1

- Wi-Fi vía `nmcli_adapter` (ya existe esqueleto)
- Nmap vía `python-nmap` en worker thread + resultados en tabla
- Export JSON de escaneos

### v1.2

- Pestaña **Topología** (grafo: NetworkX + pyqtgraph o vista simple)
- Fingerprint TTL básico (como netpwn `fingerprint`)

### v2+ (decisión de producto)

- Sniffer solo lectura + BPF (audit homelab)
- **No** MITM sin proyecto separado GPL + checklist legal

## Uso responsable

Igual que [NetPwn DISCLAIMER](https://github.com/letox4/netpwn/blob/main/DISCLAIMER.md): solo redes propias o autorización escrita.
