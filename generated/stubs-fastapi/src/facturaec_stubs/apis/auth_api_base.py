# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from facturaec_stubs.models.error import Error
from facturaec_stubs.models.error_validacion import ErrorValidacion
from facturaec_stubs.models.registro_emisor import RegistroEmisor
from facturaec_stubs.models.token import Token


class BaseAuthApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAuthApi.subclasses = BaseAuthApi.subclasses + (cls,)
    async def registrar_emisor(
        self,
        registro_emisor: RegistroEmisor,
    ) -> Token:
        """Crea el emisor y su usuario administrador y devuelve un token de acceso (HU1). No requiere token."""
        ...
