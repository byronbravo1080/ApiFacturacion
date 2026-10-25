# language: es
# Historias HU3, HU4 y HU5 · Escenario de calidad E6 (integridad de la numeración) · Drivers D1 y D5
# Las tarifas de IVA (0 %, 5 % y 15 %) deben contrastarse con la ficha técnica vigente del SRI (supuesto 1.4 del dossier).

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
