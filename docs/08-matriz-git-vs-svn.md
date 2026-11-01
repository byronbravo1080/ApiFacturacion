# 08 · Matriz comparativa de sistemas de control de versiones: Git vs. Apache Subversion (SVN)

> Proyecto **FacturaEC** · Módulo 8 · Semana 3 · versión v0.3.0.
> Referencias principales: Chacon y Straub (2014), Collins-Sussman et al. (2011), Forsgren et al. (2018) e IEEE (2012).

---

## 1. Propósito y Contexto en FacturaEC

El estándar **IEEE Std 828-2012** establece que el plan de gestión de configuración del software debe fundamentar los mecanismos de identificación, control de cambios, auditoría de estados y trazabilidad de artefactos (IEEE, 2012). En el caso de **FacturaEC** —un sistema web de facturación electrónica desarrollado por un equipo de cuatro integrantes (`S4`), con presupuesto de infraestructura cero (`R2`), despliegue automatizado (`D4`, `E5`) y cadena CASE integrada (`v0.2.0`)—, la elección del sistema de control de versiones (VCS) condiciona directamente el flujo de trabajo colaborativo, la velocidad de ramificación y la integración continua.

Este documento compara las dos arquitecturas clásicas de control de versiones moderno:
1. **Git**: sistema de control de versiones distribuido (DVCS), creado por Linus Torvalds en 2005 (Chacon & Straub, 2014).
2. **Apache Subversion (SVN)**: sistema de control de versiones centralizado (CVCS), diseñado en 2000 por CollabNet como sucesor de CVS (Collins-Sussman et al., 2011).

---

## 2. Comparativa en las Siete Dimensiones de Evaluación

La Tabla 1 contrasta técnicamente Git y Subversion en las siete dimensiones exigidas por la actividad, con fundamento en los capítulos 1 y 2 de *Pro Git* (Chacon & Straub, 2014) y los capítulos 1 y 2 de *Version Control with Subversion* (Collins-Sussman et al., 2011).

| Dimensión | Git (DVCS) | Apache Subversion · SVN (CVCS) | Implicación para FacturaEC |
|---|---|---|---|
| **1. Modelo arquitectónico y almacenamiento de datos** | **Distribuido basado en instantáneas (*snapshots*):** Cada clon es una copia íntegra del repositorio y su historial completo. Modela los datos como un flujo de instantáneas del árbol de archivos; si un archivo no cambia entre commits, almacena solo un puntero al blob anterior (Chacon & Straub, 2014, cap. 1.3). | **Centralizado cliente-servidor basado en diferencias (*deltas*):** Existe un único repositorio maestro en un servidor central; cada desarrollador descarga una copia de trabajo (*working copy*) de una revisión específica y el servidor registra los cambios árbol por árbol a lo largo del tiempo (Collins-Sussman et al., 2011, cap. 1). | Con cuatro integrantes trabajando en horarios distintos y sin servidor dedicado propio (`R2`), el modelo distribuido elimina el punto único de fallo durante el desarrollo local. |
| **2. Historial e integridad** | **Grafo acíclico dirigido (DAG) con sumas criptográficas:** Cada commit se identifica mediante un hash SHA-1 (40 caracteres hexadecimales) calculado sobre el contenido del árbol, el autor, la fecha y el hash del commit padre. Es imposible alterar un archivo histórico sin que cambie el hash de todos los commits posteriores (Chacon & Straub, 2014, cap. 1.3). | **Numeración secuencial global de revisiones (`r1`, `r2`, `r3`...):** Cada commit incrementa en 1 el número de revisión global de todo el árbol del repositorio en el servidor central, lo que brinda identificadores cortos y legibles, pero sin encadenamiento criptográfico nativo entre revisiones (Collins-Sussman et al., 2011, cap. 1). | La integridad criptográfica de Git garantiza trazabilidad inmutable de las etiquetas de los hitos (`v0.1.0`, `v0.2.0`, `v0.3.0`) y del contrato `api/openapi.yaml` exigido por `S5`. |
| **3. Ramas y fusiones (*branching & merging*)** | **Punteros ligeros de 41 bytes:** Una rama en Git es simplemente un archivo de 41 bytes que contiene el hash SHA-1 del commit al que apunta (Chacon & Straub, 2014, cap. 3). Crear o cambiar de rama es instantáneo, y la fusión de tres vías (*three-way merge*) identifica automáticamente el ancestro común en el DAG. | **Copias de directorios en el árbol del repositorio:** En SVN las ramas y etiquetas no existen como primitiva separada, sino como directorios dentro del propio árbol (`/trunk`, `/branches`, `/tags`) creados mediante copias baratas de servidor (`svn copy` O(1)) y rastreados desde SVN 1.5 con la propiedad `svn:mergeinfo` (Collins-Sussman et al., 2011, cap. 2 y 4). | El flujo gobernado de FacturaEC exige ramas cortas por cada issue (`docs/issue-N-...`, `feat/issue-N-...`) y al menos 2 PR por integrante. En Git crear, alternar y fusionar estas ramas no tiene fricción ni requiere conexión al servidor. |
| **4. Trabajo sin conexión (*offline*)** | **Completo en local:** Dado que toda la base de datos histórica reside en `.git/`, el desarrollador puede hacer commits, consultar todo el historial (`git log`), comparar cualquier versión (`git diff`), crear ramas, fusionar y cambiar de contexto sin acceso a Internet (Chacon & Straub, 2014, cap. 1.1). | **Limitado sin red:** Para hacer commit (`svn commit`), consultar el historial (`svn log`), crear una rama o ver diferencias contra revisiones antiguas se requiere conexión activa con el servidor central. Sin red solo se puede editar archivos y comparar contra la revisión base descargada en `.svn/` (`svn status`, `svn diff`) (Collins-Sussman et al., 2011, cap. 1 y 2). | Permite a los integrantes realizar commits atómicos frecuentes (Conventional Commits) desde cualquier ubicación y sincronizar con `origin` solo al abrir el Pull Request. |
| **5. Permisos y control de acceso** | **Nivel de repositorio completo (y protección de ramas en la plataforma):** Por diseño distribuido, quien puede clonar un repositorio de Git obtiene todo su árbol e historial. No soporta permisos de lectura/escritura por subcarpeta dentro de un mismo repositorio (requiere separar en repositorios o submódulos). Las reglas de gobierno se aplican sobre ramas protegidas (`main`) en el servidor remoto. | **Control de acceso granular basado en rutas (*path-based authorization*):** Mediante `mod_authz_svn` o `svnserve`, el administrador puede definir permisos de lectura y escritura específicos para cada subdirectorio o archivo dentro del mismo repositorio (por ejemplo, restringir `/trunk/nominas` y abrir `/trunk/clientes`) (Collins-Sussman et al., 2011, cap. 6). | En FacturaEC los cuatro integrantes tienen acceso de lectura completo al código y se acordó separar backend y frontend en dos repositorios (`ADR-004`). Lo que se necesita es proteger la rama `main` con PR y revisión cruzada obligatoria, no ocultar subcarpetas. |
| **6. Rendimiento y archivos binarios** | **Operaciones locales en milisegundos; sensible a binarios pesados:** Comparar ramas, hacer commits, inspeccionar `blame` o cambiar de versión ocurre en disco local sin latencia de red. Sin embargo, como cada clon descarga toda la historia, versionar grandes volúmenes de binarios (gigabytes de diseño, instaladores o multimedia) degrada el tamaño del clon a menos que se use una extensión externa como Git LFS. | **Operaciones dependientes de la latencia de red; eficiente en *checkouts* parciales y binarios:** Las operaciones que consultan al servidor sufren la latencia de red, pero permite descargar únicamente un subdirectorio (*sparse checkout*) sin bajar la historia pasada, y aplica diferencias binarias (`svndiff`) de forma nativa sin inflar las copias de trabajo (Collins-Sussman et al., 2011, cap. 1). | Los artefactos de FacturaEC son texto plano (Python, YAML, Gherkin, Markdown y diagramas Mermaid como código), donde el rendimiento local de Git es óptimo. |
| **7. Ecosistema e integración CI/CD y CASE** | **Estándar de la industria para DevOps y revisión cruzada:** Integración nativa con GitHub Pull Requests, protección de ramas, plantillas `.github/`, GitHub Actions (`ci.yml`), linters de contratos (Spectral, Redocly), generadores (OpenAPI Generator) y herramientas de análisis estático (Ruff) (Forsgren et al., 2018). | **Orientado a flujos centralizados tradicionales:** Cuenta con clientes maduros (TortoiseSVN) e integración con servidores de CI clásicos (Jenkins), pero carece de un modelo nativo de Pull Requests con revisión cruzada ligera en la nube gratuita. | Toda la cadena CASE construida en `v0.2.0` y el pipeline `.github/workflows/ci.yml` de `v0.3.0` se ejecutan de forma nativa y gratuita sobre GitHub (`R2`, `D4`). |

---

## 3. Matriz de Evaluación Ponderada para FacturaEC

Para cuantificar la adecuación de ambas herramientas a los drivers arquitectónicos del proyecto (`D1`–`D5`) y a los requisitos de gobierno de esta unidad, la Tabla 2 asigna pesos que suman 100 % y califica cada alternativa en escala de 1 (deficiente) a 5 (óptimo).

| Criterio de evaluación | Dimensión asociada | Peso (%) | Git | Subversion (SVN) | Justificación técnica en el contexto de FacturaEC |
|---|---|---:|---:|---:|---|
| **C1. Flujo de ramas cortas, PR y revisión cruzada** | 3 y 7 | 30 | 5 | 2 | La práctica exige que todo cambio entre por rama corta, PR vinculado a issue y revisión cruzada. Git crea y fusiona ramas en milisegundos; en SVN las ramas son copias de directorios en el servidor y no existe el concepto nativo de PR. |
| **C2. Integración con cadena CASE y CI/CD a costo cero (`R2`, `D4`)** | 7 | 20 | 5 | 2 | GitHub ofrece repositorio, protección de rama `main`, plantillas de issue/PR y ejecución de GitHub Actions (`ruff` + `pytest`) sin costo. SVN requeriría alojar y mantener un servidor propio o contratar alojamiento especializado. |
| **C3. Trabajo autónomo sin conexión y commits atómicos** | 1 y 4 | 15 | 5 | 2 | En Git cada integrante realiza commits atómicos locales con Conventional Commits sin depender de la conexión al servidor central; en SVN todo `svn commit` y `svn log` exige red. |
| **C4. Integridad del historial y trazabilidad de hitos (`S5`)** | 2 | 15 | 5 | 4 | El grafo DAG con hashes SHA garantiza que las versiones etiquetadas (`v0.1.0`, `v0.2.0`, `v0.3.0`) sean criptográficamente verificables. SVN ofrece números de revisión secuenciales claros (`rN`), pero sin encadenamiento criptográfico. |
| **C5. Rendimiento sobre artefactos como código (Python, YAML, Mermaid)** | 6 | 10 | 5 | 3 | Todas las vistas C4 (Mermaid), el contrato OpenAPI y las pruebas Gherkin son archivos de texto, donde las operaciones locales de Git son inmediatas. |
| **C6. Control de permisos por subdirectorio y manejo de binarios pesados** | 5 y 6 | 10 | 2 | 5 | SVN supera claramente a Git cuando se requiere restringir permisos de lectura/escritura por subcarpeta dentro de un único repositorio o hacer *checkout* parcial de grandes activos binarios sin descargar toda la historia. |
| **Total ponderado ($\sum \text{peso} \times \text{puntaje} / 100$)** | | **100** | **4,70** | **2,65** | **Git supera a SVN por 2,05 puntos sobre 5** para las necesidades del proyecto FacturaEC. |

Cálculo detallado:
$$\text{Total}_{\text{Git}} = \frac{30(5) + 20(5) + 15(5) + 15(5) + 10(5) + 10(2)}{100} = \frac{470}{100} = 4{,}70$$
$$\text{Total}_{\text{SVN}} = \frac{30(2) + 20(2) + 15(2) + 15(4) + 10(3) + 10(5)}{100} = \frac{265}{100} = 2{,}65$$

---

## 4. Conclusión y Escenario en que Aplicaría Subversion (SVN)

1. **Decisión para FacturaEC:** Se selecciona **Git** (alojado en GitHub con rama `main` protegida) como sistema de control de versiones del proyecto. La decisión formal, sus consecuencias y su vínculo con la organización de repositorios quedan registrados en [`docs/03-adr/adr-004-repositorios-separados.md`](03-adr/adr-004-repositorios-separados.md) y en [`docs/03-adr/adr-006-seleccion-git-vs-svn.md`](03-adr/adr-006-seleccion-git-vs-svn.md).
2. **¿En qué caso concreto aplicaría Subversion (SVN)?**
   Subversion sería la alternativa superior si el proyecto u organización presentara simultáneamente estas condiciones (Collins-Sussman et al., 2011):
   - Un **monorrepositorio corporativo único** donde coexistan código fuente, documentos legales confidenciales y certificados o contratos por área, exigiendo **control de acceso estricto por subcarpeta** (`path-based authorization`) para que ciertos proveedores o auditores solo puedan leer o escribir una carpeta específica sin clonar el resto del repositorio.
   - Gestión de **grandes volúmenes de activos binarios no fusionables** (archivos CAD, recursos gráficos pesados, máquinas virtuales o paquetes compilados de varios gigabytes) donde los usuarios necesitan hacer *checkout* únicamente de una subcarpeta puntual y aplicar bloqueos exclusivos de archivo (`svn lock`) para evitar ediciones simultáneas imposibles de fusionar.

---

## 5. Referencias

- Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress. https://git-scm.com/book/es/v2
- Collins-Sussman, B., Fitzpatrick, B. W., & Pilato, C. M. (2011). *Version control with Subversion: For Subversion 1.7*. O'Reilly Media. https://svnbook.red-bean.com
- Conventional Commits. (s. f.). *Conventional Commits 1.0.0*. https://www.conventionalcommits.org/es/v1.0.0/
- Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The science of lean software and DevOps*. IT Revolution Press.
- Institute of Electrical and Electronics Engineers. (2012). *IEEE standard for configuration management in systems and software engineering* (IEEE Std 828-2012). IEEE.
- Nygard, M. (2011, 15 de noviembre). Documenting architecture decisions. *Cognitect Blog*. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- Preston-Werner, T. (s. f.). *Semantic Versioning 2.0.0*. https://semver.org/lang/es/
- Souppaya, M., Scarfone, K., & Dodson, D. (2022). *Secure software development framework (SSDF) version 1.1* (NIST Special Publication 800-218). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-218
