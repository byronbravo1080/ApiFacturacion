# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Versionado [SemVer](https://semver.org/lang/es/).

## [0.3.0] · 2026-11-01 · Hito H3 (semana 3): repositorio gobernado y selección Git vs SVN

### Agregado
- Guía de contribución y gobierno del repositorio (`CONTRIBUTING.md`) con flujo de ramas cortas, convención Conventional Commits, trazabilidad `Closes #n` y reglas de revisión cruzada.
- Plantillas de Issues para tareas e incidentes (`.github/ISSUE_TEMPLATE/tarea.md` y `.github/ISSUE_TEMPLATE/bug.md`).
- Flujo de integración continua en GitHub Actions (`.github/workflows/ci.yml`) que ejecuta `ruff check`, `ruff format --check` y `pytest` en cada Pull Request hacia `main`.
- Matriz comparativa en 7 dimensiones entre Git y Apache Subversion (SVN) con análisis ponderado y referencias APA (`docs/08-matriz-git-vs-svn.md`).
- ADR de selección de sistema de control de versiones Git frente a SVN (`docs/03-adr/adr-006-seleccion-git-vs-svn.md` y ampliación de `docs/03-adr/adr-004-repositorios-separados.md`).
- Reporte técnico de conflicto de integración deliberado, marcadores de Git, resolución y medidas de prevención (`docs/09-reporte-conflicto.md`).
- Documento de controles de gobierno en `main`, verificación de ausencia de secretos y auditoría de dependencias de `pyproject.toml` (`docs/10-gobierno-seguridad-y-dependencias.md`).

### Cambiado
- Plantilla de Pull Request (`.github/pull_request_template.md`) y `.gitignore` reforzados con controles de vinculación de Issues, verificación de secretos (`.p12`, `.pem`, `.env`) y artefactos de cobertura.
- Registro de uso de IA actualizado con las actividades y verificaciones de la semana 3 (`docs/04-registro-ia.md`).

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
