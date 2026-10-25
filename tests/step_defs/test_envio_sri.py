"""Pruebas derivadas de tests/features/envio_sri.feature (HU6, HU7 · E2)."""

import time

from pytest_bdd import given, parsers, scenarios, then, when

from ayudantes import cabecera, crear_factura

scenarios("envio_sri.feature")


@given(parsers.parse('que el emisor "{nombre}" tiene una factura en estado "CREADA"'))
def factura_creada(client, ctx, nombre):
    assert crear_factura(client, ctx, nombre).status_code == 201
    ctx["total_original"] = ctx["factura"]["total"]


@given("que el SRI está disponible")
def sri_disponible(sri):
    sri.disponible = True


@given("que el SRI no está disponible")
def sri_caido(sri):
    sri.disponible = False


@given("que el SRI se restablece")
def sri_restablecido(sri):
    sri.disponible = True
    sri.intentos = 0


def enviar(client, ctx, nombre):
    inicio = time.perf_counter()
    ctx["respuesta"] = client.post(
        f"/api/v1/facturas/{ctx['factura']['id']}/enviar-sri", headers=cabecera(ctx, nombre)
    )
    ctx["duracion"] = time.perf_counter() - inicio


@given(parsers.parse('que el emisor "{nombre}" envió la factura al SRI'))
def ya_envio(client, ctx, nombre):
    enviar(client, ctx, nombre)


@when(parsers.parse('el emisor "{nombre}" envía la factura al SRI'))
def envia(client, ctx, nombre):
    enviar(client, ctx, nombre)


@then(parsers.parse("se hizo {intentos:d} intento de envío"))
def un_intento(ctx, sri, intentos):
    assert ctx["respuesta"].json()["intentosEnEsteEnvio"] == intentos
    assert sri.intentos == intentos


@then(parsers.parse("la respuesta tiene el código {codigo:d} en menos de {segundos:d} segundos"))
def codigo_a_tiempo(ctx, codigo, segundos):
    assert ctx["respuesta"].status_code == codigo, ctx["respuesta"].text
    assert ctx["duracion"] < segundos


@then(
    parsers.parse(
        "se hicieron {intentos:d} intentos de envío con esperas de {e1:d} y {e2:d} segundos"
    )
)
def intentos_con_esperas(ctx, sri, espera, intentos, e1, e2):
    assert ctx["respuesta"].json()["intentosEnEsteEnvio"] == intentos
    assert sri.intentos == intentos
    assert espera.esperas == [e1, e2]


@then("la factura sigue registrada con sus totales")
def factura_conservada(client, ctx):
    nombre = next(iter(ctx["emisores"]))
    respuesta = client.get(
        f"/api/v1/facturas/{ctx['factura']['id']}", headers=cabecera(ctx, nombre)
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["total"] == ctx["total_original"]


@then("el SRI recibió la factura una sola vez")
def recibida_una_vez(ctx, sri):
    assert sri.recibidos == [ctx["factura"]["claveAcceso"]]


@when(parsers.parse('se consulta la factura con la cuenta del emisor "{nombre}"'))
def consulta(client, ctx, nombre):
    ctx["respuesta"] = client.get(
        f"/api/v1/facturas/{ctx['factura']['id']}", headers=cabecera(ctx, nombre)
    )


@then(parsers.parse("la consulta muestra {intentos:d} intentos de envío"))
def muestra_intentos(ctx, intentos):
    assert ctx["respuesta"].json()["intentosEnvio"] == intentos
