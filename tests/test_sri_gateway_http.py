"""Adaptador HTTP del microservicio validacion-SRI, sin red, y su efecto en el envío de facturas."""

import json

import httpx
import pytest

from ayudantes import cabecera, crear_factura, registrar
from facturaec.config import Settings
from facturaec.main import crear_app
from facturaec.sri_gateway import SriGatewayHttp, SriNoDisponibleError, SriRechazoError

URL = "https://proyecto.invalid/functions/v1/sri-gateway"
CLAVE = "0411202601990000000000110010010000000451234567816"


def gateway_que_responde(*args, **kwargs) -> SriGatewayHttp:
    return SriGatewayHttp(
        url=URL, transporte=httpx.MockTransport(lambda _: httpx.Response(*args, **kwargs))
    )


def test_autorizada_devuelve_el_numero_de_autorizacion():
    gateway = gateway_que_responde(
        200, json={"estado": "AUTORIZADA", "numeroAutorizacion": CLAVE, "claveAcceso": CLAVE}
    )
    assert gateway.enviar(CLAVE) == CLAVE


@pytest.mark.parametrize(("clave_api", "simular"), [("clave-anonima", True), ("", False)])
def test_envia_la_solicitud_del_contrato_del_microservicio(clave_api, simular):
    recibidas: list[httpx.Request] = []

    def responder(solicitud: httpx.Request) -> httpx.Response:
        recibidas.append(solicitud)
        return httpx.Response(200, json={"estado": "AUTORIZADA", "numeroAutorizacion": CLAVE})

    SriGatewayHttp(
        url=URL,
        clave_api=clave_api,
        simular_caida=simular,
        transporte=httpx.MockTransport(responder),
    ).enviar(CLAVE)

    solicitud = recibidas[0]
    assert solicitud.method == "POST"
    assert str(solicitud.url) == URL
    assert json.loads(solicitud.content) == {"claveAcceso": CLAVE, "simularCaida": simular}
    esperada = f"Bearer {clave_api}" if clave_api else None
    assert solicitud.headers.get("Authorization") == esperada


def test_rechazada_conserva_el_motivo():
    gateway = gateway_que_responde(422, json={"estado": "RECHAZADA", "error": "Clave inválida."})
    with pytest.raises(SriRechazoError, match="Clave inválida."):
        gateway.enviar(CLAVE)


@pytest.mark.parametrize(
    ("estado_http", "opciones"),
    [
        (503, {"json": {"estado": "PENDIENTE", "claveAcceso": CLAVE, "mensaje": "Caído"}}),
        (200, {"json": {"estado": "PENDIENTE", "claveAcceso": CLAVE, "mensaje": "Caído"}}),
        (200, {"json": {"estado": "AUTORIZADA"}}),
        (200, {"json": ["AUTORIZADA"]}),
        (200, {"text": "<html>no es JSON</html>"}),
        (401, {"json": {"msg": "Invalid JWT"}}),
        (404, {"json": {"error": "No existe"}}),
        (400, {"json": {"error": "Solicitud mal formada"}}),
        (500, {"json": {"error": "Error interno"}}),
        (504, {"text": "Gateway Timeout"}),
    ],
)
def test_cualquier_otra_respuesta_significa_no_disponible(estado_http, opciones):
    with pytest.raises(SriNoDisponibleError):
        gateway_que_responde(estado_http, **opciones).enviar(CLAVE)


@pytest.mark.parametrize(
    "error", [httpx.ConnectError("sin conexión"), httpx.ReadTimeout("tiempo agotado")]
)
def test_los_fallos_de_red_significan_no_disponible(error):
    def fallar(_: httpx.Request) -> httpx.Response:
        raise error

    with pytest.raises(SriNoDisponibleError):
        SriGatewayHttp(url=URL, transporte=httpx.MockTransport(fallar)).enviar(CLAVE)


def test_la_url_mal_escrita_significa_no_disponible():
    with pytest.raises(SriNoDisponibleError):
        SriGatewayHttp(url="sin-protocolo").enviar(CLAVE)


def test_el_rechazo_responde_422_sin_reintentar_ni_cambiar_la_factura(client, ctx, sri, espera):
    registrar(client, ctx, "A", "9990000001001")
    crear_factura(client, ctx, "A")
    factura_id = ctx["factura"]["id"]
    sri.rechazo = "Clave de acceso inválida."

    respuesta = client.post(f"/api/v1/facturas/{factura_id}/enviar-sri", headers=cabecera(ctx, "A"))

    assert respuesta.status_code == 422
    assert respuesta.json() == {
        "codigo": "SRI_RECHAZO",
        "mensaje": "El SRI rechazó la factura. Clave de acceso inválida.",
    }
    assert sri.intentos == 1
    assert espera.esperas == []
    factura = client.get(f"/api/v1/facturas/{factura_id}", headers=cabecera(ctx, "A")).json()
    assert factura == ctx["factura"]


def test_la_api_no_arranca_sin_la_url_del_microservicio(tmp_path):
    settings = Settings(database_url=f"sqlite:///{tmp_path / 'x.db'}", sri_gateway_url="")
    with pytest.raises(RuntimeError, match="SRI_GATEWAY_URL"):
        crear_app(settings=settings)


def test_la_api_configura_el_adaptador_desde_settings(tmp_path):
    settings = Settings(
        database_url=f"sqlite:///{tmp_path / 'x.db'}",
        sri_gateway_url=URL,
        supabase_anon_key="clave-anonima",
        sri_timeout_segundos=7,
        sri_simular_caida=True,
    )
    app = crear_app(settings=settings)
    assert app.state.sri_gateway == SriGatewayHttp(
        url=URL, clave_api="clave-anonima", timeout_segundos=7, simular_caida=True
    )
    app.state.engine.dispose()
