# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from facturaec_stubs.apis.facturas_api_base import BaseFacturasApi
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
from facturaec_stubs.models.error import Error
from facturaec_stubs.models.error_validacion import ErrorValidacion
from facturaec_stubs.models.factura import Factura
from facturaec_stubs.models.factura_nueva import FacturaNueva
from facturaec_stubs.models.resultado_envio import ResultadoEnvio
from facturaec_stubs.models.extra_models import TokenModel  # noqa: F401
from facturaec_stubs.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = facturaec_stubs.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/api/v1/facturas",
    responses={
        201: {"model": Factura, "description": "Factura creada."},
        401: {"model": Error, "description": "Falta el token o no es válido (E1)."},
        404: {"model": Error, "description": "El recurso no existe o pertenece a otro emisor; no se revela cuál de los dos casos ocurre (E1)."},
        422: {"model": ErrorValidacion, "description": "Los datos de entrada no cumplen el contrato."},
    },
    tags=["Facturas"],
    summary="Crear una factura",
    response_model_by_alias=True,
)
async def crear_factura(
    factura_nueva: FacturaNueva = Body(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Factura:
    """Calcula subtotal, IVA y total; asigna el siguiente secuencial del emisor bajo bloqueo de fila y genera la clave de acceso de 49 dígitos (HU4, HU5, E6). La factura queda en estado CREADA. Responde 404 si el cliente o algún producto no existen o pertenecen a otro emisor (E1). """
    if not BaseFacturasApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseFacturasApi.subclasses[0]().crear_factura(factura_nueva)


@router.get(
    "/api/v1/facturas/{facturaId}",
    responses={
        200: {"model": Factura, "description": "Datos de la factura."},
        401: {"model": Error, "description": "Falta el token o no es válido (E1)."},
        404: {"model": Error, "description": "El recurso no existe o pertenece a otro emisor; no se revela cuál de los dos casos ocurre (E1)."},
    },
    tags=["Facturas"],
    summary="Consultar una factura y su estado",
    response_model_by_alias=True,
)
async def obtener_factura(
    facturaId: Annotated[int, Field(ge=1, description="Identificador de la factura.")] = Path(..., description="Identificador de la factura.", ge=1),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Factura:
    """Devuelve la factura, su estado de autorización y el total de intentos de envío (HU7). Responde 404 si es de otro emisor (E1)."""
    if not BaseFacturasApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseFacturasApi.subclasses[0]().obtener_factura(facturaId)


@router.post(
    "/api/v1/facturas/{facturaId}/enviar-sri",
    responses={
        200: {"model": ResultadoEnvio, "description": "Factura autorizada por el SRI."},
        202: {"model": ResultadoEnvio, "description": "El SRI no respondió tras 3 intentos; la factura queda PENDIENTE para reenviarla después."},
        401: {"model": Error, "description": "Falta el token o no es válido (E1)."},
        404: {"model": Error, "description": "El recurso no existe o pertenece a otro emisor; no se revela cuál de los dos casos ocurre (E1)."},
        409: {"model": Error, "description": "La factura ya está autorizada; no se reenvía para evitar una doble autorización (riesgo 11.2 del dossier)."},
    },
    tags=["Facturas"],
    summary="Enviar una factura al SRI",
    response_model_by_alias=True,
)
async def enviar_factura_sri(
    facturaId: Annotated[int, Field(ge=1, description="Identificador de la factura.")] = Path(..., description="Identificador de la factura.", ge=1),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> ResultadoEnvio:
    """Envía la factura al SRI mediante el adaptador SriGateway (HU6, E2). Política de reintentos: hasta 3 intentos por solicitud, con esperas de 1 s y 2 s, y una respuesta en 60 s o menos. Si el SRI no responde, la factura se conserva en estado PENDIENTE y se responde 202. Solo se envían facturas CREADAS o PENDIENTES; una factura AUTORIZADA responde 409 para evitar una doble autorización (riesgo 11.2 del dossier). El tiempo máximo de 15 s por intento (E8) queda para una versión posterior. """
    if not BaseFacturasApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseFacturasApi.subclasses[0]().enviar_factura_sri(facturaId)
