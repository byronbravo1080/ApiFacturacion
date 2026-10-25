# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from facturaec_stubs.models.error import Error  # noqa: F401
from facturaec_stubs.models.error_validacion import ErrorValidacion  # noqa: F401
from facturaec_stubs.models.factura import Factura  # noqa: F401
from facturaec_stubs.models.factura_nueva import FacturaNueva  # noqa: F401
from facturaec_stubs.models.resultado_envio import ResultadoEnvio  # noqa: F401


def test_crear_factura(client: TestClient):
    """Test case for crear_factura

    Crear una factura
    """
    factura_nueva = facturaec_stubs.FacturaNueva()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/v1/facturas",
    #    headers=headers,
    #    json=factura_nueva,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_obtener_factura(client: TestClient):
    """Test case for obtener_factura

    Consultar una factura y su estado
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/v1/facturas/{facturaId}".format(facturaId=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_enviar_factura_sri(client: TestClient):
    """Test case for enviar_factura_sri

    Enviar una factura al SRI
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/v1/facturas/{facturaId}/enviar-sri".format(facturaId=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

