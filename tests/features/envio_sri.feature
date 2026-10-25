# language: es
# Historias HU6 y HU7 · Escenario de calidad E2 (fiabilidad ante la indisponibilidad del SRI) · Driver D2
# El SRI se reemplaza por el adaptador simulado SriGatewaySimulado (ADR-003); no se contacta al SRI real.

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
