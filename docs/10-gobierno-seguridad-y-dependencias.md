# 10 · Gobierno del repositorio, verificación de secretos y auditoría de dependencias

> Proyecto **FacturaEC** · Módulo 8 · Semana 3 · versión v0.3.0.
> Marco de referencia: NIST Special Publication 800-218 *Secure Software Development Framework (SSDF) v1.1* (Souppaya et al., 2022) e IEEE Std 828-2012 (IEEE, 2012).

---

## 1. Controles de Gobierno sobre el Repositorio (Práctica PO.3 y PS.1 de NIST SSDF)

Para garantizar que ningún cambio ingrese al tronco principal sin verificación técnica ni supervisión de pares, el repositorio implementa los siguientes controles en `v0.3.0`:

| Control de gobierno | Configuración aplicada en `ApiFacturacion` | Estado |
|---|---|---|
| **Protección de la rama `main`** | Regla activa en GitHub (*Branch protection rule*): bloquea commits directos a `main` y exige que todo cambio entre mediante Pull Request. | Activo |
| **Revisión cruzada obligatoria** | Se exige al menos **1 aprobación (`Require approvals: 1`)** de un integrante distinto al autor del PR, con comentario sustantivo basado en la rúbrica de `.github/pull_request_template.md`. | Activo |
| **Trazabilidad Issue ↔ Rama ↔ PR** | Cada cambio parte de un issue creado con `.github/ISSUE_TEMPLATE/`, se desarrolla en una rama corta (`<tipo>/issue-N-<desc>`) y se vincula en el PR con `Closes #N`. | Activo |
| **Verificación automática en CI** | El workflow `.github/workflows/ci.yml` ejecuta `ruff check src tests`, `ruff format --check src tests` y `pytest -v` en cada Pull Request hacia `main`. | Activo |
| **Versionado Semántico (SemVer)** | Etiquetas inmutables alineadas a cada hito: `v0.1.0` (H1: Dossier), `v0.2.0` (H2: Cadena CASE) y `v0.3.0` (H3: Repositorio gobernado). | Activo |

---

## 2. Verificación de Ausencia de Secretos y Datos Sensibles (Práctica PS.1 y PW.6)

Siguiendo las recomendaciones de NIST SSDF SP 800-218 y la Ley Orgánica de Protección de Datos Personales (LOPDP), se auditó el árbol de archivos y el historial de commits del repositorio:

1. **Variables de entorno y credenciales de base de datos:**
   - En [`src/facturaec/config.py`](../src/facturaec/config.py), tanto `DATABASE_URL` como `JWT_SECRET` se leen exclusivamente desde variables de entorno (`os.environ.get`).
   - En desarrollo y pruebas locales sin variables externas se emplea una base SQLite efímera y una clave de prueba local claramente marcada solo para test, nunca credenciales de Supabase ni de entornos productivos.
2. **Certificados de firma electrónica y llaves privadas:**
   - El archivo [`.gitignore`](../.gitignore) excluye explícitamente `*.p12`, `*.pfx`, `*.pem`, `*.key`, `*.crt`, `.env` y `.env.*`.
3. **Datos tributarios en pruebas BDD:**
   - Todos los RUC utilizados en [`tests/features/`](../tests/features/) y en los ejemplos de [`api/openapi.yaml`](../api/openapi.yaml) emplean el prefijo de provincia ficticio `99` (`9990000001001`, `9990000002001`), que no corresponde a ningún contribuyente real en el catastro del SRI.
4. **Inspección del repositorio:**
   - Se verificó que no existen archivos `.env`, llaves privadas ni tokens reales versionados en ningún commit desde `v0.1.0` hasta `v0.3.0`.

---

## 3. Registro de Revisión de Dependencias (Práctica PW.4 de NIST SSDF)

En cumplimiento de la Instrucción 6 de la actividad y de la práctica **PW.4** de NIST SSDF (*Reutilizar software existente bien asegurado y auditar dependencias de terceros*), se revisaron todas las dependencias de producción y desarrollo declaradas en [`pyproject.toml`](../pyproject.toml):

### 3.1 Dependencias de ejecución (`[project.dependencies]`)

| Paquete | Restricción en `pyproject.toml` | Versión verificada | Licencia | Propósito en FacturaEC | Estado de revisión |
|---|---|---|---|---|---|
| `fastapi` | `>=0.115,<1.0` | `0.162.0` | MIT | Framework HTTP de la API REST y publicación del contrato OpenAPI (`ADR-001`) | Revisada · Sin CVEs críticos conocidos; licencia permisiva compatible |
| `uvicorn` | `>=0.30,<1.0` | `0.40.0` | BSD-3-Clause | Servidor ASGI para ejecución del servicio FastAPI | Revisada · Sin vulnerabilidades; mantenido activamente por Encode |
| `sqlalchemy` | `>=2.0,<3.0` | `2.1.6` | MIT | ORM relacional, transacciones y bloqueo de fila `SELECT ... FOR UPDATE` (`ADR-002`, `E6`) | Revisada · Consultas parametrizadas que previenen inyección SQL |
| `pydantic` | `>=2.8,<3.0` | `2.12.0` | MIT | Validación estricta de esquemas de entrada/salida y montos decimales | Revisada · Mitiga defectos de validación de entrada (OWASP Top 10) |
| `pyjwt` | `>=2.9,<3.0` | `2.11.0` | MIT | Emisión y verificación de tokens JWT (`HS256`) para el aislamiento entre emisores (`E1`) | Revisada · Clave de firma con longitud >= 32 bytes en pruebas |
| `pyyaml` | `>=6.0,<7.0` | `6.0.3` | MIT | Carga segura (`yaml.safe_load`) del contrato `api/openapi.yaml` | Revisada · Se usa exclusivamente `safe_load`, evitando ejecución arbitraria |
| `psycopg[binary]` | `>=3.2,<4.0` | `3.3.6` | LGPL-3.0 | Adaptador PostgreSQL 16 para la prueba de concurrencia `CA5.3` (`E6`) | Revisada · Compatible con despliegue en contenedor |
| `httpx` | `>=0.27,<1.0` | `0.28.1` | BSD-3-Clause | Cliente HTTP del adaptador `SriGatewayHttp` hacia el microservicio `validacion-SRI` y de `TestClient` en las pruebas | Pasa de desarrollo a ejecución · Se usa con tiempo máximo explícito por intento |

### 3.2 Dependencias de desarrollo y verificación (`[project.optional-dependencies.dev]`)

| Paquete | Restricción en `pyproject.toml` | Versión verificada | Licencia | Propósito en la cadena CASE | Estado de revisión |
|---|---|---|---|---|---|
| `pytest` | `>=8.3,<10.0` | `9.1.1` | MIT | Ejecución de pruebas automatizadas y de conformidad (`T7`) | Revisada · Solo entorno de pruebas |
| `pytest-bdd` | `>=7.3,<10.0` | `9.0.0` | MIT | Ejecución directa de escenarios Gherkin en español (`ADR-005`, `T7`) | Revisada · Solo entorno de pruebas |
| `ruff` | `>=0.6,<1.0` | `0.17.2` | MIT | Linter, formateador y analizador estático de seguridad (`reglas S / flake8-bandit`, `T8`) | Revisada · Incluye reglas de seguridad estática activas |

---

## 4. Referencias

- Institute of Electrical and Electronics Engineers. (2012). *IEEE standard for configuration management in systems and software engineering* (IEEE Std 828-2012). IEEE.
- Souppaya, M., Scarfone, K., & Dodson, D. (2022). *Secure software development framework (SSDF) version 1.1: Recommendations for mitigating the risk of software vulnerabilities* (NIST Special Publication 800-218). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-218
