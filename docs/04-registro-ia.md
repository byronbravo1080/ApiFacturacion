# 04 · Registro de uso de IA

Registro de los usos de IA del proyecto. La primera parte cubre el dossier (Módulo 8, sesiones 1 a 3, v0.1.0). La [segunda parte](#semana-2-sesiones-4-a-6--cadena-case-v020) cubre la cadena CASE (semana 2, v0.2.0). Cada entrada indica qué se pidió, qué produjo la IA, qué defectos se encontraron, qué decisión tomó el equipo y cómo se verificó.

**Herramienta y versión:** Claude Sonnet 5.5 (`claude-sonnet-5-5`), Anthropic, mediante `claude.ai`.
**Protección de datos:** no se ingresaron credenciales, certificados de firma, RUC reales ni datos de clientes. Solo se compartieron el texto de las actividades y los escenarios del proyecto.

## Semana 1 (sesiones 1 a 3) · Dossier v0.1.0

### Registro del contraste

| Sesión y uso | Qué se pidió | Hallazgo de la IA | Decisión del equipo | Cómo se verificó |
|---|---|---|---|---|
| **S2 · Borrador de diagrama como código** | C4 niveles 1 y 2 en Mermaid con nombres consistentes y relaciones etiquetadas (verbo y, en el nivel 2, tecnología), a partir de la descripción del sistema | Produjo `c1-contexto.md` (C4Context), `c2-contenedores.md` (C4Container) y una vista complementaria `c3-componentes-api.md` (flowchart), con una sola convención de nombres: Dueño de negocio, Contador externo, Cliente final, FacturaEC, SRI, Aplicación web, API REST, Base de datos, SriGateway. Al decidirse entregar solo la documentación se cambió el texto de dos etiquetas, sin alterar la estructura | Aceptar C1 y C2 como base del dossier y C3 como vista complementaria | La sintaxis de los tres diagramas se validó con el parser de Mermaid en GitHub (renderizado válido) y se revisó la consistencia de nombres entre C1, C2 y C3 |
| **S3 · Recálculo de la matriz ponderada** | Verificar la aritmética de la matriz (3 alternativas × 7 criterios), los totales y las variantes de pesos | Un script reprodujo los totales A1 4,40, A2 3,30 y A3 3,90 y las tres variantes de pesos originales (4,25 / 3,90 / 3,45; 4,35 / 3,80 / 3,70; 4,29 / 3,29 / 3,86). Al incorporar E8 se añadieron dos variantes: con A1 = 3 en fiabilidad, 4,20 / 3,30 / 3,90; y con además más peso a la fiabilidad, 4,00 / 3,80 / 3,70. A1 gana en todas y el margen mínimo frente a A2 es 0,20 | Mantener puntajes y pesos; el punto de sensibilidad de E8 consta en el ADR-003 | Script en Python (Σ peso × puntaje / 100) y comprobación en hoja de cálculo (`=SUMAPRODUCTO(pesos; puntajes)/100`), cuyos resultados coinciden con las tablas de `01-contexto-y-drivers.md` |


## Semana 2 (sesiones 4 a 6) · Cadena CASE v0.2.0

**Herramienta y versión:** Claude Opus 5.5 (`claude-opus-5-5`), Anthropic, mediante `claude.ai`. Para las revisiones del contrato y de consistencia documental (`IA-S5-03`, `IA-S5-04` e `IA-S6-03`) se abrieron sesiones nuevas y separadas sin el contexto previo de redacción.

**Protección de datos (LOPDP):** no se ingresaron credenciales, certificados, URI de bases de datos, RUC reales ni datos de clientes. Los RUC de las pruebas son ficticios (provincia 99). La base PostgreSQL de las pruebas fue local y temporal; no se compartió con la IA ninguna URI ni credencial de Supabase.

**Regla aplicada:** ninguna salida de la IA se aceptó sin una verificación por ejecución real (Spectral, Redocly, Prism, pytest o Ruff) o sin contrastarla con los criterios y escenarios del dossier.

### Resumen

| ID | Sesión y tarea | Uso de la IA | Defectos encontrados al verificar | Decisión del equipo |
|---|---|---|---|---|
| IA-S4-01 | S4 · T1 a T10 | Borrador del mapa de toolchain, puntajes y matriz de selección | 2 cifras mal contadas en el texto | Modificar |
| IA-S5-01 | S5 · T1 | Borrador de historias y criterios en Gherkin | Ninguno al ejecutar; 1 limitación declarada (CA6.2) | Aceptar con la limitación |
| IA-S5-02 | S5 · T4 | Borrador v1 del contrato OpenAPI | 18 hallazgos de revisión, 17 y 8 advertencias de los linters, ejemplos de error engañosos en el mock, 1 dígito verificador mal calculado | Modificar |
| IA-S5-03 | S5 · T4 | Claude como revisor del contrato v1 (herramienta evaluada) | 1 hallazgo de 18 parcialmente incorrecto | Modificar el hallazgo R15; aceptar los demás |
| IA-S5-04 | S5 · T4 | Repetición de la revisión para medir reproducibilidad | Se repitió el mismo hallazgo parcialmente incorrecto | Usar la medición en C2 de la matriz |
| IA-S6-01 | S6 · T6 y T7 | Código del esqueleto (`src/`) | Secuencial duplicado bajo concurrencia; `null` contrario al contrato; 38 hallazgos de Ruff | Modificar |
| IA-S6-02 | S6 · T7 | Pasos de las pruebas de aceptación BDD | Prueba de conformidad vacía por un cambio de FastAPI; aviso de longitud de clave en PyJWT | Modificar |
| IA-S5-05 | S5 · T3, T4 | ADR-005 y ajustes al ADR-004 y a la vista C2 | Una afirmación sin probar (soporte de español en behave) | Modificar |
| IA-S6-03 | S6 · entrega | Revisión cruzada de consistencia de la matriz, el informe y las cifras | 20 observaciones: 4 graves (matriz, costo, cifras) y 16 menores | Modificar |

### IA-S4-01 · Mapa de toolchain y matriz de selección

| Campo | Contenido |
|---|---|
| Prompt resumido | Con la práctica 04 del docente y el dossier como modelo: estructurar el proceso de FacturaEC por fase, listar 10 tareas, puntuarlas con F × E × R justificando cada valor con un hecho observable, y asignar herramienta y categoría por fase. Después, estructurar la matriz ISO/IEC 14102 con pesos que sumen 100 y puntajes tomados de las pruebas reales |
| Salida | Borrador de `docs/06-mapa-toolchain.md` y `docs/08-matriz-seleccion.md` |
| Defectos | El texto decía «19 esquemas» en el contrato y «40 archivos» generados; el conteo real sobre el repositorio dio 16 y 50. La matriz asignaba a la IA un 2 en reproducibilidad sin haberla medido |
| Decisión | **Modificar:** se corrigieron las cifras. Se midió la reproducibilidad repitiendo la revisión (IA-S5-04), y el puntaje pasó a 3 |
| Verificación | Conteo sobre `api/openapi.yaml` y `generated/`, y acuerdo del equipo sobre los puntajes F, E y R. Los totales y las variantes de la matriz se recalcularon con un script (Σ peso × puntaje / 100) |

### IA-S5-01 · Historias y criterios en Gherkin

| Campo | Contenido |
|---|---|
| Prompt resumido | Redactar historias «Como / quiero / para» ligadas a S, D y E del dossier, y criterios en Gherkin en español con las medidas numéricas de E1, E2 y E6, un comportamiento por escenario. No agregar requisitos fuera del dossier |
| Salida | 7 historias, 25 escenarios en `tests/features/*.feature` y `docs/07-historias-y-criterios.md` |
| Defectos | Ninguno al ejecutar: pytest-bdd interpretó los 25 escenarios y todos pasan. Una **limitación**: CA6.2 verifica las esperas de 1 s y 2 s con un reloj simulado, así que el límite de 60 s se mide sobre una ejecución de menos de un segundo. Está declarada en `docs/07` |
| Decisión | **Aceptar** con la limitación declarada |
| Verificación | Ejecución con pytest-bdd, revisión INVEST y lista de ISO/IEC/IEEE 29148 (`docs/07`, secciones 2.1 y 4), y `tests/test_documentacion.py`, que falla si `docs/07` deja de mostrar el Gherkin que se ejecuta |

### IA-S5-02 · Contrato OpenAPI (borrador v1 y correcciones)

| Campo | Contenido |
|---|---|
| Prompt resumido | Escribir un contrato OpenAPI 3.0.3 API-first para las historias HU1 a HU7, partiendo de la tabla de endpoints de la vista C2, sin datos personales |
| Salida | `docs/evidencias/openapi-v1-borrador.yaml` (v1), corregido en `api/openapi.yaml` |
| Defectos | **(1)** El `security` global se heredaba en el registro y en `/health`: nadie podía registrarse (rompía CA1.1). Lo detectó la revisión con IA, no los linters. **(2)** Faltaban 401, 404, 409 y 422, el esquema de error y los `required`. **(3)** Spectral dio 17 advertencias y Redocly 8. **(4)** El mock de Prism devolvía el mismo ejemplo `NO_ENCONTRADO` en el 401 y el 422. **(5)** El ejemplo de clave de acceso agregado en la corrección tenía un dígito verificador incorrecto (terminaba en 4); al recalcular el módulo 11 dio 1 |
| Decisión | **Modificar:** se aplicaron las correcciones aceptadas de la revisión, se agregaron ejemplos por tipo de error y se corrigió la clave de ejemplo |
| Verificación | Spectral sin hallazgos de ninguna severidad, Redocly válido, mock de Prism, cálculo del módulo 11 con un script y prueba de conformidad (`tests/test_contrato.py`) |

### IA-S5-03 · Claude como revisor del contrato (herramienta evaluada en la matriz)

| Campo | Contenido |
|---|---|
| Prompt resumido | «Actúa como revisor crítico de contratos. No reescribas ni inventes requisitos ni ejecutes linters. Para cada defecto: ubicación, defecto, severidad, criterio afectado y corrección» |
| Salida | 18 hallazgos: 6 errores, 8 advertencias y 4 de información sobre `docs/evidencias/openapi-v1-borrador.yaml` |
| Defectos | R15 era parcialmente incorrecto: trató como el mismo dato dos contadores distintos (los intentos de la solicitud y el total acumulado) |
| Decisión | **Aceptar** 17 hallazgos. **Modificar** R15: se conservan los dos campos con nombres que los distinguen (`intentosEnEsteEnvio` e `intentosEnvio`). Los hallazgos R1, R2, R3, R6 y R7 se convirtieron en **reglas propias de Spectral** (tres en ese momento; la revisión de consistencia de IA-S6-03 llevó a agregar una cuarta), para que el control no dependa de repetir la revisión |
| Verificación | Cada hallazgo se contrastó con el archivo `openapi-v1-borrador.yaml` y con las salidas de Spectral y Redocly. Las reglas propias en `.spectral.yaml` dan 14 errores sobre v1 y 0 sobre la versión final |

### IA-S5-04 · Repetición de la revisión (reproducibilidad)

| Campo | Contenido |
|---|---|
| Prompt resumido | El mismo de IA-S5-03, en una sesión nueva e independiente sobre los mismos archivos de entrada (`openapi-v1-borrador.yaml`, `.feature` y escenarios) |
| Salida | 16 hallazgos |
| Defectos | Repitió el hallazgo parcialmente incorrecto sobre los contadores de intentos. De las 12 observaciones menores de la primera ejecución cubrió 10 (con 9 hallazgos, porque uno agrupa dos) y omitió 2; además agregó 1 nueva |
| Decisión | **Usar la medición:** C2 de la IA pasa de 2 (supuesto) a 3 (medido) en la matriz |
| Verificación | Comparación hallazgo por hallazgo con la primera ejecución: coinciden los 6 errores |

### IA-S6-01 · Código del esqueleto ejecutable

| Campo | Contenido |
|---|---|
| Prompt resumido | Implementar en FastAPI las 8 operaciones del contrato, respetando el monolito modular (ADR-003): filtro por emisor (E1), secuencial con bloqueo de fila y restricción única (ADR-002, E6), y adaptador del SRI simulado con 3 intentos (E2). Tomar de los stubs generados las rutas y los códigos de respuesta |
| Salida | Borrador inicial de `src/facturaec/` (11 módulos y el `__init__.py`) |
| Defectos | **(1) Secuencial duplicado bajo concurrencia:** la primera ejecución de CA5.3 contra PostgreSQL falló con `UniqueViolation`. El bloqueo de fila se pedía, pero SQLAlchemy reutilizaba el emisor ya cargado en la sesión con su secuencial viejo. Con SQLite la prueba se omite, así que el defecto habría pasado. **(2)** La API devolvía `"direccion": null` y el contrato declara un texto; lo detectó Prism en modo proxy. **(3)** Ruff dio 38 hallazgos (líneas largas, `Depends` en valores por defecto, nombres de excepciones y orden de imports) |
| Decisión | **Modificar:** `populate_existing=True` en la lectura con bloqueo; omitir los campos nulos opcionales; `Annotated` en las dependencias y excepciones renombradas |
| Verificación | 31 pruebas pasan contra PostgreSQL 16. **Prueba de mutación:** al quitar `with_for_update()`, CA5.3 falla, así que la prueba sí detecta la falta del bloqueo. Prism en modo proxy: 0 violaciones en 10 llamadas. Ruff: 0 hallazgos |

### IA-S6-02 · Pasos de las pruebas de aceptación BDD

| Campo | Contenido |
|---|---|
| Prompt resumido | Escribir las definiciones de pasos de pytest-bdd para los 25 escenarios y una prueba de conformidad contrato ↔ código |
| Salida | Borrador de `tests/step_defs/`, `tests/test_contrato.py` y `tests/test_documentacion.py` |
| Defectos | **(1)** La prueba de conformidad comparaba el contrato con un conjunto vacío: en FastAPI 0.162 las rutas incluidas ya no se listan directamente en `app.routes`. Se detectó porque la prueba falló. **(2)** La clave de las pruebas (18 bytes) era más corta que lo recomendado para HS256 (aviso de PyJWT) |
| Decisión | **Modificar:** comparar contra el esquema que FastAPI infiere del código (`get_openapi`) y alargar la clave de las pruebas |
| Verificación | Ejecución de `pytest` sin fallas: con SQLite 30 aprobadas y 1 omitida; con PostgreSQL 31 aprobadas. La validez de CA5.3 se comprobó con la prueba de mutación de IA-S6-01 |

### IA-S5-05 · ADR-005 y ajustes al ADR-004 y a la vista C2

| Campo | Contenido |
|---|---|
| Prompt resumido | Registrar como ADR la decisión de contrato API-first y pruebas BDD, con alternativas y consecuencias, y actualizar las referencias al contrato en el ADR-004 y en la vista C2 |
| Salida | Borrador de `docs/03-adr/adr-005-contrato-api-first-y-pruebas-bdd.md`, nota de modificación en el ADR-004 y párrafo del contrato en `c2-contenedores.md` |
| Defectos | El borrador afirmaba que behave soporta Gherkin en español como si se hubiera verificado; no se probó |
| Decisión | **Modificar:** se marcó como «según su documentación (no probado)», a diferencia de pytest-bdd, que sí se verificó |
| Verificación | Enlaces relativos comprobados; diagramas Mermaid validados con el analizador de Mermaid 11 |

### IA-S6-03 · Revisión cruzada de consistencia documental y de la matriz

| Campo | Contenido |
|---|---|
| Prompt resumido | Revisar la consistencia entre la matriz de selección (`docs/08`), el mapa de toolchain (`docs/06`), el informe y la rúbrica de la actividad, buscando discrepancias en cifras, rúbricas o identificadores |
| Salida | Listado de 20 observaciones de consistencia (4 principales sobre la matriz y cifras, y 16 menores) |
| Defectos | **Principales detectados en los borradores:** (1) seis puntajes de la matriz no seguían exactamente el nivel de su propia rúbrica (por ejemplo, Spectral C1 = 2 cuando la justificación correspondía a «solo estilo», es decir, 1); (2) se marcaba como seleccionada la IA, que es de pago, aunque el costo cero era requisito obligatorio; (3) se afirmaba que los 18 hallazgos de la IA eran reales cuando uno era parcialmente correcto; (4) imprecisión al describir el nivel de hilos de la prueba de concurrencia. **Menores:** la regla de operaciones públicas no impedía que otra operación se declarara pública; la escala de riesgo no coincidía con los valores asignados, y los dos códigos 409 del contrato compartían el mismo ejemplo |
| Decisión | **Modificar:** el equipo reasignó los puntajes siguiendo estrictamente la rúbrica. La base quedó en empate entre Spectral y Redocly (3,70), resuelto por el requisito obligatorio de la actividad, y la IA en 2,80 como complemento opcional fuera de la cadena obligatoria. Se precisaron las cifras de concurrencia, se agregó una cuarta regla propia con su prueba negativa, se separaron los dos 409 del contrato y se corrigieron los ejemplos |
| Verificación | Ejecución de linter y pruebas sin fallas tras los cambios; recálculo de la matriz con un script y revisión completa de los documentos del repositorio |

### Evaluación crítica

- **Donde más aportó la IA:** la revisión semántica del contrato. Encontró los dos errores más graves, que los linters no podían ver porque el archivo era sintácticamente válido. Además, sus hallazgos se pudieron convertir en reglas automáticas de Spectral.
- **Donde más falló:** el código inicial que generó tenía un defecto de concurrencia que no se ve leyendo el código ni probando con SQLite. Lo detectó una prueba contra PostgreSQL, escrita a partir del criterio de E6. Esto confirma la regla de la sesión: a mayor riesgo, más supervisión del equipo y ejecución real.
- **Riesgo principal observado:** que una prueba generada con asistencia de IA pase sin probar nada. Se mitigó con la prueba de mutación y con una implementación independiente del módulo 11 en la prueba.
- **Decisiones propias del equipo:** el alcance del hito (E8, el XML firmado y el frontend quedan en el backlog), la definición de los pesos de la matriz y la selección final de herramientas.
