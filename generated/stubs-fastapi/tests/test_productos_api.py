# coding: utf-8

from fastapi.testclient import TestClient


from facturaec_stubs.models.error import Error  # noqa: F401
from facturaec_stubs.models.error_validacion import ErrorValidacion  # noqa: F401
from facturaec_stubs.models.producto import Producto  # noqa: F401
from facturaec_stubs.models.producto_nuevo import ProductoNuevo  # noqa: F401


def test_registrar_producto(client: TestClient):
    """Test case for registrar_producto

    Registrar un producto
    """
    producto_nuevo = facturaec_stubs.ProductoNuevo()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/v1/productos",
    #    headers=headers,
    #    json=producto_nuevo,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

