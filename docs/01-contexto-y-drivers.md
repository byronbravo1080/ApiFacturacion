# 01 · Contexto del caso y drivers arquitectónicos

> Proyecto: **FacturaEC** — sistema web de facturación electrónica para pequeñas empresas de Ecuador.
> Módulo 8 · Automatización de procesos de software · Maestría en Ingeniería en Software (UPEC).
> Versión del documento: v0.1.0 (hito H1).

## 1. Contexto del caso

### 1.1 Problema
Los pequeños negocios ecuatorianos están obligados a emitir comprobantes electrónicos autorizados por el SRI. Las soluciones comerciales suelen ser costosas o demasiado complejas para un negocio que emite pocas facturas al mes, y emitir comprobantes con formato, firma o numeración incorrectos genera rechazos y riesgos tributarios.

### 1.2 Propuesta
Una aplicación web donde el negocio registra clientes y productos, emite facturas y las envía al SRI para su autorización; luego consulta el estado y descarga el RIDE (PDF) y el XML.

### 1.3 Alcance de la primera versión del sistema

| Dentro del alcance | Fuera del alcance (evolución) |
|---|---|
| Factura (código de documento `01`) con IVA | Notas de crédito/débito, retenciones, guías de remisión |
| Un emisor por cuenta, un usuario administrador | Multiusuario con roles, multiempresa |
| Generación de clave de acceso (49 dígitos, módulo 11) y XML | Firma XAdES-BES con certificado `.p12` |
| Envío al SRI mediante un adaptador **simulado** | Adaptador real contra el ambiente de pruebas del SRI |
| API REST, base de datos relacional, RIDE en PDF | Facturación recurrente, reportes contables, envío por correo |

> **Alcance de este repositorio (v0.1.0, hito H1):** contiene el dossier de arquitectura. El código del backend y del frontend se incorporará en hitos posteriores.

### 1.4 Supuestos
- El ambiente objetivo del SRI es **pruebas** (`ambiente = 1`).
- Los códigos de porcentaje de IVA y el esquema del XML deben contrastarse con la ficha técnica del SRI vigente antes de pasar a producción.
- La obtención del certificado de firma electrónica y de un RUC habilitado para pruebas puede exceder el plazo del hito H1 (supuesto a confirmar por el equipo).

## 2. Stakeholders y concerns

Los concerns se redactan como necesidades o preocupaciones, no como soluciones.

| ID | Stakeholder | Concerns |
|---|---|---|
| S1 | Dueño/administrador de una pequeña empresa (usuario principal) | Emitir facturas válidas sin conocimientos tributarios ni técnicos; no perder comprobantes ya emitidos; que sus datos no sean visibles para otros negocios; costo bajo |
| S2 | Contador externo | Consultar el estado de autorización de cada comprobante; disponer de los XML y RIDE para la declaración de impuestos |
| S3 | SRI (regulador y sistema externo) | Que cada comprobante cumpla formato, numeración, clave de acceso y firma; que no se dupliquen números de comprobante |
| S4 | Equipo de desarrollo (4 integrantes) | Poder evolucionar el sistema sin reescribirlo; probar y desplegar con poco esfuerzo; repartir el trabajo sin bloquearse |
| S5 | Docente/evaluador | Trazabilidad entre drivers, escenarios, vistas y decisiones; evidencia verificable y versionada |
| S6 | Cliente final (comprador) | Recibir un comprobante legible y verificable |

## 3. Restricciones

| ID | Restricción | Origen | Negociabilidad |
|---|---|---|---|
| R1 | Cumplir la normativa y fichas técnicas de comprobantes electrónicos del SRI | Regulatorio | No negociable |
| R2 | Costo de infraestructura cero o casi cero | Económico/académico (equipo estudiantil) | Poco negociable: se aceptan las limitaciones de los planes gratuitos |
| R3 | Entrega del dossier el 18/10/2026 a las 23:55 (hito H1) | Académico | No negociable |
| R4 | Tecnologías disponibles en el equipo: .NET, FastAPI, Angular, Next.js | Organizacional | Negociable (ver ADR-001) |
| R5 | La arquitectura debe incluir una API con al menos 4 endpoints, un frontend y una base de datos, y quedar preparada para CI/CD | Académico (Módulo 8) | No negociable |
| R6 | Obtención del certificado de firma y RUC de pruebas puede no estar lista a tiempo | Externo/administrativo | Parcialmente negociable: se simula el SRI (ver ADR-003) |
| R7 | Backend y documentación en un repositorio; frontend en otro | Decisión del equipo | Negociable (ver ADR-004) |

## 4. Drivers arquitectónicos priorizados

Se eligen cinco drivers: los concerns, restricciones y atributos que más condicionan la arquitectura. **Importancia** (para el negocio y el evaluador) y **dificultad** (esfuerzo o riesgo técnico) se expresan como Alta / Media / Baja. Los tipos de atributo siguen la nomenclatura de ISO/IEC 25010:2023. Cada driver se vincula a un stakeholder o restricción y se verifica con al menos un escenario de calidad (sección 5).

| ID | Driver | Vinculado a | Importancia | Dificultad | Escenario |
|---|---|---|---|---|---|
| D1 | Cumplimiento del formato y numeración íntegra exigidos por el SRI (clave de acceso, XML, secuenciales sin duplicados ni saltos) | R1, S3 | Alta | Alta | E6 |
| D2 | Tolerancia a la indisponibilidad o lentitud del SRI sin perder comprobantes | S1, S3 | Alta | Media | E2, E8 |
| D3 | Aislamiento y confidencialidad de los datos de cada emisor | S1, S2 | Alta | Media | E1 |
| D4 | Operación sostenible por un equipo pequeño: costo de infraestructura cero, despliegue automatizado y cambio barato | R2, R5, S4 | Alta | Media | E5, E4 |
| D5 | Experiencia del usuario principal: respuesta ágil y uso sin formación técnica | S1 | Media | Media | E3, E7 |

### 4.1 Orden de atención
1. **Alta importancia / alta dificultad** (D1): se mitiga aislando al SRI detrás de un adaptador (ADR-003) y asignando los secuenciales con restricción única en la base de datos (ADR-002).
2. **Alta importancia / dificultad media** (D2, D3, D4): condicionan el estilo arquitectónico, la base de datos y la organización del código (ADR-001 a ADR-004).
3. **Media importancia** (D5): se atiende dentro del diseño modular sin decisiones propias.

## 5. Escenarios de calidad

Cada escenario tiene las **seis partes** (fuente, estímulo, artefacto, entorno, respuesta y medida de respuesta), un **solo atributo** de calidad y una **medida numérica comprobable**. E1 a E7 se definen en la Parte I; E8 se incorpora en la Parte III (sección 6).

### E1 · Confidencialidad: aislamiento entre emisores (D3)

| Parte | Descripción |
|---|---|
| Fuente | Usuario autenticado de un emisor, o un tercero sin autenticar |
| Estímulo | Solicita facturas, clientes o productos que no le pertenecen, o consulta sin token |
| Artefacto | API REST (todos los endpoints protegidos) |
| Entorno | Operación normal, dos o más emisores registrados |
| Respuesta | La API rechaza la solicitud sin revelar la existencia del recurso |
| Medida | 401 en el 100 % de las solicitudes sin token válido; 404 en el 100 % de las solicitudes a recursos de otro emisor; 0 campos de otro emisor en las respuestas |

*Verificación:* pruebas automáticas de acceso sin token y de aislamiento entre dos emisores, en el código del backend (a incluir en el repositorio en el hito H2). Un prototipo ya las ejecuta; ver [registro de IA](04-registro-ia.md).

### E2 · Fiabilidad: indisponibilidad del SRI (D2)

| Parte | Descripción |
|---|---|
| Fuente | Servicio del SRI (sistema externo) |
| Estímulo | No responde o falla al recibir un comprobante |
| Artefacto | Módulo Comprobantes / adaptador `SriGateway` |
| Entorno | Operación normal, factura creada y pendiente de envío |
| Respuesta | La factura se conserva en estado PENDIENTE, se reintenta con espera exponencial y la API informa al usuario que quedó en cola |
| Medida | 0 facturas perdidas (100 % conservadas); hasta 3 intentos por solicitud (esperas de 1 s y 2 s); respuesta HTTP 202 en ≤ 60 s; el reenvío posterior, con el SRI restablecido, autoriza la factura en 1 solicitud |

*Verificación:* prueba automática que simula la caída del SRI y comprueba el estado PENDIENTE, los 3 intentos y la autorización posterior, en el código del backend (hito H2; un prototipo ya la ejecuta). *Evolución:* worker en segundo plano para reintentos diferidos.

### E3 · Eficiencia de desempeño: emisión con carga pequeña (D5)

| Parte | Descripción |
|---|---|
| Fuente | 20 usuarios concurrentes de uno o varios emisores |
| Estímulo | Crean facturas de hasta 10 líneas simultáneamente |
| Artefacto | Endpoint `POST /api/v1/facturas` |
| Entorno | Instancia en ejecución (sin arranque en frío) y base de datos PostgreSQL gestionada |
| Respuesta | La API crea la factura, calcula totales, asigna secuencial y genera el XML |
| Medida | Percentil 95 de latencia < 800 ms, excluyendo la llamada al SRI; 0 errores 5xx |

*Verificación:* prueba de carga (k6 o Locust) planificada para el hito H2; objetivo aún no medido.

### E4 · Mantenibilidad: nuevo tipo de comprobante (D4)

| Parte | Descripción |
|---|---|
| Fuente | Equipo de desarrollo |
| Estímulo | Debe agregar la nota de crédito (código `04`) |
| Artefacto | Módulos de facturación y comprobantes del backend |
| Entorno | Tiempo de desarrollo, con el código base de la primera versión del backend |
| Respuesta | Se incorpora el nuevo documento reutilizando clave de acceso, adaptador del SRI y RIDE |
| Medida | ≤ 2 días-persona de esfuerzo; 0 cambios en los módulos de autenticación, clientes y productos; ≥ 80 % de las pruebas existentes siguen pasando sin modificación |

*Verificación:* estimación con revisión de código al implementarlo (hito H2).

### E5 · Flexibilidad: despliegue automatizado (D4)

| Parte | Descripción |
|---|---|
| Fuente | Integrante del equipo |
| Estímulo | Fusiona un cambio en la rama `main` |
| Artefacto | Pipeline de CI/CD y repositorios backend y frontend |
| Entorno | Servicios con plan gratuito (Render/Vercel/Supabase o Neon) |
| Respuesta | El pipeline ejecuta pruebas, construye y despliega sin pasos manuales |
| Medida | ≤ 10 minutos desde la fusión hasta el despliegue disponible; 0 pasos manuales; costo mensual de infraestructura = USD 0 |

*Verificación:* ejecución del pipeline en el hito H2 (la primera versión del backend incluirá un `Dockerfile` y la estructura de repositorios lista para el pipeline).

### E6 · Integridad: numeración secuencial (D1)

| Parte | Descripción |
|---|---|
| Fuente | Múltiples solicitudes de emisión concurrentes del mismo emisor |
| Estímulo | Crean facturas al mismo tiempo en el mismo establecimiento y punto de emisión |
| Artefacto | Módulo de facturación y tabla `factura` |
| Entorno | Operación normal sobre PostgreSQL |
| Respuesta | Cada factura recibe un secuencial distinto y consecutivo |
| Medida | 0 secuenciales duplicados y 0 saltos en 1000 solicitudes concurrentes |

*Verificación:* prueba secuencial de 30 facturas consecutivas (prototipo) y restricción única por emisor, establecimiento, punto de emisión y secuencial en el modelo de datos. La prueba concurrente de 1000 solicitudes contra PostgreSQL se ejecutará en CI (hito H2).

### E7 · Capacidad de interacción: primera factura (D5)

| Parte | Descripción |
|---|---|
| Fuente | Dueño de un pequeño negocio sin formación técnica |
| Estímulo | Quiere emitir su primera factura |
| Artefacto | Aplicación web |
| Entorno | Cuenta ya registrada, cliente y producto cargados |
| Respuesta | El usuario completa la emisión guiado por la interfaz |
| Medida | ≤ 3 minutos desde el inicio de sesión hasta la factura creada, con ≥ 4 de 5 usuarios de prueba sin ayuda externa |

*Verificación:* prueba de usabilidad con el frontend (hito H2).

## 6. Parte III · Escenario nuevo E8 y priorización

Al comparar estilos aparece un riesgo que faltaba: en un monolito, la lentitud del SRI (no su caída) puede retener los procesos de la API y degradar todas las operaciones. E2 cubre la caída; E8 cubre la lentitud.

### E8 · Fiabilidad: lentitud del SRI sin degradar el resto de la API (D2)

| Parte | Descripción |
|---|---|
| Fuente | Servicio del SRI (sistema externo) |
| Estímulo | Responde con mucha lentitud (más de 15 s) o deja la conexión abierta durante varios envíos seguidos |
| Artefacto | API REST (adaptador `SriGateway`) |
| Entorno | Operación normal con carga pequeña (20 usuarios) y una sola instancia de la API en plan gratuito |
| Respuesta | El adaptador corta cada intento por tiempo de espera, la factura queda PENDIENTE y el resto de las operaciones (listar, crear facturas, descargar RIDE) siguen respondiendo |
| Medida | Tiempo de espera ≤ 15 s por intento; percentil 95 < 800 ms en las operaciones que no llaman al SRI mientras el SRI está lento; 0 facturas perdidas |

*Verificación:* prueba con un adaptador simulado que introduce retardo (hito H2); objetivo aún no medido. Si no se cumple, la mitigación prevista es trasladar los reintentos a un proceso en segundo plano.

### Priorización

| Prioridad | Escenario | Atributo | Driver | Importancia | Dificultad |
|---|---|---|---|---|---|
| 1 | E2 | Fiabilidad (tolerancia a fallos) | D2 | Alta | Media |
| 2 | E6 | Seguridad (integridad) | D1 | Alta | Alta |
| 3 | E1 | Seguridad (confidencialidad) | D3 | Alta | Media |
| 4 | E8 | Fiabilidad (aislamiento ante lentitud) | D2 | Alta | Media |
| 5 | E5 | Flexibilidad (instalabilidad/despliegue) | D4 | Alta | Baja |
| 6 | E4 | Mantenibilidad (modificabilidad) | D4 | Media | Media |
| 7 | E7 | Capacidad de interacción (usabilidad) | D5 | Media | Media |
| 8 | E3 | Eficiencia de desempeño | D5 | Media | Baja |

## 7. Alternativas de estilo

| ID | Alternativa | Descripción | Costo operativo |
|---|---|---|---|
| A1 | Monolito modular | Un solo despliegue de la API, con módulos de fronteras claras (routers, servicios) y la integración del SRI aislada tras el puerto `SriGateway` | Bajo: un despliegue y un servicio que vigilar |
| A2 | Microservicios | Servicios separados (autenticación, facturación, comprobantes/SRI), cada uno con su despliegue y posiblemente su base de datos | Alto: varios despliegues, red entre servicios y trazabilidad distribuida |
| A3 | Monolito en capas | Un solo despliegue con capas técnicas (controladores, lógica, datos), sin fronteras por funcionalidad ni adaptador explícito del SRI | Bajo: un despliegue, pero con acoplamiento interno |

## 8. Criterios y pesos

Los criterios se derivan de los escenarios y las restricciones. Los pesos suman 100 y reflejan la priorización de la sección 6. Cada criterio se califica de 1 (peor) a 5 (mejor) con la rúbrica de la sección 9.

| Criterio | Origen | Peso | Cómo se evalúa |
|---|---|---|---|
| 1. Confidencialidad entre emisores | E1 · D3 | 15 | Puntos de control de acceso y superficie expuesta |
| 2. Fiabilidad ante caída o lentitud del SRI | E2, E8 · D2 | 20 | Aislamiento del fallo y conservación de la factura |
| 3. Desempeño | E3 · D5 | 10 | Latencia esperada con 20 usuarios |
| 4. Modificabilidad | E4 · D4 | 15 | Piezas que cambian al agregar un comprobante |
| 5. Despliegue y costo cero | E5 · D4 · R2 | 20 | Despliegues, pipelines y encaje en planes gratuitos |
| 6. Integridad de la numeración | E6 · D1 · R1 | 15 | Capacidad de garantizar 0 duplicados con poca complejidad |
| 7. Usabilidad | E7 · D5 | 5 | Efecto del estilo sobre la experiencia de uso |
| **Total** | | **100** | |

## 9. Rúbrica de calificación (1 a 5)

Los valores 2 y 4 se usan cuando la alternativa queda entre dos descripciones.

| Criterio | 5 (mejor) | 3 (intermedio) | 1 (peor) |
|---|---|---|---|
| 1. Confidencialidad (E1) | Un solo punto de autenticación y de filtrado por emisor, sin superficie adicional | Autenticación y filtrado repartidos en varias piezas que hay que coordinar | Cada parte controla el acceso por su cuenta |
| 2. Fiabilidad ante el SRI (E2, E8) | El fallo o la lentitud del SRI queda aislado en una pieza independiente con su cola; el resto no se afecta | El fallo se contiene en un adaptador, pero comparte proceso con el resto; hay que acotar tiempos y reintentos | El fallo del SRI se propaga por el código y puede perder o bloquear facturas |
| 3. Desempeño (E3) | Llamadas en proceso y mucha holgura frente a 800 ms | Cumple justo o requiere ajustes | No cumple el tiempo pedido |
| 4. Modificabilidad (E4) | Agregar un comprobante toca una sola pieza independiente | El cambio se acota a un módulo, pero con coordinación | El cambio atraviesa varias capas |
| 5. Despliegue y costo cero (E5) | Un contenedor, un pipeline y plan gratuito | Dos o tres piezas por desplegar, posibles con esfuerzo en planes gratuitos | Varios servicios, pipelines y límites de planes gratuitos que el equipo no puede sostener |
| 6. Integridad de la numeración (E6) | Una transacción local con restricción única | Requiere coordinar varias piezas o un servicio único de numeración | No hay forma de impedir duplicados |
| 7. Usabilidad (E7) | El estilo facilita respuestas rápidas y simples de consumir | Neutral: depende del frontend | Impone esperas o flujos que degradan la experiencia |

## 10. Matriz ponderada y justificación

Total = Σ(peso × puntaje) / 100.

| Criterio | Peso | A1 Monolito modular | A2 Microservicios | A3 Monolito en capas |
|---|---|---|---|---|
| 1. Confidencialidad (E1) | 15 | 4 | 3 | 4 |
| 2. Fiabilidad ante el SRI (E2, E8) | 20 | 4 | 5 | 3 |
| 3. Desempeño (E3) | 10 | 5 | 3 | 5 |
| 4. Modificabilidad (E4) | 15 | 4 | 5 | 2 |
| 5. Despliegue y costo cero (E5) | 20 | 5 | 1 | 5 |
| 6. Integridad de la numeración (E6) | 15 | 5 | 3 | 5 |
| 7. Usabilidad (E7) | 5 | 3 | 3 | 3 |
| **Total ponderado (sobre 5)** | **100** | **4,40** | **3,30** | **3,90** |

Cálculo de A1: 15·4 + 20·4 + 10·5 + 15·4 + 20·5 + 15·5 + 5·3 = 440 → 4,40.

| Criterio | A1 Monolito modular | A2 Microservicios | A3 Monolito en capas |
|---|---|---|---|
| 1. Confidencialidad | 4: un único límite de autenticación y un solo punto de filtrado por emisor | 3: más superficie expuesta y autenticación entre servicios | 4: igual que A1 |
| 2. Fiabilidad ante el SRI | 4: el adaptador `SriGateway` aísla el fallo y conserva la factura; ante la lentitud (E8) comparte proceso con el resto, por eso no llega a 5 | 5: un servicio dedicado al SRI con su cola aísla totalmente el fallo y la lentitud | 3: sin adaptador explícito, el fallo se propaga por el código |
| 3. Desempeño | 5: llamadas en proceso, sin saltos de red | 3: saltos de red entre servicios | 5: igual que A1 |
| 4. Modificabilidad | 4: las fronteras de módulo acotan el cambio | 5: servicios independientes | 2: sin fronteras, un cambio toca varias capas |
| 5. Despliegue y costo cero | 5: un contenedor, un pipeline, plan gratuito | 1: varios servicios que desplegar, más pipelines y límites de planes gratuitos | 5: igual que A1 |
| 6. Integridad | 5: una transacción local con bloqueo de fila y restricción única | 3: consistencia entre servicios o un servicio único de numeración | 5: igual que A1 |
| 7. Usabilidad | 3: neutral (depende del frontend) | 3: neutral | 3: neutral |

Los puntajes son juicios del equipo, no mediciones; deben revisarse cuando se ejecuten las pruebas de E3, E5, E6 y E8 en el hito H2.

## 11. Trade-offs y sensibilidad

### 11.1 Trade-off

- **Lo que se gana con A1:** despliegue simple y gratuito (E5), consistencia transaccional de la numeración (E6) y mejor desempeño (E3).
- **Lo que se sacrifica frente a A2:** parte del aislamiento de fallos (criterio 2: 4 frente a 5) y de la modificabilidad (criterio 4: 4 frente a 5).
- **Por qué es aceptable:** con infraestructura gratuita y un equipo de 4 personas, el costo operativo de los microservicios (criterio 5 = 1) supera el beneficio que aportan en fiabilidad y modificabilidad. El adaptador del SRI recupera gran parte del aislamiento.
- **Frente a A3:** el estilo modular cuesta lo mismo en despliegue, pero mejora los criterios 2 y 4 (fronteras de módulo y adaptador).

### 11.2 Riesgos de la alternativa ganadora (A1)

| Riesgo de A1 | Escenario | Mitigación |
|---|---|---|
| Un SRI lento retiene procesos de la API y degrada las demás operaciones | E8 | Tiempo de espera de 15 s por intento y máximo de 3 intentos; si la prueba de E8 falla, trasladar los reintentos a un proceso en segundo plano |
| Un fallo no controlado en un módulo afecta a toda la API | E2, E1 | Pruebas automáticas, manejo de errores en el adaptador y verificación de estado (`/health`) con reinicio automático de la plataforma |
| El acoplamiento entre módulos erosiona las fronteras y encarece el cambio | E4 | Regla de dependencias (routers → servicios → adaptadores) y revisión de cambios antes de fusionar |
| Un reenvío de la misma factura al SRI genera dos autorizaciones | E2, E6 | Clave de acceso única por factura y reenvío solo de facturas PENDIENTES; verificación en las pruebas del hito H2 |

### 11.3 Sensibilidad de los pesos

| Variante | A1 Monolito modular | A2 Microservicios | A3 Monolito en capas |
|---|---|---|---|
| Base (sección 10) | **4,40** | 3,30 | 3,90 |
| Modificabilidad pesa más (criterio 4 = 30, criterio 5 = 5) | **4,25** | 3,90 | 3,45 |
| Fiabilidad e integridad pesan más (criterio 2 = 35, criterio 6 = 25, criterio 5 = 10, criterios 3 y 7 = 0) | **4,35** | 3,80 | 3,70 |
| Pesos iguales (≈14,3 cada uno) | **4,29** | 3,29 | 3,86 |
| E8 resulta peor de lo esperado: A1 baja a 3 en el criterio 2 (pesos base) | **4,20** | 3,30 | 3,90 |
| E8 resulta peor y se pesa la fiabilidad (A1 = 3 en el criterio 2, pesos de la variante 3) | **4,00** | 3,80 | 3,70 |

**Lectura.** A1 gana en todas las variantes, pero la diferencia con A2 baja a 0,20 puntos cuando la lentitud del SRI (E8) resulta peor de lo esperado y se pesa la fiabilidad. Ese es el punto de sensibilidad que se registra en el ADR-003: la decisión depende de que la prueba de E8 se cumpla con los tiempos de espera previstos.

## 12. Trazabilidad final

| Driver | Escenario | Vistas C4 | ADR |
|---|---|---|---|
| D1 | E6 | C2 (API REST, base de datos) | ADR-002, ADR-003 |
| D2 | E2, E8 | C1, C2 (relación API REST → SRI; adaptador `SriGateway` en C3) | ADR-003 |
| D3 | E1 | C2 (API REST, base de datos) | ADR-001, ADR-002 |
| D4 | E4, E5 | C2 (módulos de la API, despliegue por contenedor), C3 | ADR-001, ADR-002, ADR-003, ADR-004 |
| D5 | E3, E7 | C1, C2 (Aplicación web → API REST) | ADR-001, ADR-003 |
