"""Puerto SriGateway y adaptador HTTP hacia el microservicio validacion-SRI (ADR-003)."""

import logging
from dataclasses import dataclass
from typing import Protocol

import httpx

logger = logging.getLogger(__name__)


class SriNoDisponibleError(Exception):
    """El SRI no respondió o falló al recibir el comprobante."""


class SriRechazoError(Exception):
    """El SRI rechazó el comprobante: reenviarlo sin corregirlo no cambia el resultado."""


class SriGateway(Protocol):
    def enviar(self, clave_acceso: str) -> str:
        """Envía el comprobante y devuelve el número de autorización."""
        ...


@dataclass
class SriGatewayHttp:
    """Adaptador del microservicio. Solo AUTORIZADA y RECHAZADA son respuestas definitivas.

    Cualquier otra respuesta (caída, tiempo agotado, credencial o URL incorrectas) se trata como
    SRI no disponible, para que la factura se conserve PENDIENTE (E2).
    """

    url: str
    clave_api: str = ""
    timeout_segundos: float = 15
    simular_caida: bool = False
    transporte: httpx.BaseTransport | None = None  # permite sustituir la red en las pruebas

    def enviar(self, clave_acceso: str) -> str:
        cabeceras = {"Authorization": f"Bearer {self.clave_api}"} if self.clave_api else {}
        solicitud = {"claveAcceso": clave_acceso, "simularCaida": self.simular_caida}
        try:
            with httpx.Client(transport=self.transporte, timeout=self.timeout_segundos) as cliente:
                respuesta = cliente.post(self.url, json=solicitud, headers=cabeceras)
            cuerpo = respuesta.json()
        except (httpx.HTTPError, httpx.InvalidURL, ValueError) as error:
            logger.warning("No se obtuvo respuesta válida de sri-gateway: %s", type(error).__name__)
            raise SriNoDisponibleError("El SRI no respondió.") from error

        estado = cuerpo.get("estado") if isinstance(cuerpo, dict) else None
        if respuesta.status_code == 200 and estado == "AUTORIZADA":
            numero = cuerpo.get("numeroAutorizacion")
            if isinstance(numero, str) and numero:
                return numero
        if respuesta.status_code == 422 and estado == "RECHAZADA":
            raise SriRechazoError(str(cuerpo.get("error", "Comprobante rechazado.")))

        logger.warning("sri-gateway respondió HTTP %s, estado %s", respuesta.status_code, estado)
        raise SriNoDisponibleError("El SRI no respondió.")
