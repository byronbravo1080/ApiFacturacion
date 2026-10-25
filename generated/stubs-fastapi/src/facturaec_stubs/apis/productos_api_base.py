# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from facturaec_stubs.models.error import Error
from facturaec_stubs.models.error_validacion import ErrorValidacion
from facturaec_stubs.models.producto import Producto
from facturaec_stubs.models.producto_nuevo import ProductoNuevo
from facturaec_stubs.security_api import get_token_bearerAuth

class BaseProductosApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseProductosApi.subclasses = BaseProductosApi.subclasses + (cls,)
    async def registrar_producto(
        self,
        producto_nuevo: ProductoNuevo,
    ) -> Producto:
        """Registra un producto con su precio unitario y su tarifa de IVA (HU3)."""
        ...
