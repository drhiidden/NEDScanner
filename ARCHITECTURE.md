# Arquitectura — NEDScanner

Aplicación GUI **PyQt6** para inventario y visualización de red en Linux. Sigue un diseño **hexagonal** ligero: dominio y política en `app/core/`, puertos en `app/ports.py`, implementaciones en `app/adapters/`, UI en `app/ui/`.

## Capas

```text
app/ui/          → pestañas Qt, diálogos, estilos (dependen de core + adapters)
app/adapters/    → Nmap, nmcli, Scapy (demo vs real según config)
app/core/        → scan_policy, prefs, inventario, safe_io, demo_data
app/models/      → DTOs (Host, NmapHost, WifiNetwork)
app/ports.py     → Protocol (contratos)
```

## Flujo de escaneo real

1. Usuario define objetivo en UI.
2. `scan_policy` valida CIDR/IP/targets; sin autorización → bloqueo (fail-closed).
3. Adaptador ejecuta herramienta (o datos demo).
4. Resultados → historial de sesión / Resultados / inventario conocido.

## Modo demo

`NEDSCANNER_DEMO=1` o `--demo`: sin sockets privilegiados; datos en `app/core/demo_data.py`.

## Datos locales

| Ruta | Uso |
|------|-----|
| `~/.nedscaner/preferences.json` | Autorización, timeout Nmap |
| `~/.nedscaner/known-devices.json` | Allowlist hosts/redes |
| `~/.nedscaner.log` | Log aplicación (puede contener IPs) |

## Verificación

```bash
pip install -r requirements-dev.txt
./scripts/verify-local.sh   # pytest -q tests/
```

## Dependencias externas

- **Nmap** — escaneo puertos
- **NetworkManager / nmcli** — Wi‑Fi
- **Scapy** — ARP/ICMP (descubrimiento)
