# 08 · Matriz de evaluación y selección de herramientas (ISO/IEC 14102)

> Proyecto **FacturaEC** · Módulo 8 · Semana 2 · versión v0.2.0.
> Referencia: ISO/IEC 14102:2008, guía para evaluar y seleccionar herramientas CASE. Se siguen sus cuatro pasos: definir requisitos, evaluar capacidades, comparar opciones y tomar la decisión.

## 1. Definir requisitos: qué función se evalúa y por qué

Se evalúa la función **revisar y validar el contrato OpenAPI** (tarea **T4**, puntaje 64, prioridad Alta, [`06-mapa-toolchain.md`](06-mapa-toolchain.md)). Se eligió esta función por tres razones:

1. Es la puerta de la cadena: si el contrato está mal, la documentación, el mock, los stubs y las pruebas heredan el error (ADR-005).
2. Admite alternativas comparables, incluida una de IA, que reciben **la misma entrada** y producen hallazgos que se pueden contar y verificar.
3. Las tres alternativas se probaron sobre el mismo archivo: el borrador v1 de `api/openapi.yaml`, guardado en `docs/evidencias/openapi-v1-borrador.yaml`.

Requisitos de la organización (equipo de 4 estudiantes, R2 y R5 del dossier):

| ID | Requisito | Tipo |
|---|---|---|
| RQ1 | La actividad exige validar el contrato con Spectral sin errores | Obligatorio |
| RQ2 | Detectar defectos que rompan los criterios de E1 y E2 | Evaluado (C1) |
| RQ3 | Poder bloquear la generación (y, en la sesión 10, el pipeline) con un código de salida | Evaluado (C3) |
| RQ4 | Costo cero para las herramientas **obligatorias** de la cadena (R2) | Obligatorio |
| RQ5 | No enviar a terceros datos del proyecto sin necesidad | Evaluado (C6) |

| Alternativa | Tipo | Versión probada | Licencia |
|---|---|---|---|
| Spectral (Stoplight) | Linter de reglas, conjunto `spectral:oas` | 6.17.0 | Apache-2.0 |
| Redocly CLI | Linter de reglas, conjunto `recommended` | 2.71.0 | MIT |
| Claude Opus 5.5 (Anthropic), como revisor | **Herramienta de IA**, revisión en lenguaje natural | `claude-opus-5-5` | Servicio comercial |

## 2. Evaluar capacidades: criterios, pesos y rúbrica

Los criterios siguen las características de calidad que propone ISO/IEC 14102 (funcionalidad, fiabilidad, usabilidad e integración) y los aspectos generales de adquisición (costo, proveedor y riesgo). Los pesos suman 100 y reflejan la prioridad del equipo: lo que más importa es detectar defectos que rompan los criterios.

| ID | Criterio | Característica | Peso | Cómo se mide en la prueba |
|---|---|---|---|---|
| C1 | Capacidad de detección sobre el contrato de FacturaEC | Funcionalidad | 30 | Hallazgos válidos en el borrador v1, en especial los que rompen criterios de aceptación |
| C2 | Fiabilidad y reproducibilidad | Fiabilidad | 20 | Mismo resultado en ejecuciones repetidas; hallazgos incorrectos |
| C3 | Integración en la cadena | Integración y portabilidad | 20 | CLI, código de salida para bloquear, reglas propias configurables, formatos abiertos |
| C4 | Facilidad de adopción | Usabilidad | 10 | Pasos de instalación y configuración hasta el primer resultado útil |
| C5 | Costo y licencia | Adquisición | 10 | Precio y licencia para un equipo estudiantil |
| C6 | Riesgo de uso y privacidad | Proveedor y seguridad | 10 | Qué datos salen del equipo y riesgo de confiar sin verificar |
| | **Total** | | **100** | |

| Criterio | 5 (mejor) | 3 (intermedio) | 1 (peor) |
|---|---|---|---|
| C1 | Detecta los defectos que rompen criterios de aceptación | Detecta parte, o solo defectos genéricos | Solo estilo, o nada |
| C2 | Determinista, sin hallazgos incorrectos | Mayormente estable, con algún falso positivo | Resultado distinto en cada ejecución o con errores frecuentes |
| C3 | CLI con código de salida y reglas propias probadas | CLI con código de salida; reglas propias no probadas | Sin CLI ni código de salida |
| C4 | Un comando de instalación y uno de ejecución | Requiere configuración o redactar instrucciones | Requiere infraestructura o capacitación |
| C5 | Libre y gratuita | Gratuita con límites | De pago |
| C6 | Se ejecuta en local y no envía datos | Envía telemetría que se puede desactivar | Envía el artefacto a un tercero y exige verificar cada salida |

Los valores 2 y 4 se usan solo cuando la alternativa queda claramente entre dos descripciones. Cada puntaje de la sección 3 cita el nivel de la rúbrica que le corresponde.

## 3. Comparar opciones: matriz ponderada

Total = Σ(peso × puntaje) / 100.

| Criterio | Peso | Spectral | Redocly CLI | Claude Opus 5.5 (IA) |
|---|---|---|---|---|
| C1 Detección | 30 | 1 | 3 | 5 |
| C2 Fiabilidad | 20 | 5 | 5 | 3 |
| C3 Integración | 20 | 5 | 3 | 1 |
| C4 Adopción | 10 | 4 | 4 | 3 |
| C5 Costo | 10 | 5 | 5 | 1 |
| C6 Riesgo de uso | 10 | 5 | 3 | 1 |
| **Total ponderado (sobre 5)** | **100** | **3,70** | **3,70** | **2,80** |

Cálculo de Spectral: 30·1 + 20·5 + 20·5 + 10·4 + 10·5 + 10·5 = 370 → 3,70. Cálculo de Redocly: 30·3 + 20·5 + 20·3 + 10·4 + 10·5 + 10·3 = 370 → 3,70.

### 3.1 Justificación observable de cada puntaje

| Criterio | Spectral | Redocly CLI | Claude Opus 5.5 |
|---|---|---|---|
| C1 | **1 (solo estilo):** 17 advertencias en v1, todas de estilo o metadatos (falta `description`, `operationId`, etiquetas o `contact`). No detectó el `security` heredado en el registro y en `/health` (R1, R2), que rompía CA1.1, ni la falta de 401, 409 y 422 | **3 (detecta parte):** 8 advertencias. Además de metadatos, marcó 5 operaciones sin ninguna respuesta 4xx, un aviso genérico que cubre en parte R3 a R8 sin indicar qué código falta. Tampoco vio R1 ni R2 | **5 (detecta los que rompen criterios):** 18 hallazgos; 17 resultaron reales y 1 parcialmente correcto (R15, que se evalúa en C2). Incluyen R1 y R2, los más graves, y los faltantes ligados a criterios: 401 (CA2.3), 409 (CA6.4) y 422 (CA3.2) |
| C2 | **5 (determinista):** el mismo resultado en todas las ejecuciones de la semana; la versión final da 0 hallazgos en cada corrida | **5 (determinista):** igual | **3 (mayormente estable, con algún falso positivo):** se midió con dos ejecuciones independientes en sesiones separadas con el mismo prompt. Coincidieron los 6 errores; las observaciones menores variaron (18 hallazgos en la primera, 16 en la segunda), y las dos repitieron el mismo hallazgo parcialmente incorrecto |
| C3 | **5 (reglas propias probadas):** CLI con código de salida (0 o 1). Cuatro reglas propias en `.spectral.yaml` dan 14 errores sobre v1 y 0 sobre la versión final; una prueba negativa (volver pública una operación protegida) hace fallar la regla correspondiente | **3 (reglas propias no probadas):** CLI con código de salida y archivo de excepciones; admite reglas propias, pero no se probaron | **1 (sin código de salida):** en la prueba se usó mediante su interfaz conversacional web, sin código de salida ni reglas; su resultado lo lee una persona |
| C4 | **4:** `npm install -g` y un comando, pero exige un archivo de reglas (`.spectral.yaml`) para ejecutarse | **4:** se ejecuta sin configurar, pero hubo que desactivar una regla (servidor `localhost`) y justificar una excepción (`/health`) | **3 (requiere redactar instrucciones):** redactar el prompt, entregar el contexto (criterios y escenarios) y verificar uno por uno los hallazgos |
| C5 | **5 (libre y gratuita):** Apache-2.0 | **5 (libre y gratuita):** MIT | **1 (de pago):** servicio comercial, con dependencia del proveedor |
| C6 | **5 (local, no envía datos):** se ejecuta en local y no envía el contrato | **3 (telemetría desactivable):** se ejecuta en local, pero envía telemetría de uso por defecto y se desactivó con `telemetry: off` en `redocly.yaml` | **1 (el artefacto sale a un tercero):** el contrato se envía a un servicio externo (sin datos personales ni credenciales, como exige la actividad) y cada hallazgo exige verificación humana |

### 3.2 Sensibilidad de los pesos

| Variante de pesos (C1 · C2 · C3 · C4 · C5 · C6) | Spectral | Redocly CLI | Claude Opus 5.5 |
|---|---|---|---|
| Base (30 · 20 · 20 · 10 · 10 · 10) | **3,70** | **3,70** | 2,80 |
| La detección pesa más (50 · 15 · 15 · 10 · 5 · 5) | 2,90 | **3,50** | **3,50** |
| Pesos iguales (≈16,7 cada uno) | **4,17** | 3,83 | 2,33 |
| Fiabilidad e integración pesan más (20 · 30 · 30 · 10 · 5 · 5) | **4,10** | 3,80 | 2,60 |

**Lectura.** Con los pesos base, **Spectral y Redocly empatan**. De las otras tres variantes de pesos, Spectral gana dos (pesos iguales; fiabilidad e integración). Cuando la detección pesa la mitad, Spectral queda último (2,90), y Redocly y la IA empatan (3,50). Esto muestra la debilidad central de Spectral sola: con su conjunto estándar solo detecta estilo. No se recalcula C1 de Spectral con las reglas propias, porque esas reglas se escribieron a partir de defectos ya conocidos y medir con ellas sería circular. Su valor se refleja en C3 (configurabilidad probada), no en C1.

## 4. Tomar la decisión: selección y riesgos

**Regla de desempate (declarada antes de decidir).** Ante un empate en el total, decide primero un requisito obligatorio (RQ1 y RQ4) y, si persiste, el criterio de mayor peso en el que difieran las alternativas empatadas. RQ1 exige Spectral, así que el empate de la base se resuelve a su favor sin usar el segundo paso.

| Herramienta | Decisión | Rol en la cadena |
|---|---|---|
| **Spectral** con `.spectral.yaml` (conjunto `spectral:oas` + 4 reglas propias) | **Seleccionada** (empate en la base, resuelto por RQ1; gana en 2 de las 3 variantes de pesos) | Validación obligatoria: no se genera documentación, mock ni stubs si reporta errores. En la sesión 10 será un paso del pipeline de CI. Su debilidad en detección (C1 = 1) se mitiga con las reglas propias y con la revisión semántica |
| **Redocly CLI** | **No seleccionada** | Empata con Spectral, pero RQ1 ya obliga a Spectral. Su aporte diferencial sobre Spectral (el aviso genérico de 4xx) queda cubierto por las reglas propias, más precisas porque indican qué código falta (401 o 422). Además envía telemetría por defecto. Se conserva `redocly.yaml` por si el equipo necesita su función de empaquetado |
| **Claude Opus 5.5** como revisor | **No forma parte de la cadena obligatoria**; se usa como **complemento opcional** | Tiene el total más bajo (2,80) y es de pago, lo que incumple RQ4 para una herramienta obligatoria. Pero fue la única que detectó R1 y R2. Por eso, en cada cambio mayor del contrato, el equipo puede usarla como revisión semántica previa a la revisión cruzada humana (T9). Si no hay acceso a la IA, la sustituye la revisión cruzada con la rúbrica de la plantilla de pull request. Cada hallazgo se verifica antes de aceptarlo, y cada hallazgo recurrente se convierte en una regla de Spectral |

### 4.1 Riesgos de la selección y mitigación

| Riesgo | Herramienta | Mitigación |
|---|---|---|
| Un contrato sintácticamente válido pasa el linter aunque rompa un criterio, como pasó con R1 y R2 (C1 = 1) | Spectral | Reglas propias para los defectos ya conocidos; pruebas de conformidad (`tests/test_contrato.py`); Prism en modo proxy contra la API real; revisión semántica (IA o humana) en los cambios mayores |
| Defectos nuevos, distintos de los que cubren las reglas propias | Spectral | Revisión cruzada (T9) con la rúbrica; cada defecto nuevo que se repita se convierte en regla |
| Aceptar un hallazgo plausible pero incorrecto (como R15) | Claude | Tabla de verificación por hallazgo en `docs/04-registro-ia.md`: aceptar, modificar o rechazar, con evidencia |
| Exponer información al servicio de IA | Claude | Solo se comparten el contrato, los criterios y los escenarios. Nunca credenciales, certificados, RUC reales ni datos de clientes (LOPDP) |
| Depender de un proveedor de pago para un control obligatorio | Claude | La IA no es puerta de la cadena ni herramienta obligatoria; la puerta es Spectral, que es gratuita y corre en local |
| Reglas propias desactualizadas cuando cambie el contrato | Spectral | Las reglas viven en el repositorio, se revisan en cada pull request y se prueban contra el borrador v1 (`docs/evidencias/openapi-v1-borrador.yaml`) |

## 5. Otras herramientas de la cadena

Las demás herramientas no compiten entre sí en esta semana: cada una es la única candidata de su fase, elegida por el stack (ADR-001, ADR-005) o por la práctica del módulo. Todas son gratuitas y de código abierto (RQ4). Su resultado se registró en la sección 6 de `06-mapa-toolchain.md`.

| Herramienta | Fase | Resultado de la prueba | Decisión |
|---|---|---|---|
| OpenAPI Generator 7.26.0 | Construir | Genera stubs que arrancan, pero que no entregan el token ni implementan nada | Se usa para la documentación HTML y como referencia de forma; la implementación va en `src/` (ADR-005) |
| Prism 5.14.2 | Diseñar y probar | Mock útil para el frontend; en modo proxy detectó una violación real del contrato | Seleccionada |
| pytest + pytest-bdd | Probar | Ejecuta el Gherkin en español; detectó un defecto real de concurrencia | Seleccionada (ADR-005) |
| Ruff 0.17.2 | Probar | 38 hallazgos en la primera ejecución, corregidos | Seleccionada |
| GitHub (Issues, Projects y pull requests) | Analizar e integrar | Candidata asignada en el mapa (`T2` y `T9`, prioridad Media); se incluye la plantilla de revisión `.github/pull_request_template.md` | Seleccionada para el flujo colaborativo |
