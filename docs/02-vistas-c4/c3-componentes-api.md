# Vista complementaria (C4 nivel 3) — Componentes de la API

Vista adicional, no exigida para el hito H1. Muestra los módulos internos del monolito modular y sirve de evidencia para los escenarios E2 y E4. Los nombres corresponden a la estructura de módulos prevista para el backend (carpeta `app/`, a incluir en el hito siguiente).

```mermaid
flowchart LR
    subgraph API["API REST (FastAPI)"]
        direction LR
        subgraph Entrada["Capa de entrada: app/routers"]
            r_auth["auth"]
            r_cli["clientes"]
            r_prod["productos"]
            r_fact["facturas"]
        end
        subgraph Dominio["Servicios: app/services"]
            s_fact["facturacion"]
            s_clave["clave_acceso"]
            s_xml["xml_factura"]
            s_ride["ride"]
            s_ident["identificacion"]
            s_gw["sri_gateway (SriGateway)"]
        end
        seg["security + deps (JWT, emisor actual)"]
        datos["models + database (SQLAlchemy)"]
    end

    web["Aplicación web (Next.js)"] -->|HTTPS / JSON| r_auth & r_cli & r_prod & r_fact
    r_auth & r_cli & r_prod & r_fact --> seg
    r_cli --> s_ident
    r_fact --> s_fact
    r_fact --> s_ride
    s_fact --> s_clave
    s_fact --> s_xml
    s_fact --> s_gw
    s_gw -->|SOAP/HTTPS| sri[("SRI")]
    r_auth & r_cli & r_prod & r_fact & s_fact --> datos
    datos --> db[("PostgreSQL")]
```

| Componente | Responsabilidad |
|---|---|
| `routers/*` | Contrato HTTP; validación de entrada con Pydantic |
| `security`, `deps` | Hash de contraseñas, JWT y resolución del emisor autenticado (E1) |
| `services/facturacion` | Cálculo de totales, asignación de secuencial bajo bloqueo (E6), reintentos al SRI (E2) |
| `services/clave_acceso` | Clave de 49 dígitos con dígito verificador módulo 11 |
| `services/xml_factura` | XML de factura 1.1.0 sin firmar |
| `services/ride` | PDF de representación impresa |
| `services/sri_gateway` | Puerto con adaptadores `SriGatewaySimulado` y `SriGatewayPruebas` (E2, E4) |

**Lectura para E4:** agregar la nota de crédito implica un nuevo `xml_*` y un caso de uso en `services/`; no toca `routers/auth`, `routers/clientes` ni `routers/productos`.
