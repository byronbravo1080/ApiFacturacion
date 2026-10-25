"""Funciones auxiliares que usan los pasos de Gherkin para llamar a la API."""

CLAVE_PRUEBA = "clave-de-prueba-123"


def cabecera(ctx: dict, nombre: str) -> dict:
    return {"Authorization": f"Bearer {ctx['emisores'][nombre]['token']}"}


def registrar(client, ctx: dict, nombre: str, ruc: str):
    datos = {"ruc": ruc, "razonSocial": f"Comercial Ficticio {nombre}", "clave": CLAVE_PRUEBA}
    respuesta = client.post("/api/v1/auth/registro", json=datos)
    if respuesta.status_code == 201:
        ctx["emisores"][nombre] = {
            "token": respuesta.json()["accessToken"],
            "id": respuesta.json()["emisorId"],
            "ruc": ruc,
            "datos": [ruc, datos["razonSocial"]],  # datos que no deben filtrarse a otros (E1)
        }
    return respuesta


def crear_cliente(client, ctx: dict, nombre: str, razon_social: str = "Cliente Ficticio"):
    respuesta = client.post(
        "/api/v1/clientes",
        headers=cabecera(ctx, nombre),
        json={
            "tipoIdentificacion": "PASAPORTE",
            "identificacion": "X0000001",
            "razonSocial": razon_social,
        },
    )
    if respuesta.status_code == 201:
        ctx["emisores"][nombre]["datos"].append(razon_social)
        ctx["cliente_id"] = respuesta.json()["id"]
    return respuesta


def crear_producto(client, ctx: dict, nombre: str, precio: str = "10.00", tarifa: int = 15):
    respuesta = client.post(
        "/api/v1/productos",
        headers=cabecera(ctx, nombre),
        json={
            "codigo": "P-001",
            "descripcion": "Producto ficticio",
            "precioUnitario": precio,
            "tarifaIva": tarifa,
        },
    )
    if respuesta.status_code == 201:
        ctx["producto_id"] = respuesta.json()["id"]
    return respuesta


def crear_factura(client, ctx: dict, nombre: str, cantidad: int = 1):
    if "cliente_id" not in ctx:
        crear_cliente(client, ctx, nombre)
    if "producto_id" not in ctx:
        crear_producto(client, ctx, nombre)
    respuesta = client.post(
        "/api/v1/facturas",
        headers=cabecera(ctx, nombre),
        json={
            "clienteId": ctx["cliente_id"],
            "detalles": [{"productoId": ctx["producto_id"], "cantidad": cantidad}],
        },
    )
    if respuesta.status_code == 201:
        factura = respuesta.json()
        ctx["factura"] = factura
        ctx["emisores"][nombre]["datos"] += [factura["numero"], factura["claveAcceso"]]
    return respuesta
