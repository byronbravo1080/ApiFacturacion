# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field
from typing_extensions import Annotated
from facturaec_stubs.models.cliente import Cliente
from facturaec_stubs.models.cliente_nuevo import ClienteNuevo
from facturaec_stubs.models.error import Error
from facturaec_stubs.models.error_validacion import ErrorValidacion
from facturaec_stubs.security_api import get_token_bearerAuth

class BaseClientesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseClientesApi.subclasses = BaseClientesApi.subclasses + (cls,)
    async def registrar_cliente(
        self,
        cliente_nuevo: ClienteNuevo,
    ) -> Cliente:
        """Registra un cliente del emisor autenticado (HU2, E1)."""
        ...


    async def obtener_cliente(
        self,
        clienteId: Annotated[int, Field(ge=1, description="Identificador del cliente.")],
    ) -> Cliente:
        """Devuelve un cliente del emisor autenticado. Responde 404 si no existe o pertenece a otro emisor, sin revelar cuál de los dos casos ocurre (E1)."""
        ...
