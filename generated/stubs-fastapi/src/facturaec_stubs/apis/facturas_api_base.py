# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field
from typing_extensions import Annotated
from facturaec_stubs.models.error import Error
from facturaec_stubs.models.error_validacion import ErrorValidacion
from facturaec_stubs.models.factura import Factura
from facturaec_stubs.models.factura_nueva import FacturaNueva
from facturaec_stubs.models.resultado_envio import ResultadoEnvio
from facturaec_stubs.security_api import get_token_bearerAuth

class BaseFacturasApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseFacturasApi.subclasses = BaseFacturasApi.subclasses + (cls,)
    async def crear_factura(
        self,
        factura_nueva: FacturaNueva,
    ) -> Factura:
        """Calcula subtotal, IVA y total; asigna el siguiente secuencial del emisor bajo bloqueo de fila y genera la clave de acceso de 49 dígitos (HU4, HU5, E6). La factura queda en estado CREADA. Responde 404 si el cliente o algún producto no existen o pertenecen a otro emisor (E1). """
        ...


    async def obtener_factura(
        self,
        facturaId: Annotated[int, Field(ge=1, description="Identificador de la factura.")],
    ) -> Factura:
        """Devuelve la factura, su estado de autorización y el total de intentos de envío (HU7). Responde 404 si es de otro emisor (E1)."""
        ...


    async def enviar_factura_sri(
        self,
        facturaId: Annotated[int, Field(ge=1, description="Identificador de la factura.")],
    ) -> ResultadoEnvio:
        """Envía la factura al SRI mediante el adaptador SriGateway (HU6, E2). Política de reintentos: hasta 3 intentos por solicitud, con esperas de 1 s y 2 s, y una respuesta en 60 s o menos. Si el SRI no responde, la factura se conserva en estado PENDIENTE y se responde 202. Solo se envían facturas CREADAS o PENDIENTES; una factura AUTORIZADA responde 409 para evitar una doble autorización (riesgo 11.2 del dossier). El tiempo máximo de 15 s por intento (E8) queda para una versión posterior. """
        ...
