# FacturaEC · API de facturación electrónica

Sistema web de **facturación electrónica para pequeñas empresas de Ecuador**. Este repositorio contiene el **dossier de arquitectura** ([`docs/`](docs/)) y, desde la versión **v0.2.0**, la **cadena CASE** del proyecto: contrato OpenAPI, historias y criterios en Gherkin, documentación, mock y stubs generados, y un esqueleto ejecutable de la API con sus pruebas.

Módulo 8 · Automatización de procesos de software · Maestría en Ingeniería en Software, Universidad Politécnica Estatal del Carchi.
**Integrantes:** Byron Bravo, Jairo Jácome, Jordan Montenegro, Luis Cisneros.

## Cadena CASE (v0.2.0)

```mermaid
flowchart LR
    hu["Historias HU1–HU7<br/>docs/07"] --> ca["Criterios Gherkin<br/>tests/features/*.feature"]
    hu --> contrato["Contrato OpenAPI<br/>api/openapi.yaml"]
    contrato --> lint["Spectral + reglas propias<br/>0 hallazgos"]
    lint --> docs["Documentación<br/>docs/api/index.html"]
    lint --> mock["Mock<br/>Prism :4010"]
    lint --> stubs["Stubs<br/>generated/stubs-fastapi"]
    stubs -. forma .-> src["Esqueleto FastAPI<br/>src/facturaec"]
    ca --> pruebas["pytest-bdd<br/>31 pruebas"]
    src --> pruebas
    contrato --> conf["Conformidad<br/>test_contrato.py + Prism proxy"]
    src --> conf
```

| Documento | Contenido |
|---|---|
| [`docs/01-contexto-y-drivers.md`](docs/01-contexto-y-drivers.md) | Contexto, stakeholders, drivers, escenarios E1–E8 y matriz de estilos (v0.1.0) |
| [`docs/02-vistas-c4/`](docs/02-vistas-c4/) | Vistas C4 como código (Mermaid) |
| [`docs/03-adr/`](docs/03-adr/) | ADR-001 a ADR-005 (nuevo: contrato API-first y pruebas BDD) |
| [`docs/04-registro-ia.md`](docs/04-registro-ia.md) | Registro de uso de IA, con la verificación de cada artefacto |
| [`docs/06-mapa-toolchain.md`](docs/06-mapa-toolchain.md) | Proceso, 10 tareas puntuadas, herramientas por fase y pruebas de herramientas |
| [`docs/07-historias-y-criterios.md`](docs/07-historias-y-criterios.md) | Historias, criterios en Gherkin y matriz de trazabilidad |
| [`docs/08-matriz-seleccion.md`](docs/08-matriz-seleccion.md) | Evaluación y selección de herramientas (ISO/IEC 14102) |
| [`api/openapi.yaml`](api/openapi.yaml) | Contrato de la API (fuente de verdad) |

## Alcance de v0.2.0

**Implementado y probado:**

- Registro del emisor con token JWT.
- Clientes y productos aislados por emisor (E1).
- Facturas con IVA (0 %, 5 % y 15 %).
- Secuencial asignado bajo bloqueo de fila, con 0 duplicados en 1000 solicitudes concurrentes (E6).
- Clave de acceso de 49 dígitos con módulo 11.
- Envío al SRI mediante un **adaptador simulado**, con 3 intentos y la factura PENDIENTE si el SRI no responde (E2).

**No implementado (backlog, `docs/07`, sección 5.1):**

- Lentitud del SRI (E8).
- XML firmado (XAdES-BES) y RIDE.
- Inicio de sesión.
- Nota de crédito.
- Frontend.
- Pipeline de CI/CD.
- Integración real con el SRI.

Los RUC usados en las pruebas son ficticios.

## Requisitos

- Python 3.12 o superior.
- Node.js 18 o superior (para Spectral, Redocly y Prism).
- Java 11 o superior (para OpenAPI Generator).
- PostgreSQL, local o gestionado (por ejemplo, Supabase), **solo para la prueba de concurrencia de E6**.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate
pip install -e ".[dev]" openapi-generator-cli
npm install -g @stoplight/spectral-cli @stoplight/prism-cli @redocly/cli
```

`openapi-generator-cli` de PyPI trae el JAR de OpenAPI Generator. La alternativa de npm (`@openapitools/openapi-generator-cli`) descarga el JAR de Maven en el primer uso.

## Ejecutar la API

```bash
PYTHONPATH=src uvicorn facturaec.main:crear_app --factory --reload
```

- `http://localhost:8000/docs` muestra el contrato `api/openapi.yaml` (no el que infiere FastAPI).
- Sin `DATABASE_URL`, la API usa SQLite (`facturaec.db`).
- Para simular la caída del SRI (E2), arranque con `SRI_SIMULAR_CAIDA=true`.
- En producción, defina `JWT_SECRET`.

## Comandos de la cadena

| Paso | Comando |
|---|---|
| Validar el contrato (T4) | `spectral lint api/openapi.yaml` |
| Revisor alternativo (T4) | `redocly lint api/openapi.yaml` |
| Documentación (T5) | `openapi-generator-cli generate -i api/openapi.yaml -g html2 -o docs/api` |
| Mock (T5) | `prism mock api/openapi.yaml --port 4010` |
| Stubs (T6) | `openapi-generator-cli generate -i api/openapi.yaml -g python-fastapi -o generated/stubs-fastapi --additional-properties=packageName=facturaec_stubs` |
| Pruebas (T7) | `pytest` (SQLite; omite la prueba de E6) |
| Pruebas con E6 (T7) | `TEST_DATABASE_URL=postgresql+psycopg://usuario:clave@host:5432/base pytest` |
| Linter (T8) | `ruff check src tests` y `ruff format --check src tests` |

**Base para la prueba de E6.** Puede ser un PostgreSQL local o una base de Supabase propia. Use una base vacía y exclusiva para pruebas, porque la prueba borra y recrea las tablas. La URI con la clave va solo en la variable de entorno de su máquina: no se escribe en el repositorio ni se comparte con herramientas de IA.

## Versiones

Ver [`CHANGELOG.md`](CHANGELOG.md). Convención de commits: [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/).
