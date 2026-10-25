# ADR-005 · Cadena CASE: contrato API-first y pruebas BDD con pytest-bdd

- **Estado:** Aceptado
- **Fecha:** 2026-10-23
- **Modifica:** ADR-004, en la ubicación y el origen del contrato (antes, `docs/openapi.json` generado desde el código)

## Contexto

En el hito H2 el backend pasa de dossier a código ejecutable. La cadena CASE del Módulo 8 exige que historias, contrato, documentación, stubs y pruebas estén enlazados, y que las pruebas se deriven de los criterios de aceptación. Hay que decidir dos cosas:

1. **Origen del contrato.** Puede escribirse antes del código (API-first) o generarse desde el código (code-first, lo que hace FastAPI por defecto y lo que suponía el ADR-004).
2. **Herramienta para ejecutar los criterios Gherkin** sobre un backend en Python.

E1 y E2 dependen de respuestas precisas del contrato (401, 404, 202, 409). Con dos repositorios (ADR-004), el contrato es además el acuerdo con el futuro frontend.

## Alternativas consideradas

### Origen del contrato

| Criterio | API-first (`api/openapi.yaml` escrito a mano) | Code-first (`openapi.json` que genera FastAPI) |
|---|---|---|
| Fuente de verdad | El contrato, revisado antes de programar | El código; el contrato es un subproducto |
| Validación con linter antes de construir | Sí (Spectral, Redocly) | Solo después de programar |
| Mock para el frontend antes del backend | Sí (Prism) | No hasta que exista el código |
| Riesgo de desfase contrato ↔ código | Alto si nadie lo vigila | Bajo: siempre coinciden |
| Esfuerzo | Mayor: el YAML se escribe y se mantiene | Menor |

### Ejecución de los criterios Gherkin

| Criterio | pytest-bdd | behave | Cucumber.js (demo de la sesión 4) |
|---|---|---|---|
| Lenguaje | Python, el mismo del backend | Python | JavaScript: obliga a un segundo entorno |
| Gherkin en español (`# language: es`) | Sí (verificado en esta semana) | Sí, según su documentación (no probado) | Sí (demo de la sesión 4) |
| Integración con pytest (fixtures, marcadores, PostgreSQL) | Nativa | No (corredor propio) | No |
| Acceso directo a la base para verificar E6 | Sí, con las mismas fixtures | Sí | Requiere llamar a la API o a otra conexión |

## Decisión

1. **Contrato API-first:** `api/openapi.yaml` es la fuente de verdad. Se valida con Spectral (sin errores, como condición para generar) y de él se generan la documentación (`docs/api/`), el mock (Prism) y los stubs (`generated/stubs-fastapi/`). La API publica ese mismo contrato en `/docs`, no el que infiere FastAPI.
2. **El riesgo de desfase se controla con pruebas automáticas.** `tests/test_contrato.py` falla si el código y el contrato no tienen exactamente las mismas operaciones, y las respuestas reales se validan también con Prism en modo proxy.
3. **pytest-bdd** ejecuta los archivos `.feature` de `tests/features/`. La prueba concurrente de E6 (CA5.3) se ejecuta contra PostgreSQL; con SQLite se omite (ADR-002).
4. **Los stubs generados no se editan a mano.** La implementación vive en `src/facturaec/`, porque el stub `python-fastapi` no entrega el token a la implementación y no permite filtrar por emisor (E1).

## Consecuencias

- (+) El contrato se valida y se prueba con mock antes de programar. En esta semana, la revisión del borrador encontró dos errores graves antes de escribir código (ver el [registro de IA](../04-registro-ia.md)).
- (+) Los criterios se escriben una sola vez y se ejecutan tal cual; `tests/test_documentacion.py` comprueba que `docs/07` muestra el mismo Gherkin que se ejecuta.
- (+) El frontend (ADR-004) puede trabajar contra el mock de Prism antes de que exista el backend.
- (−) Mantener el YAML cuesta más que generarlo; se compensa con la validación y las pruebas de conformidad.
- (−) Los stubs generados sirven como referencia de forma, no como base editable. Si se regeneran, no se pierde nada, porque la implementación está aparte.
- (−) Quien ejecute las pruebas solo con SQLite no prueba E6; el pipeline de CI (hito posterior) debe usar PostgreSQL.

## Vínculo

| Elemento | Referencia |
|---|---|
| Drivers | D1, D2, D3, D4 |
| Escenarios | E1, E2, E6 |
| Restricciones | R2, R5 |
| Stakeholders | S4, S5 |
| Tareas del mapa | T1, T4, T5, T6, T7 ([`06-mapa-toolchain.md`](../06-mapa-toolchain.md)) |
| Vista C4 | Nivel 2: relación Aplicación web → API REST («Consume el contrato OpenAPI») |
