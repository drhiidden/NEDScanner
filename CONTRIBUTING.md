# Contribuir a NEDScanner

Gracias por revisar o proponer mejoras. Repo: [drhiidden/NEDScanner](https://github.com/drhiidden/NEDScanner) (MIT).

## Requisitos

- Python 3.10+
- Linux (desarrollo probado en WSL; modo demo sin root)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

## Verificación obligatoria antes de PR/push

```bash
./scripts/verify-local.sh
# equivalente: pytest -q tests/
```

Incluye tests de política, adaptadores demo, preferencias y comprobación de que la documentación pública no arrastra rutas privadas (`tests/test_opsec.py`).

## Mantenimiento (HHP)

El flujo de publicación del mantenedor sigue el **Human Harness Protocol (HHP)**: verificación local (Gate VERIFY) antes de subir cambios, checklist humana en push y docs adoptantes sin contexto privado. No es un requisito para contribuir desde un fork; solo describe cómo se opera el repo canónico. Norma OSS de referencia: [Human Code AI Protocol](https://github.com/haletheia/human-code-ai-protocol).

## Estilo de cambios

- Lógica de red y validación en `app/core/` — sin PyQt.
- Nuevas integraciones → nuevo módulo en `app/adapters/` + tests demo o unitarios.
- UI solo orquesta; no saltarse `scan_policy` ni autorización.

## Seguridad

- No commitear tokens, capturas con datos reales de terceros ni rutas absolutas de tu máquina de desarrollo.
- Escaneo en red real solo en entornos autorizados; ver `DISCLAIMER.md` y Configuración → Seguridad.

## Commits (visibles en GitHub)

Conventional Commits en inglés o español, una idea por commit. Identidad: noreply de la cuenta que publica.

**Asunto y cuerpo adoptante-neutros:** describen el producto (UI, docs, tests), no gobernanza interna del mantenedor. Evita en metadatos git: ADRs, fases de integración, nombres de repos absorbidos, rutas de hub (`.procontext`), herramientas de escaneo del taller (`oss-gem`, `OPSEC`) o siglas de flujo interno en el mensaje (la norma puede citarse en `CONTRIBUTING`, no en cada commit).

```bash
./scripts/check-unpushed-commit-messages.sh   # solo commits ahead de origin/master
```

Detalle operativo del mantenedor → hub privado; el historial remoto debe leerse como changelog de producto.
