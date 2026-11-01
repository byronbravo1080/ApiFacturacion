# ADR-004 · Selección de Git como sistema de control de versiones (frente a SVN) y organización en dos repositorios

- **Estado:** Aceptado. **Actualizado en `v0.3.0` (Hito H3)** para incorporar la fundamentación formal de la selección de **Git frente a Apache Subversion (SVN)** ([`08-matriz-git-vs-svn.md`](../08-matriz-git-vs-svn.md)), y **modificado por [ADR-005](adr-005-contrato-api-first-y-pruebas-bdd.md)** en el origen del contrato (`api/openapi.yaml` escrito antes del código). Ver también el detalle extendido en [ADR-006](adr-006-seleccion-git-vs-svn.md).
- **Fecha:** 2026-10-15 (actualizado el 2026-10-31 para el Hito H3)

## Contexto

El proyecto **FacturaEC** es desarrollado por un equipo distribuido de cuatro integrantes (`S4`) con presupuesto de infraestructura cero (`R2`), requisito de despliegue automatizado (`D4`, `E5`) y trazabilidad verificable de artefactos por hito (`S5`). El backend (FastAPI) y el frontend (Next.js) se despliegan en servicios distintos (Render y Vercel).

Para gobernar la configuración del software conforme a IEEE Std 828-2012 (IEEE, 2012), el equipo debe tomar dos decisiones acopladas:
1. **Seleccionar el sistema de control de versiones (VCS):** elegir entre un modelo distribuido (**Git**) y un modelo centralizado (**Apache Subversion · SVN**).
2. **Definir la topología de repositorios:** organizar el código en dos repositorios por contenedor o en un único monorrepositorio.

## Alternativas consideradas

### Parte A · Sistema de control de versiones: Git vs. Apache Subversion (SVN)

La evaluación detallada de las siete dimensiones (modelo, historial, ramas, trabajo sin conexión, permisos, rendimiento y ecosistema) se encuentra en [`docs/08-matriz-git-vs-svn.md`](../08-matriz-git-vs-svn.md), donde **Git obtuvo 4,70/5,00** frente a **2,65/5,00 de SVN**.

| Dimensión | Git (Distribuido · DVCS) | Apache Subversion · SVN (Centralizado · CVCS) |
|---|---|---|
| Modelo e historial | Instantáneas (*snapshots*) en un grafo DAG con integridad criptográfica SHA-1 (Chacon & Straub, 2014) | Diferencias basadas en árbol en un servidor central con revisiones enteras secuenciales `r1, r2...` (Collins-Sussman et al., 2011) |
| Ramas y fusiones | Punteros ligeros de 41 bytes creados en milisegundos; *three-way merge* nativo | Copias de directorios en el servidor (`/branches`) rastreadas con `svn:mergeinfo` |
| Trabajo sin conexión | Completo en local (`commit`, `log`, `diff`, `branch`, `merge` sin red) | Requiere red para `commit`, `log` y creación de ramas; sin red solo permite `status` y `diff` contra la base local |
| Permisos y acceso | Por repositorio completo; protección de rama `main` con PR y revisión cruzada | Permisos granulares nativos por subdirectorio (`mod_authz_svn`) y bloqueo exclusivo (`svn lock`) |
| Ecosistema CI/CD y CASE | Nativo y gratuito con GitHub Issues, Pull Requests, GitHub Actions (`ci.yml`), Spectral, Ruff y pytest | Requiere infraestructura propia de servidor SVN y carece de flujo nativo de Pull Requests en la nube gratuita |

**Alternativa considerada y descartada para FacturaEC: Apache Subversion (SVN).** Se descarta porque el modelo centralizado impide realizar commits atómicos sin conexión, penaliza la creación frecuente de ramas cortas por issue y no ofrece un flujo nativo y gratuito de Pull Requests con revisión cruzada y GitHub Actions (`R2`, `D4`).

### Parte B · Topología de repositorios: dos repositorios vs. monorepo

| Criterio | Dos repositorios (polirepo) | Un monorepo |
|---|---|---|
| Pipelines independientes | Simple: un workflow por repositorio | Requiere filtros por carpeta |
| Ciclo de despliegue por contenedor | Independiente | Acoplado al mismo historial |
| Sincronización del contrato API | Explícita mediante `api/openapi.yaml` versionado | Inmediata en un solo commit |
| Visibilidad de la documentación | Concentrada en el repositorio del backend | Concentrada en un único repositorio |

**Alternativa descartada:** un monorepo, porque acopla los pipelines y el historial de dos contenedores con tecnologías y plataformas de despliegue distintas.

## Decisión

1. **Seleccionar Git como sistema de control de versiones**, alojado en GitHub como repositorio gobernado:
   - Rama `main` protegida sin commits directos, exigiendo Pull Request vinculado a su issue (`Closes #N`), verificación automática en `.github/workflows/ci.yml` y revisión cruzada con comentario sustantivo (`CONTRIBUTING.md`).
   - Historial atómico con **Conventional Commits 1.0.0** y versiones etiquetadas con **SemVer** alineadas a los hitos (`v0.1.0`, `v0.2.0` y `v0.3.0`).
2. **Organizar el sistema en dos repositorios Git**:
   - `ApiFacturacion` (`facturaec-backend`): API FastAPI, contrato `api/openapi.yaml`, `docs/` (dossier, cadena CASE y gobierno), pruebas BDD (`tests/`) y workflow de CI.
   - `facturaec-frontend`: aplicación Next.js (en hito posterior).

## Consecuencias

- (+) **Positivas:**
  - Ramas cortas instantáneas por cada issue y fusión verificable mediante Pull Requests con revisión cruzada entre los cuatro integrantes (`S4`, `S5`).
  - Trabajo sin conexión completo para realizar commits atómicos e inspeccionar el historial local sin latencia de red.
  - Integridad criptográfica del historial y de las etiquetas de versión (`v0.1.0`, `v0.2.0`, `v0.3.0`).
  - Integración gratuita y directa con GitHub Actions, Spectral, OpenAPI Generator, Prism, Ruff y pytest (`R2`, `D4`, `E5`).
- (−) **Negativas y riesgos a mitigar:**
  - Mayor probabilidad de conflictos de fusión cuando dos ramas modifican concurrentemente las mismas líneas de un archivo; se mitiga manteniendo ramas de corta duración (< 48 h) y sincronizando frecuentemente con `main` (Forsgren et al., 2018; ver reporte en [`docs/09-reporte-conflicto.md`](../09-reporte-conflicto.md)).
  - Git no ofrece permisos de lectura/escritura por subcarpeta dentro de un mismo repositorio; se mitiga separando backend y frontend en dos repositorios y excluyendo secretos y certificados `.p12` en `.gitignore` ([`docs/10-gobierno-seguridad-y-dependencias.md`](../10-gobierno-seguridad-y-dependencias.md)).

## ¿En qué caso aplicaría Apache Subversion (SVN)?

Subversion sería la opción recomendada frente a Git en cualquiera de los siguientes escenarios (Collins-Sussman et al., 2011):
1. **Monorrepositorio corporativo con requisitos estrictos de confidencialidad por carpeta:** cuando una organización almacena en un solo repositorio central tanto módulos de software como documentación contable, contratos o certificados, y necesita autorizar o denegar lectura/escritura por subdirectorio específico (`path-based authorization`) sin permitir que el usuario descargue el resto del repositorio.
2. **Proyectos intensivos en activos binarios pesados no fusionables:** cuando el flujo principal gira en torno a archivos binarios de gran tamaño (diseños CAD, activos multimedia, imágenes médicas o paquetes compilados) que requieren *checkouts* parciales de una sola subcarpeta y bloqueo exclusivo en el servidor (`svn lock`) para impedir ediciones concurrentes.

## Vínculo

| Elemento | Referencia |
|---|---|
| Drivers | D4 |
| Escenarios | E5, E4 |
| Restricciones | R2, R5, R7 |
| Stakeholders | S4, S5 |
| Matriz comparativa | [`docs/08-matriz-git-vs-svn.md`](../08-matriz-git-vs-svn.md) |
| Normativa y literatura | Chacon & Straub (2014); Collins-Sussman et al. (2011); IEEE Std 828-2012; Nygard (2011) |
