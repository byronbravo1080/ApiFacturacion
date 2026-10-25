# ADR-003 · Estilo arquitectónico: monolito modular con adaptador del SRI

- **Estado:** Aceptado (decisión final de estilo)
- **Fecha:** 2026-10-15 (actualizado el 2026-10-16 con E8 y la sensibilidad ampliada)
- **Matriz de decisión:** [sección 10 de `01-contexto-y-drivers.md`](../01-contexto-y-drivers.md#10-matriz-ponderada-y-justificación)

## Contexto

El sistema debe ser fiable ante la caída o la lentitud del SRI (E2, E8), conservar la integridad de la numeración (E6), poder incorporar nuevos tipos de comprobante con poco esfuerzo (E4) y desplegarse automáticamente a costo cero (E5). Estas calidades se contraponen: separar en servicios mejora el aislamiento y la modificabilidad, pero encarece el despliegue y complica la consistencia. El equipo es de 4 personas, con un plazo muy corto (R3) y con infraestructura gratuita (R2). Además, la firma electrónica y la integración con el SRI son la parte de mayor riesgo (D1) y puede que no estén disponibles a tiempo (R6).

## Alternativas consideradas

1. **A1 · Monolito modular:** un solo despliegue de la API con módulos de fronteras claras (routers, servicios, adaptadores).
2. **A2 · Microservicios:** servicios separados (autenticación, facturación, comprobantes/SRI), cada uno con su despliegue y posiblemente su base de datos.
3. **A3 · Monolito en capas sin fronteras de módulo:** un solo despliegue con capas técnicas (controladores, lógica, datos) y sin separación por funcionalidad ni adaptador explícito del SRI.

### Alternativas descartadas

- **A2 · Microservicios:** costo operativo desproporcionado para un equipo de 4 personas con planes gratuitos (criterio de despliegue y costo cero = 1) y consistencia distribuida de la numeración (E6).
- **A3 · Monolito en capas:** sin adaptador explícito ni fronteras de módulo, el fallo del SRI se propaga por el código y el cambio de comprobante toca varias capas (E2, E4).

## Decisión

Adoptar un **monolito modular (A1)** para la API, con la integración del SRI aislada detrás del puerto `SriGateway`. Los módulos internos (`routers`, `services/facturacion`, `services/clave_acceso`, `services/xml_factura`, `services/ride`, `services/sri_gateway`) pueden extraerse a servicios en el futuro sin cambiar los contratos.

El resultado de la [matriz ponderada](../01-contexto-y-drivers.md#10-matriz-ponderada-y-justificación) es: A1 **4,40**; A3 **3,90**; A2 **3,30** (sobre 5). La conclusión se mantiene al variar los pesos (análisis de sensibilidad).

## Trade-off explícito

Se **sacrifica** parte del aislamiento de fallos y de la modificabilidad que ofrecerían los microservicios (E2, E4 puntúan más alto en esa alternativa) a cambio de **simplicidad de despliegue, costo cero y consistencia transaccional** (E5, E6). El riesgo de acoplamiento del monolito se compensa con fronteras de módulo y con el adaptador del SRI, que concentra el punto de falla externo (E2) y permite reemplazar la implementación simulada por la real sin tocar el dominio (D1, R6).

## Punto de sensibilidad

La decisión depende de que la lentitud del SRI (E8) no degrade el resto de la API. Si A1 bajara a 3 en el criterio de fiabilidad, su total sería 4,20 con los pesos base, y 4,00 frente a 3,80 de A2 si además se pondera más la fiabilidad. Por eso la prueba de E8 (hito H2) puede reabrir esta decisión; la mitigación prevista es trasladar los reintentos a un proceso en segundo plano.

## Consecuencias

- (+) Un solo contenedor de API y una sola base de datos: despliegue gratuito y pipeline sencillo (E5, D4).
- (+) Los secuenciales se asignan en una única transacción local con bloqueo de fila (E6).
- (+) `SriGateway` permite desarrollar y probar sin certificado, y cambiar al ambiente de pruebas del SRI sin alterar el dominio (E2, E4).
- (−) Un fallo no controlado en la API afecta a todos los módulos; se mitiga con pruebas automáticas y tratamiento de errores del adaptador.
- (−) Los reintentos al SRI ocurren dentro de la solicitud HTTP (máximo 3 intentos, 15 s de espera por intento); un SRI lento retiene procesos de la API (E8). Un proceso en segundo plano queda como evolución.
- (−) Si la carga crece mucho, habrá que extraer módulos; la estructura actual lo facilita, pero no lo evita.

## Vínculo

| Elemento | Referencia |
|---|---|
| Drivers | D1, D2, D4 |
| Escenarios | E2, E4, E5, E6, E8 (y E1, E3, E7 en la matriz) |
| Restricciones | R2, R3, R6 |
| Vista C4 | Nivel 2: contenedor «API REST» (una sola API con módulos internos) y relación API REST → SRI; nivel 3 complementario: módulos internos |

## Estado de implementación

El repositorio v0.1.0 contiene solo el dossier. Existe un prototipo del backend, fuera de este repositorio, con el adaptador `SriGatewaySimulado` implementado y probado. `SriGatewayPruebas` es un esqueleto sin verificar contra el servicio real y requiere XML firmado (XAdES-BES), que **no** está implementado.
