# coding: utf-8

from fastapi.testclient import TestClient


from facturaec_stubs.models.error import Error  # noqa: F401
from facturaec_stubs.models.error_validacion import ErrorValidacion  # noqa: F401
from facturaec_stubs.models.registro_emisor import RegistroEmisor  # noqa: F401
from facturaec_stubs.models.token import Token  # noqa: F401


def test_registrar_emisor(client: TestClient):
    """Test case for registrar_emisor

    Registrar un emisor
    """
    registro_emisor = facturaec_stubs.RegistroEmisor()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/v1/auth/registro",
    #    headers=headers,
    #    json=registro_emisor,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

