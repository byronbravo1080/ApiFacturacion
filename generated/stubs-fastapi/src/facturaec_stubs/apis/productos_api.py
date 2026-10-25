# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from facturaec_stubs.apis.productos_api_base import BaseProductosApi
import facturaec_stubs.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from facturaec_stubs.models.error import Error
from facturaec_stubs.models.error_validacion import ErrorValidacion
from facturaec_stubs.models.producto import Producto
from facturaec_stubs.models.producto_nuevo import ProductoNuevo
from facturaec_stubs.models.extra_models import TokenModel  # noqa: F401
from facturaec_stubs.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = facturaec_stubs.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/api/v1/productos",
    responses={
        201: {"model": Producto, "description": "Producto registrado."},
        401: {"model": Error, "description": "Falta el token o no es válido (E1)."},
        422: {"model": ErrorValidacion, "description": "Los datos de entrada no cumplen el contrato."},
    },
    tags=["Productos"],
    summary="Registrar un producto",
    response_model_by_alias=True,
)
async def registrar_producto(
    producto_nuevo: ProductoNuevo = Body(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Producto:
    """Registra un producto con su precio unitario y su tarifa de IVA (HU3)."""
    if not BaseProductosApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProductosApi.subclasses[0]().registrar_producto(producto_nuevo)
