# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any
from facturaec_stubs.models.estado import Estado


class BaseSistemaApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseSistemaApi.subclasses = BaseSistemaApi.subclasses + (cls,)
    async def verificar_estado(
        self,
    ) -> Estado:
        """Usado por la plataforma de despliegue para reiniciar la API si no responde (riesgo 11.2 del dossier). No requiere token."""
        ...
