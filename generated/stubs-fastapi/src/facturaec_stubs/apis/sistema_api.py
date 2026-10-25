# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from facturaec_stubs.apis.sistema_api_base import BaseSistemaApi
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

from typing import Any
from facturaec_stubs.models.estado import Estado

router = APIRouter()

ns_pkg = facturaec_stubs.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/health",
    responses={
        200: {"model": Estado, "description": "El servicio está activo."},
        503: {"description": "El servicio no puede atender solicitudes."},
    },
    tags=["Sistema"],
    summary="Verificar el estado del servicio",
    response_model_by_alias=True,
)
async def verificar_estado(
) -> Estado:
    """Usado por la plataforma de despliegue para reiniciar la API si no responde (riesgo 11.2 del dossier). No requiere token."""
    if not BaseSistemaApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSistemaApi.subclasses[0]().verificar_estado()
