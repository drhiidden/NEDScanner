# Roadmap — NEDScanner

Prioridades orientadas a **inventario y visibilidad** en redes propias o autorizadas. Sin capacidades ofensivas (MITM, envenenamiento, interceptación de credenciales).

## Alcance del producto

| Incluido | Fuera de alcance (MIT) |
|----------|-------------------------|
| Descubrimiento ARP/ICMP/mDNS | Ataques activos contra terceros |
| Escaneo Nmap con política fail-closed | MITM / poison |
| Wi‑Fi vía NetworkManager | Modificación de firewall del sistema |
| Historial, comparación, inventario de confianza | Sniffing promiscuo no documentado |

## Estado actual (v1.0.7)

| Área | Estado |
|------|--------|
| Descubrimiento ARP/ICMP | ✅ |
| Modo demo (WSL/CI sin root) | ✅ |
| Wi‑Fi (nmcli + demo) | 🟡 |
| Nmap con timeout y autorización UI | 🟡 |
| Inventario conocido / desconocido | ✅ |
| Topología en grafo | ❌ planificado |

## Próximas versiones

### v1.1

- Wi‑Fi estable en Linux sin depender del demo
- Persistencia y exportación mejorada de resultados de escaneo
- Comparación visual entre dos sesiones del mismo rango

### v1.2

- Pestaña **Topología** (grafo simple: hosts y enlaces inferidos)
- Señales ligeras de huella (p. ej. TTL) solo con fines de inventario

### v1.3+

- Alertas cuando aparece un host nuevo respecto al inventario de confianza
- Sniffer **solo lectura** con filtros BPF (homelab, opt-in)

## Uso responsable

Solo redes propias o con autorización escrita. Detalle legal: [DISCLAIMER.md](../DISCLAIMER.md).
