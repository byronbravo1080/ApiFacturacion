# coding: utf-8

from fastapi.testclient import TestClient


from typing import Any  # noqa: F401
from facturaec_stubs.models.estado import Estado  # noqa: F401


def test_verificar_estado(client: TestClient):
    """Test case for verificar_estado

    Verificar el estado del servicio
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/health",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

