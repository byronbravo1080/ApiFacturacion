# language: es
# Historias HU1 y HU2 · Escenario de calidad E1 (confidencialidad entre emisores) · Driver D3
# RUC ficticios: el código de provincia 99 no existe, por lo que no corresponden a contribuyentes reales.

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
