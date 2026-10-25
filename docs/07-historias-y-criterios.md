# 07 · Historias de usuario, criterios de aceptación y trazabilidad

> Proyecto **FacturaEC** · Módulo 8 · Semana 2 (sesiones 4 y 5) · versión v0.2.0.
> Fuente de los escenarios: [`01-contexto-y-drivers.md`](01-contexto-y-drivers.md), sección 5 (E1 a E8).
> Fuente ejecutable de los criterios: [`tests/features/`](../tests/features/). Los bloques Gherkin de este documento son copia de esos archivos; si se cambia un criterio, se cambia primero el `.feature` (es el que se ejecuta) y después este documento.

Identificadores: **HU** (historia de usuario), **CA** (criterio de aceptación, numerado por historia: CA2.3 es el tercer criterio de HU2), **E** (escenario de calidad), **S** (stakeholder), **D** (driver), **ADR** (decisión de arquitectura) y **T** (tarea del mapa de toolchain, ver [`06-mapa-toolchain.md`](06-mapa-toolchain.md)).

## 1. Alcance de v0.2.0

El esqueleto cubre los escenarios **E1** (aislamiento entre emisores), **E2** (caída del SRI) y **E6** (numeración sin duplicados ni saltos). Son tres de los cuatro escenarios de mayor prioridad del dossier (sección 6). El cuarto, **E8** (lentitud del SRI), y los escenarios E3, E4, E5 y E7 quedan como historias del backlog (sección 5 de este documento). Necesitan una prueba de carga, el frontend o el pipeline de CI/CD, que corresponden a hitos posteriores.

## 2. Historias de usuario

Formato «Como / quiero / para» (Cohn, 2004). Cada historia se liga a un stakeholder, un driver y un escenario del dossier.

| ID | Historia | Stakeholder | Driver · escenario | Endpoint |
|---|---|---|---|---|
| HU1 | Como dueño de una pequeña empresa, quiero registrar mi negocio y obtener acceso, para emitir comprobantes a mi nombre. | S1 | D3 · E1 | `POST /api/v1/auth/registro` |
| HU2 | Como dueño de una pequeña empresa, quiero registrar a mis clientes y que solo mi negocio pueda verlos, para facturarles sin exponer sus datos a otros negocios. | S1 | D3 · E1 | `POST /api/v1/clientes`, `GET /api/v1/clientes/{clienteId}` |
| HU3 | Como dueño de una pequeña empresa, quiero registrar mis productos con su precio y su tarifa de IVA, para facturarlos sin escribir sus datos cada vez. | S1 | D5 · E7 (indirecto) | `POST /api/v1/productos` |
| HU4 | Como dueño de una pequeña empresa, quiero que la factura calcule subtotal, IVA y total, para no hacer cálculos a mano ni equivocarme. | S1 | D5, D1 · E3 (indirecto) | `POST /api/v1/facturas` |
| HU5 | Como SRI (regulador), quiero que cada factura tenga un secuencial único y consecutivo y una clave de acceso válida, para que no existan comprobantes duplicados. | S3 | D1 · E6 | `POST /api/v1/facturas` |
| HU6 | Como dueño de una pequeña empresa, quiero enviar mis facturas al SRI y que se conserven si el SRI no responde, para no perder comprobantes ni volver a emitirlos. | S1, S3 | D2 · E2 | `POST /api/v1/facturas/{facturaId}/enviar-sri` |
| HU7 | Como contador externo, quiero consultar el estado de autorización de una factura, para saber qué comprobantes puedo declarar. | S2 | D2 · E2 | `GET /api/v1/facturas/{facturaId}` |

**Nota sobre HU7.** En la primera versión hay un solo usuario por emisor (sección 1.3 del dossier), así que el contador consulta con la cuenta del emisor. Los roles separados son una evolución (fuera de alcance).

### 2.1 Revisión INVEST

| Cualidad | Cómo se cumple | Observación |
|---|---|---|
| Independiente | Cada historia tiene su endpoint y sus criterios | HU4 a HU7 necesitan datos previos (cliente, producto, factura); los pasos `Dado` los crean y no dependen de otra historia en ejecución |
| Negociable | Ninguna fija tecnología ni interfaz | La forma de la respuesta se acuerda en el contrato, no en la historia |
| Valiosa | Cada una nombra el beneficio para S1, S2 o S3 | — |
| Estimable | Alcance acotado a una operación | — |
| Pequeña (Small) | Ninguna supera un endpoint, salvo HU2 (dos) | — |
| Verificable (Testable) | Todas tienen criterios en Gherkin con una medida | Ver sección 3 |

## 3. Criterios de aceptación en Gherkin

Una medida por escenario y un solo comportamiento por escenario (buena práctica de la sesión 5). Las medidas numéricas salen de los escenarios del dossier:

- **E1:** 401 en el 100 % de las solicitudes sin token; 404 ante recursos de otro emisor; 0 campos de otro emisor.
- **E2:** 0 facturas perdidas; 3 intentos con esperas de 1 s y 2 s; 202 en 60 s o menos; reenvío en 1 solicitud.
- **E6:** 0 secuenciales duplicados y 0 saltos en 1000 solicitudes concurrentes.

### 3.1 HU1 y HU2 · `tests/features/registro_y_aislamiento.feature` (E1)

```gherkin
# language: es
@HU1 @HU2 @E1
Característica: Registro del emisor y aislamiento de sus datos
  Como dueño de una pequeña empresa
  Quiero registrar mi negocio y que mis clientes y facturas solo sean visibles para él
  Para emitir comprobantes a mi nombre sin exponer mis datos a otros negocios

  @HU1 @CA1.1
  Escenario: Registro de un emisor nuevo
    Cuando se registra el emisor "A" con RUC "9990000001001"
    Entonces la respuesta tiene el código 201
    Y la respuesta contiene un token de acceso

  @HU1 @CA1.2
  Escenario: Rechazo de un RUC ya registrado
    Dado que el emisor "A" está registrado con RUC "9990000001001"
    Cuando se registra el emisor "C" con RUC "9990000001001"
    Entonces la respuesta tiene el código 409

  @HU2 @CA2.1
  Escenario: El emisor registra un cliente y lo consulta
    Dado que el emisor "A" está registrado con RUC "9990000001001"
    Cuando el emisor "A" registra el cliente "Ferretería Ejemplo"
    Entonces la respuesta tiene el código 201
    Y el emisor "A" puede consultar el cliente "Ferretería Ejemplo"

  @HU2 @CA2.2
  Esquema del escenario: Otro emisor no puede ver un <recurso> ajeno
    Dado que el emisor "A" está registrado con RUC "9990000001001"
    Y que el emisor "B" está registrado con RUC "9990000002001"
    Y que el emisor "A" tiene un <recurso> registrado
    Cuando el emisor "B" consulta ese <recurso>
    Entonces la respuesta tiene el código 404
    Y la respuesta no contiene datos del emisor "A"

    Ejemplos:
      | recurso |
      | cliente |
      | factura |

  @HU2 @CA2.3
  Esquema del escenario: Solicitud sin token a <operacion>
    Dado que el emisor "A" está registrado con RUC "9990000001001"
    Cuando se llama a "<operacion>" sin token
    Entonces la respuesta tiene el código 401

    Ejemplos:
      | operacion                                  |
      | POST /api/v1/clientes                      |
      | GET /api/v1/clientes/{id}                  |
      | POST /api/v1/productos                     |
      | POST /api/v1/facturas                      |
      | GET /api/v1/facturas/{id}                  |
      | POST /api/v1/facturas/{id}/enviar-sri      |
```

Los RUC son ficticios: el código de provincia 99 no existe, así que no corresponden a contribuyentes reales. CA2.3 recorre las seis operaciones protegidas para comprobar la medida «401 en el 100 % de las solicitudes sin token».

### 3.2 HU3, HU4 y HU5 · `tests/features/facturacion.feature` (E6)

```gherkin
# language: es
@HU3 @HU4 @HU5
Característica: Emisión de facturas con totales y numeración válidos
  Como dueño de una pequeña empresa
  Quiero que cada factura calcule el IVA y reciba un número único y consecutivo
  Para emitir comprobantes que el SRI acepte sin hacer cálculos a mano

  Antecedentes:
    Dado que el emisor "A" está registrado con RUC "9990000001001"
    Y que el emisor "A" tiene un cliente registrado

  @HU3 @CA3.1
  Escenario: Registro de un producto con tarifa de IVA válida
    Cuando el emisor "A" registra un producto con precio "10.00" y tarifa de IVA 15
    Entonces la respuesta tiene el código 201

  @HU3 @CA3.2
  Escenario: Rechazo de una tarifa de IVA no permitida
    Cuando el emisor "A" registra un producto con precio "10.00" y tarifa de IVA 12
    Entonces la respuesta tiene el código 422

  @HU4 @CA4.1
  Esquema del escenario: Cálculo de subtotal, IVA y total de una línea
    Dado que el emisor "A" tiene un producto con precio "<precio>" y tarifa de IVA <tarifa>
    Cuando el emisor "A" crea una factura con <cantidad> unidades de ese producto
    Entonces la respuesta tiene el código 201
    Y la factura tiene subtotal "<subtotal>", IVA "<iva>" y total "<total>"
    Y la factura queda en estado "CREADA"

    Ejemplos:
      | precio | tarifa | cantidad | subtotal | iva  | total |
      | 10.00  | 15     | 1        | 10.00    | 1.50 | 11.50 |
      | 3.35   | 15     | 3        | 10.05    | 1.51 | 11.56 |
      | 8.00   | 0      | 2        | 16.00    | 0.00 | 16.00 |
      | 20.00  | 5      | 1        | 20.00    | 1.00 | 21.00 |

  @HU5 @E6 @CA5.1
  Escenario: Secuenciales consecutivos para facturas sucesivas
    Cuando el emisor "A" crea 3 facturas seguidas
    Entonces los números de factura son "001-001-000000001", "001-001-000000002" y "001-001-000000003"

  @HU5 @E6 @CA5.2
  Escenario: Clave de acceso válida
    Cuando el emisor "A" crea una factura
    Entonces la clave de acceso tiene 49 dígitos
    Y su dígito verificador módulo 11 es correcto
    Y la clave de acceso contiene el RUC del emisor y el secuencial de la factura

  @HU5 @E6 @CA5.3 @postgresql
  Escenario: Solicitudes concurrentes de emisión del mismo emisor
    Cuando se envían 1000 solicitudes concurrentes de creación de factura del emisor "A"
    Entonces se crean 1000 facturas
    Y hay 0 secuenciales duplicados
    Y hay 0 saltos en la numeración
```

El segundo ejemplo de CA4.1 prueba el redondeo: 10,05 × 15 % = 1,5075, que se redondea a 1,51 (mitad hacia arriba). CA5.3 lleva la etiqueta `@postgresql` porque, según el ADR-002, SQLite ignora el bloqueo de fila (`FOR UPDATE`), así que la prueba solo tiene sentido contra PostgreSQL. **Nivel de concurrencia:** la prueba envía las 1000 solicitudes desde 50 hilos simultáneos, y la API las atiende con hasta 40 hilos. Son 1000 solicitudes con concurrencia real acotada, no 1000 simultáneas; basta para que, sin el bloqueo de fila, aparezcan duplicados (lo demuestra la prueba de mutación al retirar `with_for_update()`).

### 3.3 HU6 y HU7 · `tests/features/envio_sri.feature` (E2)

```gherkin
# language: es
@HU6 @HU7 @E2
Característica: Envío de facturas al SRI sin perder comprobantes
  Como dueño de una pequeña empresa
  Quiero enviar mis facturas al SRI y que se conserven si el SRI no responde
  Para no perder comprobantes ni tener que volver a emitirlos

  Antecedentes:
    Dado que el emisor "A" está registrado con RUC "9990000001001"
    Y que el emisor "A" tiene una factura en estado "CREADA"

  @HU6 @CA6.1
  Escenario: Envío con el SRI disponible
    Dado que el SRI está disponible
    Cuando el emisor "A" envía la factura al SRI
    Entonces la respuesta tiene el código 200
    Y la factura queda en estado "AUTORIZADA"
    Y se hizo 1 intento de envío

  @HU6 @CA6.2
  Escenario: Envío con el SRI no disponible
    Dado que el SRI no está disponible
    Cuando el emisor "A" envía la factura al SRI
    Entonces la respuesta tiene el código 202 en menos de 60 segundos
    Y la factura queda en estado "PENDIENTE"
    Y se hicieron 3 intentos de envío con esperas de 1 y 2 segundos
    Y la factura sigue registrada con sus totales

  @HU6 @CA6.3
  Escenario: Reenvío cuando el SRI se restablece
    Dado que el SRI no está disponible
    Y que el emisor "A" envió la factura al SRI
    Y que el SRI se restablece
    Cuando el emisor "A" envía la factura al SRI
    Entonces la respuesta tiene el código 200
    Y la factura queda en estado "AUTORIZADA"

  @HU6 @CA6.4
  Escenario: Rechazo del reenvío de una factura ya autorizada
    Dado que el SRI está disponible
    Y que el emisor "A" envió la factura al SRI
    Cuando el emisor "A" envía la factura al SRI
    Entonces la respuesta tiene el código 409
    Y el SRI recibió la factura una sola vez

  @HU7 @CA7.1
  Escenario: El contador consulta el estado de una factura pendiente
    Dado que el SRI no está disponible
    Y que el emisor "A" envió la factura al SRI
    Cuando se consulta la factura con la cuenta del emisor "A"
    Entonces la respuesta tiene el código 200
    Y la factura queda en estado "PENDIENTE"
    Y la consulta muestra 3 intentos de envío
```

El SRI se reemplaza por el adaptador `SriGatewaySimulado` (ADR-003); no se contacta al SRI real. En CA6.2 las esperas de 1 s y 2 s se verifican con un reloj simulado que registra las esperas pedidas, para no detener la prueba. Por eso el límite de 60 s se comprueba sobre una ejecución que dura menos de un segundo. Con esperas reales, la respuesta tardaría unos 3 s. CA6.4 cubre el riesgo de doble autorización de la sección 11.2 del dossier.

## 4. Revisión con la lista de ISO/IEC/IEEE 29148

| Atributo | Pregunta | Resultado |
|---|---|---|
| Necesario | ¿Responde a un stakeholder o a un driver? | Sí: las siete historias se ligan a S1, S2 o S3 y a D1, D2, D3 o D5 |
| No ambiguo | ¿Admite una sola interpretación? | Se precisaron tres términos: «factura conservada» (sigue consultable con los mismos totales), «recurso ajeno» (pertenece a otro emisor) y «salto» (diferencia mayor que 1 entre secuenciales consecutivos) |
| Verificable | ¿Tiene un criterio comprobable? | Sí: 25 escenarios ejecutables, todos con una medida |
| Consistente | ¿Contradice otro requisito o decisión? | No: CA5.3 es coherente con el ADR-002 (bloqueo y restricción única), CA6.2 con el ADR-003 (adaptador) y CA2.2 con el 404 que exige E1 |
| Trazable | ¿Se rastrea hasta un escenario y un artefacto? | Sí: ver la tabla de la sección 5 |

## 5. Matriz de trazabilidad

| Historia | Escenario | Criterios | Endpoint (operationId) | ADR | Prueba ejecutable |
|---|---|---|---|---|---|
| HU1 | E1 | CA1.1, CA1.2 | `registrarEmisor` | ADR-001, ADR-005 | `test_registro_y_aislamiento.py` |
| HU2 | E1 | CA2.1, CA2.2, CA2.3 | `registrarCliente`, `obtenerCliente` | ADR-001, ADR-002 | `test_registro_y_aislamiento.py` |
| HU3 | E7 (indirecto) | CA3.1, CA3.2 | `registrarProducto` | ADR-001 | `test_facturacion.py` |
| HU4 | E3 (indirecto) | CA4.1 | `crearFactura` | ADR-001, ADR-003 | `test_facturacion.py` |
| HU5 | E6 | CA5.1, CA5.2, CA5.3 | `crearFactura` | ADR-002, ADR-003 | `test_facturacion.py` |
| HU6 | E2 | CA6.1, CA6.2, CA6.3, CA6.4 | `enviarFacturaSri` | ADR-003 | `test_envio_sri.py` |
| HU7 | E2 | CA7.1 | `obtenerFactura` | ADR-003 | `test_envio_sri.py` |
| — | — | Conformidad contrato ↔ código | las 8 operaciones | ADR-005 | `test_contrato.py` |

**Trazabilidad hacia adelante** (¿en qué se convirtió el requisito?): se lee de izquierda a derecha. **Trazabilidad hacia atrás** (¿por qué existe esta prueba?): cada escenario Gherkin lleva las etiquetas `@HU` y `@CA`, y cada operación del contrato menciona en su `description` la historia y el escenario que la originan.

### 5.1 Backlog pendiente (hitos posteriores)

| ID | Historia | Escenario | Por qué queda pendiente |
|---|---|---|---|
| HU8 | Como dueño de una pequeña empresa, quiero que la API siga respondiendo aunque el SRI esté lento, para seguir emitiendo y consultando facturas. | E8 | Necesita el tiempo máximo de 15 s por intento en el adaptador real y una prueba con retardo bajo carga |
| HU9 | Como contador externo, quiero descargar el XML y el RIDE de cada factura, para archivarlos y declarar. | E2 (S2) | Necesita la generación del XML y del RIDE en PDF |
| HU10 | Como dueño de una pequeña empresa, quiero iniciar sesión con mi RUC y mi clave, para entrar desde otro dispositivo. | E1 | El registro ya entrega un token; el inicio de sesión se agrega con el frontend |
| HU11 | Como equipo de desarrollo, quiero agregar la nota de crédito reutilizando la clave de acceso y el adaptador del SRI, para ampliar los comprobantes con poco esfuerzo. | E4 | Fuera del alcance de la primera versión (sección 1.3 del dossier) |
| HU12 | Como dueño de una pequeña empresa sin formación técnica, quiero emitir mi primera factura en 3 minutos o menos, para empezar a usar el sistema sin ayuda. | E7 | Necesita el frontend (repositorio `facturaec-frontend`) |

## 6. Gestión de trazabilidad y evolución hacia GitHub Issues / Projects

En el mapa de toolchain ([`06-mapa-toolchain.md`](06-mapa-toolchain.md)), la fase *Analizar* asigna como herramienta candidata **GitHub Issues y Projects** junto con **Gherkin** (tarea `T2`, 27 puntos, prioridad Media). Dado que `T2` no forma parte de las tres tareas de mayor puntaje priorizadas para la prueba de herramientas (`T7`, `T4` y `T6`), en `v0.2.0` la trazabilidad completa se consolida directamente en la matriz de la sección 5 de este documento y en las etiquetas `@HU`, `@CA` y `@E` de los archivos `.feature`. Para los hitos posteriores de integración continua, cada historia del backlog (`HU8` a `HU12`) se gestionará como issue individual enlazado mediante la plantilla [`.github/pull_request_template.md`](../.github/pull_request_template.md).
