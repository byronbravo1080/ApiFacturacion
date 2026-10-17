# ADR-001 · Framework del backend: FastAPI (Python)

- **Estado:** Propuesta — pendiente de ratificación por el equipo
- **Fecha:** 2026-10-15

## Contexto

El equipo domina .NET, FastAPI, Angular y Next.js (R4). El backend debe exponer una API REST con al menos 4 endpoints (R5), documentarse con un contrato verificable, desplegarse sin costo (R2, D4) y quedar listo para CI/CD (D4). El plazo es muy corto (R3), por lo que pesa la velocidad de arranque. La parte más delicada del dominio (clave de acceso, XML, firma, integración con el SRI) debe poder implementarse y probarse con poco código de infraestructura.

## Alternativas consideradas

| Criterio | FastAPI (Python) | ASP.NET Core Web API (.NET 8) |
|---|---|---|
| Arranque y volumen de código | Muy rápido; validación y OpenAPI generados desde los tipos | Rápido, algo más de estructura inicial |
| Contrato OpenAPI | Automático, sin configuración adicional | Disponible con paquetes adicionales (Swashbuckle/NSwag) |
| Despliegue gratuito | Contenedor sencillo en Render/Koyeb | Posible (Azure App Service F1, contenedor), con más fricción en planes gratuitos |
| Firma XML (XAdES-BES) | Requiere bibliotecas de terceros (por ejemplo, `signxml`/`lxml`); verificar soporte XAdES | XMLDSig incluido en la plataforma; XAdES requiere biblioteca de terceros |
| Rendimiento | Suficiente para la carga esperada (E3) | Superior en cargas altas, no necesario aquí |
| Afinidad con el frontend elegido (Next.js/TypeScript) | Contrato OpenAPI → cliente tipado | Igual vía OpenAPI |

**Alternativa descartada:** ASP.NET Core Web API (.NET 8), por mayor fricción en planes gratuitos y mayor volumen inicial de código frente al plazo (R3), aunque ofrece mejor rendimiento bruto que no se necesita con esta carga (E3).

## Decisión

Usar **FastAPI** sobre Python 3.12, con SQLAlchemy 2.0 y Pydantic v2.

## Consecuencias

- (+) Contrato OpenAPI automático (`/openapi.json`, `/docs`) y validación de entrada declarativa: facilita E4 y el trabajo en dos repositorios (ADR-004).
- (+) Despliegue en contenedor mínimo sobre planes gratuitos (E5).
- (+) Menos código repetitivo, lo que reduce el riesgo del plazo.
- (−) La firma XAdES-BES no está resuelta de fábrica: se aísla detrás de `SriGateway` y queda como evolución.
- (−) Menor rendimiento bruto que .NET; aceptable para el volumen objetivo y se verifica con la prueba de E3.
- (−) Parte del equipo con más experiencia en .NET tendrá curva de aprendizaje; se mitiga con la estructura de módulos prevista para `app/` (ver [vista de componentes](../02-vistas-c4/c3-componentes-api.md)).

**Revisión:** si la firma XAdES resultara inviable en Python, reabrir esta decisión sustituyendo solo el adaptador del SRI/firma.

## Vínculo

| Elemento | Referencia |
|---|---|
| Drivers | D4, D5 |
| Escenarios | E3, E4, E5 |
| Restricciones | R2, R3, R4, R5 |
| Vista C4 | Nivel 2: contenedor «API REST» (tecnología FastAPI) y relación Aplicación web → API REST |
