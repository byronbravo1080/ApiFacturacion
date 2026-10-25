"""Pruebas derivadas de tests/features/facturacion.feature (HU3, HU4, HU5 · E6)."""

from concurrent.futures import ThreadPoolExecutor

from pytest_bdd import given, parsers, scenarios, then, when
from sqlalchemy import func, select

from ayudantes import cabecera, crear_factura, crear_producto
from facturaec.models import Factura

scenarios("facturacion.feature")


def modulo11_independiente(digitos: str) -> int:
    """Implementación propia de la prueba, distinta de la del código, para no validarse a sí mismo."""
    total, peso = 0, 2
    for digito in reversed(digitos):
        total += int(digito) * peso
        peso = 2 if peso == 7 else peso + 1
    verificador = 11 - total % 11
    return 0 if verificador == 11 else 1 if verificador == 10 else verificador


@when(
    parsers.parse(
        'el emisor "{nombre}" registra un producto con precio "{precio}" y tarifa de IVA {tarifa:d}'
    )
)
def registra_producto(client, ctx, nombre, precio, tarifa):
    ctx["respuesta"] = crear_producto(client, ctx, nombre, precio, tarifa)


@given(
    parsers.parse(
        'que el emisor "{nombre}" tiene un producto con precio "{precio}" y tarifa de IVA {tarifa:d}'
    )
)
def tiene_producto(client, ctx, nombre, precio, tarifa):
    assert crear_producto(client, ctx, nombre, precio, tarifa).status_code == 201


@when(
    parsers.parse('el emisor "{nombre}" crea una factura con {cantidad:d} unidades de ese producto')
)
def crea_factura_cantidad(client, ctx, nombre, cantidad):
    ctx["respuesta"] = crear_factura(client, ctx, nombre, cantidad)


@then(parsers.parse('la factura tiene subtotal "{subtotal}", IVA "{iva}" y total "{total}"'))
def totales(ctx, subtotal, iva, total):
    factura = ctx["respuesta"].json()
    assert (factura["subtotal"], factura["iva"], factura["total"]) == (subtotal, iva, total)


@when(parsers.parse('el emisor "{nombre}" crea {cantidad:d} facturas seguidas'))
def crea_varias(client, ctx, nombre, cantidad):
    ctx["numeros"] = []
    for _ in range(cantidad):
        respuesta = crear_factura(client, ctx, nombre)
        assert respuesta.status_code == 201
        ctx["numeros"].append(respuesta.json()["numero"])


@then(parsers.parse('los números de factura son "{n1}", "{n2}" y "{n3}"'))
def numeros_consecutivos(ctx, n1, n2, n3):
    assert ctx["numeros"] == [n1, n2, n3]


@when(parsers.parse('el emisor "{nombre}" crea una factura'))
def crea_una(client, ctx, nombre):
    ctx["respuesta"] = crear_factura(client, ctx, nombre)
    assert ctx["respuesta"].status_code == 201


@then("la clave de acceso tiene 49 dígitos")
def clave_49(ctx):
    clave = ctx["factura"]["claveAcceso"]
    assert len(clave) == 49 and clave.isdigit()


@then("su dígito verificador módulo 11 es correcto")
def clave_modulo11(ctx):
    clave = ctx["factura"]["claveAcceso"]
    assert modulo11_independiente(clave[:48]) == int(clave[48])


@then("la clave de acceso contiene el RUC del emisor y el secuencial de la factura")
def clave_contiene_ruc_y_secuencial(ctx):
    clave, numero = ctx["factura"]["claveAcceso"], ctx["factura"]["numero"]
    ruc = next(iter(ctx["emisores"].values()))["ruc"]
    assert clave[8:10] == "01"  # tipo de comprobante: factura
    assert clave[10:23] == ruc
    assert clave[24:30] == numero[0:3] + numero[4:7]  # establecimiento y punto de emisión
    assert clave[30:39] == numero[8:]  # secuencial de 9 dígitos


@when(
    parsers.parse(
        'se envían {total:d} solicitudes concurrentes de creación de factura del emisor "{nombre}"'
    )
)
def solicitudes_concurrentes(client, ctx, total, nombre):
    crear_producto(client, ctx, nombre)
    cuerpo = {
        "clienteId": ctx["cliente_id"],
        "detalles": [{"productoId": ctx["producto_id"], "cantidad": 1}],
    }
    encabezado = cabecera(ctx, nombre)

    def emitir(_):
        return client.post("/api/v1/facturas", headers=encabezado, json=cuerpo).status_code

    with ThreadPoolExecutor(max_workers=50) as hilos:
        ctx["codigos"] = list(hilos.map(emitir, range(total)))


@then(parsers.parse("se crean {total:d} facturas"))
def se_crean(app, ctx, total):
    assert ctx["codigos"].count(201) == total, {
        c: ctx["codigos"].count(c) for c in set(ctx["codigos"])
    }
    with app.state.sessionmaker() as sesion:
        assert sesion.scalar(select(func.count()).select_from(Factura)) == total


@then(parsers.parse("hay {cantidad:d} secuenciales duplicados"))
def sin_duplicados(app, cantidad):
    with app.state.sessionmaker() as sesion:
        secuenciales = list(sesion.scalars(select(Factura.secuencial)))
    assert len(secuenciales) - len(set(secuenciales)) == cantidad


@then(parsers.parse("hay {cantidad:d} saltos en la numeración"))
def sin_saltos(app, cantidad):
    with app.state.sessionmaker() as sesion:
        secuenciales = sorted(sesion.scalars(select(Factura.secuencial)))
    saltos = sum(1 for a, b in zip(secuenciales, secuenciales[1:], strict=False) if b - a > 1)
    assert secuenciales[0] == 1 and saltos == cantidad
