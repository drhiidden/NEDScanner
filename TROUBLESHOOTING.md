# TROUBLESHOOTING — NEDScanner

Guía rápida para adopantes (Linux). No sustituye [docs/SECURITY-DESIGN.md](docs/SECURITY-DESIGN.md).

## La aplicación no arranca

| Síntoma | Causa habitual | Qué hacer |
|---------|----------------|-----------|
| `ModuleNotFoundError: PyQt6` | Dependencias sin instalar | `pip install -r requirements.txt` |
| Pantalla negra / sin estilos | Falta `app/ui/styles.qss` | Ejecutar desde la raíz del repo clonado |
| Crash al importar Scapy | Scapy opcional para ARP | Usa demo: `NEDSCANNER_DEMO=1 python main.py` o desactiva ARP en Descubrimiento |

## Modo demo (WSL, CI, sin capabilities)

```bash
export NEDSCANNER_DEMO=1
python main.py --demo
```

Datos sintéticos; no toca red real. Tests en CI usan el mismo flag vía fixtures.

## Descubrimiento / ARP

| Síntoma | Qué hacer |
|---------|-----------|
| «ARP requiere cap_net_raw» | `sudo setcap cap_net_raw+ep $(readlink -f $(which python3))` **solo si aceptas el riesgo**, o ejecuta con permisos adecuados en tu política local |
| «Scapy no disponible» | `pip install scapy` o desmarca ARP |
| Lista vacía en /24 grande | Política limita ICMP (máx. 64 hosts); prueba un CIDR más pequeño |

## Nmap

| Síntoma | Qué hacer |
|---------|-----------|
| `nmap no instalado` | `sudo apt install nmap` (o equivalente) |
| Escaneo se cancela con timeout | Configuración → Herramientas → subir timeout; o `NEDSCANNER_NMAP_TIMEOUT_S` |
| Objetivo rechazado | Revisa [scan_policy](app/core/scan_policy.py): solo rangos IPv4 permitidos; confirma autorización en Configuración → Seguridad |

## Wi‑Fi (NetworkManager)

| Síntoma | Qué hacer |
|---------|-----------|
| `nmcli no encontrado` | Instala NetworkManager CLI o usa modo demo |
| Sin redes listadas | Comprueba que la interfaz Wi‑Fi está activa (`nmcli dev wifi list`) |

## Tests y calidad local

```bash
pip install -r requirements-dev.txt
./scripts/verify-local.sh
```

`tests/test_opsec.py` revisa que README y docs no incluyan rutas de contexto privado (p. ej. árboles de documentación interna de otro proyecto).

## Logs

Salida en consola y en `~/.nedscaner.log`. Los adaptadores recortan stderr largo y objetivos de escaneo en mensajes de advertencia (sin volcar inventarios completos).
