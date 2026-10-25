# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from facturaec_stubs.models.cliente import Cliente  # noqa: F401
from facturaec_stubs.models.cliente_nuevo import ClienteNuevo  # noqa: F401
from facturaec_stubs.models.error import Error  # noqa: F401
from facturaec_stubs.models.error_validacion import ErrorValidacion  # noqa: F401


def test_registrar_cliente(client: TestClient):
    """Test case for registrar_cliente

    Registrar un cliente
    """
    cliente_nuevo = facturaec_stubs.ClienteNuevo()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/v1/clientes",
    #    headers=headers,
    #    json=cliente_nuevo,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_obtener_cliente(client: TestClient):
    """Test case for obtener_cliente

    Consultar un cliente
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/v1/clientes/{clienteId}".format(clienteId=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

