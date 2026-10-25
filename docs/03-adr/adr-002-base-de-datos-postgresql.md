# ADR-002 · Base de datos: PostgreSQL gestionado

- **Estado:** Aceptado
- **Fecha:** 2026-10-15

## Contexto

El sistema necesita transacciones, restricciones de unicidad y bloqueo de filas para garantizar que los secuenciales de las facturas nunca se repitan (D1/E6), además de aislar los datos por emisor (D3/E1). La restricción de costo (R2) exige una opción gratuita. El modelo de datos es claramente relacional (emisor, cliente, producto, factura, detalle, comprobante).

## Alternativas consideradas

| Criterio | PostgreSQL gestionado (Supabase / Neon) | SQL Server (Azure, nivel gratuito) | MongoDB Atlas (nivel gratuito) | SQLite |
|---|---|---|---|---|
| Transacciones y restricciones únicas (E6) | Completas | Completas | Limitadas para este caso | Completas, pero un solo escritor |
| Bloqueo de fila (`SELECT … FOR UPDATE`) | Sí | Sí (hints) | No equivalente directo | No |
| Nivel gratuito | Sí | Limitado | Sí | No aplica (archivo local) |
| Despliegue en entorno efímero | Sí | Sí | Sí | No (el disco de los planes gratuitos es efímero) |
| Afinidad con el modelo | Alta | Alta | Baja | Alta |

**Alternativas descartadas:** SQL Server (nivel gratuito limitado), MongoDB Atlas (sin equivalente directo al bloqueo de fila y a la restricción única que exige E6) y SQLite como base de producción (disco efímero y un solo escritor).

## Decisión

Usar **PostgreSQL gestionado** (Supabase o Neon). **SQLite** se usa solo en desarrollo local y en las pruebas automáticas, mediante la misma capa SQLAlchemy.

## Consecuencias

- (+) Integridad de la numeración: bloqueo de la fila del emisor al asignar el secuencial más la restricción `uq_factura_secuencial` como red de seguridad (E6).
- (+) El esquema relacional impone `emisor_id` en cada tabla de negocio y facilita filtrar por tenant (E1).
- (+) Nivel gratuito sin costo (E5, R2).
- (−) Los planes gratuitos pueden pausar o escalar a cero proyectos inactivos y añadir latencia al primer acceso; se documenta como limitación. Verificar las condiciones vigentes del proveedor antes de fijarlas.
- (−) SQLite en pruebas ignora `FOR UPDATE`: la prueba concurrente de E6 debe ejecutarse contra PostgreSQL en CI (hito H2).
- (−) El primer incremento del backend creará las tablas al arrancar; las migraciones con Alembic quedan como evolución.

## Vínculo

| Elemento | Referencia |
|---|---|
| Drivers | D1, D3, D4 |
| Escenarios | E6, E1, E5 |
| Restricciones | R1, R2 |
| Vista C4 | Nivel 2: contenedor «Base de datos» y relación API REST → Base de datos (lee y escribe, SQL) |
