# ADR-004 · Organización del código: dos repositorios (backend + docs / frontend)

- **Estado:** Aceptado. **Modificado por [ADR-005](adr-005-contrato-api-first-y-pruebas-bdd.md)** en el origen del contrato: ahora es `api/openapi.yaml`, escrito antes del código.
- **Fecha:** 2026-10-15

## Contexto

El backend (FastAPI) y el frontend (Next.js) se despliegan en servicios distintos (Render y Vercel). Habrá cuatro integrantes trabajando en paralelo y pipelines de CI/CD en una fase posterior. La entrega pide un repositorio etiquetado `v0.1.0` con la documentación en `docs/`.

## Alternativas consideradas

| Criterio | Dos repositorios (polirepo) | Un monorepo |
|---|---|---|
| Pipelines independientes | Simple: un workflow por repositorio | Requiere filtros por carpeta |
| Ciclo de despliegue por contenedor | Independiente | Acoplado al mismo historial |
| Sincronización del contrato API | Manual (OpenAPI versionado) | Inmediata en un solo commit |
| Visibilidad de la documentación | Concentrada en el backend | Concentrada en un único repositorio |
| Facilidad de revisión para el evaluador | Dos repositorios que enlazar | Un solo lugar |

**Alternativa descartada:** un monorepo. Mantiene el contrato de la API sincronizado en un solo commit, pero acopla los pipelines y el historial de dos contenedores que se despliegan en servicios distintos.

## Decisión

Usar **dos repositorios**:

- `facturaec-backend`: API FastAPI, `docs/` (dossier completo), `Dockerfile` y workflows. **En v0.1.0 (hito H1) contiene solo `docs/` y el `README`;** el código se incorporará en el hito siguiente.
- `facturaec-frontend`: aplicación Next.js.

El contrato entre ambos es el archivo OpenAPI generado por la API (`docs/openapi.json`). El entregable del dossier es el repositorio `facturaec-backend`, etiquetado `v0.1.0`. `facturaec-frontend` se creará y etiquetará cuando exista código de interfaz, y el `README` del backend lo enlazará.

## Consecuencias

- (+) Pipelines pequeños e independientes, alineados con los contenedores del C4 (E5, D4).
- (+) Trabajo en paralelo sin conflictos entre equipos de backend y frontend (S4).
- (+) Las vistas C4 coinciden con la estructura de repositorios prevista.
- (−) Riesgo de desalineación del contrato; se mitiga versionando `docs/openapi.json` y, en el hito H2, generando el cliente TypeScript del frontend desde él.
- (−) Cuando exista el frontend, el evaluador deberá consultar dos repositorios; se mitiga con enlaces cruzados en los `README`. En v0.1.0 solo hay uno.

## Vínculo

| Elemento | Referencia |
|---|---|
| Drivers | D4 |
| Escenarios | E5, E4 |
| Restricciones | R5, R7 |
| Stakeholders | S4, S5 |
| Vista C4 | Nivel 2: los contenedores «Aplicación web» (repositorio frontend) y «API REST» (repositorio backend) y la relación Aplicación web → API REST |
