# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from facturaec_stubs.apis.auth_api_base import BaseAuthApi
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
from facturaec_stubs.models.registro_emisor import RegistroEmisor
from facturaec_stubs.models.token import Token

router = APIRouter()

ns_pkg = facturaec_stubs.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/api/v1/auth/registro",
    responses={
        201: {"model": Token, "description": "Emisor registrado."},
        409: {"model": Error, "description": "El RUC ya está registrado."},
        422: {"model": ErrorValidacion, "description": "Los datos de entrada no cumplen el contrato."},
    },
    tags=["Auth"],
    summary="Registrar un emisor",
    response_model_by_alias=True,
)
async def registrar_emisor(
    registro_emisor: RegistroEmisor = Body(..., description=""),
) -> Token:
    """Crea el emisor y su usuario administrador y devuelve un token de acceso (HU1). No requiere token."""
    if not BaseAuthApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthApi.subclasses[0]().registrar_emisor(registro_emisor)
