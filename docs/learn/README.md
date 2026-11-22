# Aprende con tu red — NEDScanner

Material didáctico para usar **junto con la GUI**: lee un concepto, ejecuta el escaneo en la app y compara con tu LAN (solo redes **propias o autorizadas**).

## Ruta recomendada

| Paso | Lección | Practica en NEDScanner |
|------|---------|------------------------|
| 1 | [TCP/IP y modelo OSI](01-fundamentos-redes/tcp-ip-modelo-osi.md) | Pestaña **Descubrimiento** — qué hosts responden |
| 2 | [Puertos y servicios](01-fundamentos-redes/puertos-servicios.md) | Pestaña **Escaneo de Red** (Nmap) |
| 3 | [Reconocimiento pasivo](03-reconocimiento/reconocimiento-pasivo.md) | Inventario **Conocido / Desconocido** en descubrimiento |
| 4 | [Escaneo de puertos](04-escaneo-redes/escaneo-puertos.md) | Comparar dos sesiones en **Resultados** |

**Próximo (v1.2):** pestaña **Aprendizaje** en la app con tu último escaneo como ejemplo. Roadmap: [../ROADMAP.md](../ROADMAP.md).

## Modo demo (sin root)

```bash
NEDSCANNER_DEMO=1 python main.py
# o
python main.py --demo
```

Útil para seguir las lecciones en WSL o CI sin capacidades de red.

## Ética

Solo redes propias o con autorización escrita. [DISCLAIMER.md](../../DISCLAIMER.md).

## Origen

[ATTRIBUTION.md](ATTRIBUTION.md)