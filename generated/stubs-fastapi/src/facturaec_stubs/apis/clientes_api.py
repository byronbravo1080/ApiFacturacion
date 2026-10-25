# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from facturaec_stubs.apis.clientes_api_base import BaseClientesApi
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

from pydantic import Field
from typing_extensions import Annotated
from facturaec_stubs.models.cliente import Cliente
from facturaec_stubs.models.cliente_nuevo import ClienteNuevo
from facturaec_stubs.models.error import Error
from facturaec_stubs.models.error_validacion import ErrorValidacion
from facturaec_stubs.models.extra_models import TokenModel  # noqa: F401
from facturaec_stubs.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = facturaec_stubs.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/api/v1/clientes",
    responses={
        201: {"model": Cliente, "description": "Cliente registrado."},
        401: {"model": Error, "description": "Falta el token o no es válido (E1)."},
        422: {"model": ErrorValidacion, "description": "Los datos de entrada no cumplen el contrato."},
    },
    tags=["Clientes"],
    summary="Registrar un cliente",
    response_model_by_alias=True,
)
async def registrar_cliente(
    cliente_nuevo: ClienteNuevo = Body(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Cliente:
    """Registra un cliente del emisor autenticado (HU2, E1)."""
    if not BaseClientesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseClientesApi.subclasses[0]().registrar_cliente(cliente_nuevo)


@router.get(
    "/api/v1/clientes/{clienteId}",
    responses={
        200: {"model": Cliente, "description": "Datos del cliente."},
        401: {"model": Error, "description": "Falta el token o no es válido (E1)."},
        404: {"model": Error, "description": "El recurso no existe o pertenece a otro emisor; no se revela cuál de los dos casos ocurre (E1)."},
    },
    tags=["Clientes"],
    summary="Consultar un cliente",
    response_model_by_alias=True,
)
async def obtener_cliente(
    clienteId: Annotated[int, Field(ge=1, description="Identificador del cliente.")] = Path(..., description="Identificador del cliente.", ge=1),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Cliente:
    """Devuelve un cliente del emisor autenticado. Responde 404 si no existe o pertenece a otro emisor, sin revelar cuál de los dos casos ocurre (E1)."""
    if not BaseClientesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseClientesApi.subclasses[0]().obtener_cliente(clienteId)
