"""Pruebas derivadas de tests/features/registro_y_aislamiento.feature (HU1, HU2 · E1)."""

from pytest_bdd import parsers, scenarios, then, when

from ayudantes import cabecera, crear_cliente

scenarios("registro_y_aislamiento.feature")

RUTAS = {"cliente": "/api/v1/clientes/{id}", "factura": "/api/v1/facturas/{id}"}


@then("la respuesta contiene un token de acceso")
def contiene_token(ctx):
    cuerpo = ctx["respuesta"].json()
    assert cuerpo["tokenType"] == "bearer"
    assert cuerpo["accessToken"].count(".") == 2  # formato JWT: cabecera.datos.firma


@when(parsers.parse('el emisor "{nombre}" registra el cliente "{razon_social}"'))
def registra_cliente(client, ctx, nombre, razon_social):
    ctx["respuesta"] = crear_cliente(client, ctx, nombre, razon_social)


@then(parsers.parse('el emisor "{nombre}" puede consultar el cliente "{razon_social}"'))
def puede_consultar(client, ctx, nombre, razon_social):
    respuesta = client.get(f"/api/v1/clientes/{ctx['cliente_id']}", headers=cabecera(ctx, nombre))
    assert respuesta.status_code == 200
    assert respuesta.json()["razonSocial"] == razon_social


@when(parsers.parse('el emisor "{nombre}" consulta ese {recurso}'))
def consulta_recurso_ajeno(client, ctx, nombre, recurso):
    ruta = RUTAS[recurso].format(id=ctx["recurso_id"])
    ctx["respuesta"] = client.get(ruta, headers=cabecera(ctx, nombre))


@then(parsers.parse('la respuesta no contiene datos del emisor "{nombre}"'))
def sin_datos_ajenos(ctx, nombre):
    texto = ctx["respuesta"].text
    filtrados = [dato for dato in ctx["emisores"][nombre]["datos"] if dato in texto]
    assert filtrados == [], f"La respuesta expone datos de otro emisor: {filtrados}"


@when(parsers.parse('se llama a "{operacion}" sin token'))
def llamada_sin_token(client, ctx, operacion):
    metodo, ruta = operacion.split(" ")
    ctx["respuesta"] = client.request(metodo, ruta.replace("{id}", "1"), json={})
