"""Pasos de Gherkin compartidos por las tres características."""

from pytest_bdd import given, parsers, then, when

from ayudantes import cabecera, crear_cliente, crear_factura, registrar


@given(parsers.parse('que el emisor "{nombre}" está registrado con RUC "{ruc}"'))
def emisor_registrado(client, ctx, nombre, ruc):
    assert registrar(client, ctx, nombre, ruc).status_code == 201


@when(parsers.parse('se registra el emisor "{nombre}" con RUC "{ruc}"'))
def se_registra_emisor(client, ctx, nombre, ruc):
    ctx["respuesta"] = registrar(client, ctx, nombre, ruc)


@given(parsers.parse('que el emisor "{nombre}" tiene un {recurso} registrado'))
def tiene_recurso(client, ctx, nombre, recurso):
    if recurso == "cliente":
        assert crear_cliente(client, ctx, nombre).status_code == 201
        ctx["recurso_id"] = ctx["cliente_id"]
    elif recurso == "factura":
        assert crear_factura(client, ctx, nombre).status_code == 201
        ctx["recurso_id"] = ctx["factura"]["id"]
    else:
        raise AssertionError(f"Recurso no previsto en los pasos: {recurso}")


@then(parsers.parse("la respuesta tiene el código {codigo:d}"))
def codigo_respuesta(ctx, codigo):
    respuesta = ctx["respuesta"]
    assert respuesta.status_code == codigo, respuesta.text


@then(parsers.parse('la factura queda en estado "{estado}"'))
def factura_en_estado(client, ctx, estado):
    nombre = next(iter(ctx["emisores"]))
    respuesta = client.get(
        f"/api/v1/facturas/{ctx['factura']['id']}", headers=cabecera(ctx, nombre)
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == estado
