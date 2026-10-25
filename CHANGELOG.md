# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Versionado [SemVer](https://semver.org/lang/es/).

## [0.2.0] · 2026-10-25 · Hito H2 (semana 2): cadena CASE

### Agregado
- Mapa de toolchain con 10 tareas puntuadas (frecuencia × esfuerzo × riesgo) y una herramienta por fase (`docs/06-mapa-toolchain.md`).
- Historias HU1 a HU7, 25 escenarios Gherkin en español y matriz de trazabilidad (`docs/07-historias-y-criterios.md`, `tests/features/`).
- Contrato API-first `api/openapi.yaml` con 7 operaciones de negocio y `/health`, validado con Spectral (conjunto `spectral:oas` y 4 reglas propias) y Redocly.
- Documentación HTML (`docs/api/`), mock con Prism y stubs `python-fastapi` generados desde el contrato.
- Esqueleto ejecutable de la API (`src/facturaec/`): registro con JWT, clientes, productos, facturas con IVA, secuencial bajo bloqueo de fila, clave de acceso módulo 11 y envío al SRI simulado con reintentos.
- 31 pruebas: 25 escenarios con pytest-bdd (E1, E2, E6, incluida la concurrente contra PostgreSQL), 3 de conformidad entre el contrato y el código, y 3 de sincronía entre `docs/07` y los `.feature`.
- Matriz de evaluación y selección de herramientas según ISO/IEC 14102 (`docs/08-matriz-seleccion.md`).
- ADR-005: contrato API-first y pruebas BDD con pytest-bdd.
- Plantilla de pull request con rúbrica de revisión (`.github/pull_request_template.md`).

### Cambiado
- ADR-004 y vista C2: el contrato pasa de `docs/openapi.json` generado desde el código a `api/openapi.yaml` escrito antes del código.
- Registro de IA ampliado con los usos de la semana 2 (`docs/04-registro-ia.md`).

## [0.1.0] · 2026-10-18 · Hito H1: dossier de arquitectura
- Contexto, stakeholders, drivers, escenarios E1 a E8, vistas C4, ADR-001 a ADR-004 y registro de IA.
