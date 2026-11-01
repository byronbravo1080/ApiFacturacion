# ADR-006 · Selección de Git como sistema de control de versiones frente a Apache Subversion (SVN)

- **Estado:** Aceptado
- **Fecha:** 2026-10-31
- **Complementa:** [ADR-004](adr-004-repositorios-separados.md) y [`docs/08-matriz-git-vs-svn.md`](../08-matriz-git-vs-svn.md)

## Contexto

En el hito H3 (`v0.3.0`) el proyecto **FacturaEC** consolida su repositorio como un repositorio gobernado bajo las prácticas de gestión de configuración de IEEE Std 828-2012 (IEEE, 2012) y desarrollo seguro de NIST SSDF SP 800-218 (Souppaya et al., 2022). El equipo está conformado por cuatro integrantes (`S4`) que colaboran en paralelo sobre el contrato OpenAPI, el backend en FastAPI, las pruebas BDD y la documentación arquitectónica, bajo la restricción de costo cero de infraestructura (`R2`) y despliegue automatizado (`D4`, `E5`).

Se requiere fundamentar explícitamente la selección del sistema de control de versiones comparando el modelo distribuido de **Git** frente al modelo centralizado de **Apache Subversion (SVN)** a partir del análisis de siete dimensiones técnicas documentado en [`docs/08-matriz-git-vs-svn.md`](../08-matriz-git-vs-svn.md).

## Alternativas consideradas

1. **Git (Sistema de control de versiones distribuido · DVCS):** modela la historia como un grafo acíclico dirigido (DAG) de instantáneas (*snapshots*) verificadas con hashes SHA-1, donde cada copia local contiene el repositorio completo y las ramas son punteros ligeros de 41 bytes (Chacon & Straub, 2014).
2. **Apache Subversion · SVN (Sistema de control de versiones centralizado · CVCS):** mantiene un único repositorio central con revisiones globales secuenciales (`r1`, `r2`, ...), donde los clientes descargan copias de trabajo parciales, las ramas se crean como copias de directorios en el servidor (`/trunk`, `/branches`, `/tags`) y el control de acceso se gestiona por ruta (Collins-Sussman et al., 2011).

**Resultado de la matriz ponderada ([`08-matriz-git-vs-svn.md`](../08-matriz-git-vs-svn.md)):** Git obtuvo **4,70 / 5,00** frente a **2,65 / 5,00** de Subversion.

## Decisión

Seleccionar **Git** como sistema de control de versiones del proyecto FacturaEC, operando sobre GitHub con un modelo de **ramas de corta duración** (`<tipo>/issue-N-<descripcion>`), **Pull Requests obligatorios vinculados a issues** (`Closes #N`), **revisión cruzada** por al menos otro integrante, **commits atómicos bajo Conventional Commits 1.0.0** y **etiquetas SemVer** por cada hito (`v0.1.0`, `v0.2.0` y `v0.3.0`).

## Consecuencias

- (+) **Positivas:**
  - **Ramas y fusiones de bajo costo:** crear una rama por cada issue toma milisegundos y facilita aislar cada cambio hasta que pase las verificaciones de Ruff y pytest en `.github/workflows/ci.yml`.
  - **Autonomía sin conexión:** los integrantes pueden realizar commits atómicos, revisar el historial (`git log`) y comparar cambios (`git diff`) localmente sin depender de la disponibilidad de red.
  - **Trazabilidad e integridad:** cada commit y etiqueta SemVer queda protegido criptográficamente por su hash SHA-1 y vinculado a su issue y Pull Request (`S5`).
  - **Costo cero e integración CASE (`R2`, `D4`):** GitHub proporciona protección de ramas, plantillas de gobierno y ejecución de CI/CD de forma gratuita.
- (−) **Negativas:**
  - **Curva de manejo de conflictos concurrentes:** el trabajo distribuido en paralelo puede producir conflictos de fusión al modificar las mismas líneas (documentado y mitigado en [`docs/09-reporte-conflicto.md`](../09-reporte-conflicto.md)).
  - **Ausencia de permisos nativos por subcarpeta:** todo colaborador con acceso al repositorio puede leer todo su árbol; por ello nunca se versionan secretos ni certificados `.p12`.

## Caso en que aplicaría Subversion (SVN)

Se elegiría **Apache Subversion (SVN)** en lugar de Git si el contexto del sistema cambiara hacia (Collins-Sussman et al., 2011):
- Una **arquitectura de repositorio central único con control de acceso estricto por subdirectorio (`path-based authorization`)**, donde distintos roles (contadores externos, auditores o proveedores) deban tener permiso de lectura o escritura únicamente sobre una carpeta específica del árbol sin poder clonar el resto del código o documentos.
- Un **flujo centrado en archivos binarios pesados no fusionables** (archivos de diseño industrial, recursos multimedia de varios gigabytes o documentos ofimáticos bloqueables) donde sea indispensable realizar *checkouts* de subcarpetas aisladas y aplicar bloqueos exclusivos (`svn lock` / `svn:needs-lock`) antes de editar.

## Referencias

- Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress. https://git-scm.com/book/es/v2
- Collins-Sussman, B., Fitzpatrick, B. W., & Pilato, C. M. (2011). *Version control with Subversion: For Subversion 1.7*. O'Reilly Media. https://svnbook.red-bean.com
- Institute of Electrical and Electronics Engineers. (2012). *IEEE standard for configuration management in systems and software engineering* (IEEE Std 828-2012). IEEE.
- Nygard, M. (2011, 15 de noviembre). Documenting architecture decisions. *Cognitect Blog*. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
