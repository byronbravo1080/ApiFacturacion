# 05 · Matriz de Trazabilidad Punta a Punta

> **Proyecto:** FacturaEC · API REST de Facturación Electrónica  
> **Programa:** Maestría en Ingeniería de Software · Módulo 8 (Automatización de procesos de software)  
> **Institución:** Universidad Politécnica Estatal del Carchi (UPEC)  
> **Hito:** `v0.3.0` (H3 · Repositorio Gobernado y Pipeline Automatizado)  
> **Fecha de congelamiento:** 06/11/2026  

---

## 1. Propósito y Estructura de la Matriz

Este documento establece la **trazabilidad bidireccional y continua** exigida por la actividad autónoma de la Semana 4. La matriz vincula formalmente y sin eslabones rotos cada elemento de ingeniería del software a lo largo de su ciclo de vida:

$$\text{Requisito (HU/CA)} \longrightarrow \text{Escenario de Calidad (E)} \longrightarrow \text{Decisión Arquitectónica (ADR)} \longrightarrow \text{Artefacto (Código/Test)} \longrightarrow \text{Commit / PR} \longrightarrow \text{Quality Gate en CI}$$

### Taxonomía de Identificadores
* **HU (Historia de Usuario):** Especificación funcional en formato Cohn (HU1 a HU7).
* **CA (Criterio de Aceptación):** Medida observable y ejecutable en Gherkin (CA1.1 a CA7.1).
* **E (Escenario de Calidad):** Requisito no funcional medible del dossier (E1: Aislamiento, E2: Contingencia SRI, E6: Concurrencia de secuenciales).
* **ADR (Architectural Decision Record):** Registro formal de decisión arquitectónica (ADR-001 a ADR-006).
* **PR / Commit:** Identificadores inmutables de control de versiones en GitHub.
* **Pipeline (Quality Gate):** Paso automatizado de verificación en `.github/workflows/ci.yml` (T4, T5, T7, T8).

---

## 2. Matriz de Trazabilidad Punta a Punta

| Requisito / CA | Escenario Calidad | ADR Relacionado | Artefactos del Repositorio | Commit / PR en GitHub | Quality Gate en Pipeline CI |
|:---|:---:|:---:|:---|:---:|:---|
| **HU1 · CA1.1**<br>Registro de emisor nuevo y entrega de token JWT (201 Created). | **E1**<br>(Aislamiento) | **ADR-001** (FastAPI)<br>**ADR-002** (PostgreSQL)<br>**ADR-005** (API-First) | • [`src/facturaec/routers.py`](../src/facturaec/routers.py) (`registrar_emisor`)<br>• [`src/facturaec/security.py`](../src/facturaec/security.py) (`crear_token`, `hash_clave`)<br>• [`tests/features/registro_y_aislamiento.feature`](../tests/features/registro_y_aislamiento.feature)<br>• [`api/openapi.yaml`](../api/openapi.yaml) (`/api/v1/auth/registro`) | PR #18 (`95c3dd5`)<br>Commit `f678004` | • **T4:** Spectral (`facturaec-publica-explicita`)<br>• **T7:** `pytest` (`test_registro_y_aislamiento.py`)<br>• **T8:** `ruff check/format` |
| **HU1 · CA1.2**<br>Rechazo de RUC ya registrado con código 409 Conflict. | **E1**<br>(Aislamiento) | **ADR-001** (FastAPI)<br>**ADR-002** (PostgreSQL) | • [`src/facturaec/routers.py`](../src/facturaec/routers.py) (`select(Emisor.id)` check)<br>• [`src/facturaec/models.py`](../src/facturaec/models.py) (`Emisor.ruc` `unique=True`)<br>• [`tests/features/registro_y_aislamiento.feature`](../tests/features/registro_y_aislamiento.feature) | PR #18 (`95c3dd5`)<br>Commit `da85a62` | • **T7:** `pytest` (BDD CA1.2)<br>• **T4:** Spectral (esquema `RucRegistrado`)<br>• **T8:** Ruff static check |
| **HU2 · CA2.1**<br>Registro de clientes aislados por emisor y consulta por ID. | **E1**<br>(Aislamiento) | **ADR-001** (FastAPI)<br>**ADR-002** (PostgreSQL) | • [`src/facturaec/routers.py`](../src/facturaec/routers.py) (`registrar_cliente`, `obtener_cliente`)<br>• [`src/facturaec/models.py`](../src/facturaec/models.py) (`Cliente.emisor_id`)<br>• [`api/openapi.yaml`](../api/openapi.yaml) (`/api/v1/clientes/{clienteId}`) | PR #25 (`8a155a3`, `b87bdfb`)<br>Commit `f678004` | • **T4:** Spectral (`facturaec-protegida-declara-401`)<br>• **T7:** `pytest` (BDD CA2.1 + `test_contrato.py`)<br>• **T8:** Ruff |
| **HU2 · CA2.2**<br>Confidencialidad: Emisor B recibe 404 al consultar recursos de Emisor A. | **E1**<br>(0 fugas de datos) | **ADR-001** (FastAPI)<br>**ADR-002** (PostgreSQL) | • [`src/facturaec/facturacion.py`](../src/facturaec/facturacion.py) (`obtener_propio`)<br>• [`tests/features/registro_y_aislamiento.feature`](../tests/features/registro_y_aislamiento.feature) (Scenarios cliente/factura) | Commit `f678004`<br>PR #16 (`67aa13b`) | • **T7:** `pytest` (BDD CA2.2)<br>• **T8:** Ruff Security AST (`S105`/`S106`) |
| **HU2 · CA2.3**<br>Peticiones sin cabecera `Authorization` responden 401 Unauthorized. | **E1**<br>(100% auth) | **ADR-001** (FastAPI)<br>**ADR-005** (API-First) | • [`src/facturaec/security.py`](../src/facturaec/security.py) (`emisor_actual`)<br>• [`.spectral.yaml`](../.spectral.yaml) (`facturaec-protegida-declara-401`)<br>• [`tests/features/registro_y_aislamiento.feature`](../tests/features/registro_y_aislamiento.feature) | PR #27 (`d1c92d0`)<br>PR #25 (`b87bdfb`) | • **T4:** Spectral (falla si falta 401 en YAML)<br>• **T7:** `pytest` (BDD 6 operaciones CA2.3) |
| **HU3 · CA3.1, CA3.2**<br>Registro de catálogo de productos (IVA 0%, 5%, 15%) y validación 422. | **E7** (Catálogo)<br>**E1** (Aislamiento) | **ADR-001** (FastAPI)<br>**ADR-005** (API-First) | • [`src/facturaec/routers.py`](../src/facturaec/routers.py) (`registrar_producto`, `listar_productos`)<br>• [`src/facturaec/schemas.py`](../src/facturaec/schemas.py) (`tarifa_iva: Literal[0, 5, 15]`)<br>• [`tests/features/facturacion.feature`](../tests/features/facturacion.feature) | PR #25 (`8a155a3`)<br>Commit `f678004` | • **T4:** Spectral (`facturaec-cuerpo-declara-422`)<br>• **T7:** `pytest` (BDD CA3.1/CA3.2)<br>• **T5:** Redocly docs |
| **HU4 · CA4.1**<br>Cálculo determinista de base imponible, desglose IVA y total de factura. | **E3**<br>(Cálculo tributario) | **ADR-001** (FastAPI)<br>**ADR-002** (PostgreSQL) | • [`src/facturaec/facturacion.py`](../src/facturaec/facturacion.py) (`crear_factura`, `detalles`)<br>• [`src/facturaec/models.py`](../src/facturaec/models.py) (`Numeric(12,2)`)<br>• [`tests/features/facturacion.feature`](../tests/features/facturacion.feature) | Commit `f678004`<br>PR #23 (`c7c3ae6`) | • **T7:** `pytest` (BDD CA4.1 totales)<br>• **T8:** Ruff (`E`/`W` PEP8 precision) |
| **HU5 · CA5.1, CA5.2**<br>Generación de clave de acceso de 49 dígitos con Módulo 11 oficial del SRI. | **E6**<br>(Integridad SRI) | **ADR-001** (FastAPI)<br>**ADR-003** (Microservicio SRI) | • [`src/facturaec/clave_acceso.py`](../src/facturaec/clave_acceso.py) (`digito_modulo11`)<br>• [`tests/step_defs/test_facturacion.py`](../tests/step_defs/test_facturacion.py) (`modulo11_independiente`)<br>• [`tests/features/facturacion.feature`](../tests/features/facturacion.feature) | PR #23 (`52886b2`)<br>Commit `f678004` | • **T7:** `pytest` (Verificación matemática de doble implementación limpia) |
| **HU5 · CA5.3**<br>Garantía de cero saltos y cero duplicados bajo 1000 emisiones concurrentes. | **E6**<br>(0 duplicados, 0 saltos) | **ADR-002** (PostgreSQL)<br>**ADR-001** (FastAPI) | • [`src/facturaec/facturacion.py`](../src/facturaec/facturacion.py) (`with_for_update()` en Emisor)<br>• [`src/facturaec/models.py`](../src/facturaec/models.py) (`UniqueConstraint uq_factura_secuencial`)<br>• [`tests/features/facturacion.feature`](../tests/features/facturacion.feature) (`@postgresql CA5.3`) | Commit `f678004`<br>PR #16 (`67aa13b`) | • **T7:** `pytest` con ThreadPoolExecutor (50 workers, 1000 requests) |
| **HU6 · CA6.1, CA6.2**<br>Autorización inmediata (HTTP 200) ante disponibilidad del SRI. | **E2**<br>(Integración SRI) | **ADR-003** (Microservicio SRI)<br>**ADR-001** (FastAPI) | • [`src/facturaec/sri_gateway.py`](../src/facturaec/sri_gateway.py) (`SriGatewayHttp.enviar`)<br>• [`servicioSri/supabase/functions/sri-gateway/gateway.ts`](../../servicioSri/supabase/functions/sri-gateway/gateway.ts)<br>• [`tests/features/envio_sri.feature`](../tests/features/envio_sri.feature) | PR #21 (`b124802`, `4b4add8`) | • **T7:** `pytest` (`test_envio_sri.py`, `test_sri_gateway_http.py`)<br>• **T8:** Ruff static check |
| **HU6 · CA6.3, CA6.4**<br>Resiliencia: 3 reintentos con esperas de 1s y 2s; estado PENDIENTE (HTTP 202). | **E2**<br>(0 facturas perdidas) | **ADR-003** (Microservicio SRI)<br>**ADR-002** (PostgreSQL) | • [`src/facturaec/facturacion.py`](../src/facturaec/facturacion.py) (`enviar_al_sri`, `ESPERAS_SEGUNDOS`)<br>• [`src/facturaec/sri_gateway.py`](../src/facturaec/sri_gateway.py) (`SriNoDisponibleError`)<br>• [`tests/features/envio_sri.feature`](../tests/features/envio_sri.feature) | PR #21 (`4b4add8`)<br>PR #23 (`c7c3ae6`) | • **T7:** `pytest` (BDD CA6.3 backoff + CA6.4 reenvío exitoso en 1 intento) |
| **HU6 (Extensión)**<br>Manejo de rechazo por clave inválida en SRI: HTTP 422 sin reintentos. | **E2**<br>(Respuestas definitivas) | **ADR-003** (Microservicio SRI)<br>**ADR-005** (API-First) | • [`src/facturaec/sri_gateway.py`](../src/facturaec/sri_gateway.py) (`SriRechazoError`)<br>• [`src/facturaec/schemas.py`](../src/facturaec/schemas.py) (`simular_rechazo`)<br>• [`api/openapi.yaml`](../api/openapi.yaml) (`simular_rechazo`) | PR #23 (`52886b2`)<br>PR #25 (`b87bdfb`) | • **T4:** Spectral linting<br>• **T7:** `pytest` (`test_sri_gateway_http.py`) |
| **HU7 · CA7.1**<br>Consulta de estado y trazabilidad de comprobante por ID (`GET /facturas/{id}`). | **E2** (Auditoría)<br>**E1** (Aislamiento) | **ADR-001** (FastAPI)<br>**ADR-005** (API-First) | • [`src/facturaec/routers.py`](../src/facturaec/routers.py) (`obtener_factura`, `listar_facturas`)<br>• [`api/openapi.yaml`](../api/openapi.yaml) (`/api/v1/facturas/{facturaId}`) | PR #25 (`8a155a3`, `b87bdfb`)<br>Commit `f678004` | • **T4:** Spectral<br>• **T5:** Redocly docs build<br>• **T7:** `pytest` (`test_contrato.py`) |

---

## 3. Verificación de Eslabones y Cero Rupturas

### 3.1. Requisitos a Pruebas (Gherkin y `07-historias-y-criterios.md`)
* La prueba unitaria [`tests/test_documentacion.py`](../tests/test_documentacion.py) valida automáticamente que cada escenario Gherkin en `tests/features/` coincida carácter por carácter con el texto publicado en [`docs/07-historias-y-criterios.md`](07-historias-y-criterios.md).
* **Resultado:** 0 discrepancias de texto entre los criterios de aceptación formales y el código ejecutable de prueba.

### 3.2. Contrato a Código (`api/openapi.yaml` a `src/facturaec/routers.py`)
* La prueba de conformidad [`tests/test_contrato.py`](../tests/test_contrato.py) extrae todas las operaciones HTTP inferidas de FastAPI (`app.routes`) y las contrasta contra el conjunto de operaciones del contrato YAML (`api/openapi.yaml`).
* **Resultado:** Las 11 operaciones del backend coinciden exactamente en método HTTP, ruta y `operationId` con el contrato.

### 3.3. Quality Gates Automatizados en GitHub Actions (`.github/workflows/ci.yml`)
Cada Pull Request dirigido a `main` es evaluado por 4 Quality Gates secuenciales:
1. **Gate 1 · Lint de Contrato OpenAPI (Spectral CLI 6.14.3):**
   * Evalúa las reglas base `spectral:oas` más las 4 reglas propias en [`.spectral.yaml`](../.spectral.yaml).
2. **Gate 2 · Construcción de Documentación (Redocly CLI 1.25.12):**
   * Genera el artefacto estático [`docs/api/index.html`](api/index.html) sin advertencias sintácticas.
3. **Gate 3 · Linter y Formateo de Código (Ruff 0.6+):**
   * Ejecuta `ruff check` y `ruff format --check` sobre `src/` y `tests/` con reglas PEP 8, flake8 y Bandit (`S101`-`S106`).
4. **Gate 4 · Ejecución de Pruebas BDD y de Integración (pytest 8+):**
   * Ejecuta los 25 escenarios BDD y los tests de transporte HTTP del SRI con SQLite en memoria y PostgreSQL en pipeline.
   * **Resultado de cobertura:** 100% de los criterios de aceptación CA1.1 a CA7.1 validados.
