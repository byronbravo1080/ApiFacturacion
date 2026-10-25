"""Puerto SriGateway y adaptador simulado (ADR-003). No se contacta al SRI real."""

from dataclasses import dataclass, field
from typing import Protocol


class SriNoDisponibleError(Exception):
    """El SRI no respondió o falló al recibir el comprobante."""


class SriGateway(Protocol):
    def enviar(self, clave_acceso: str) -> str:
        """Envía el comprobante y devuelve el número de autorización."""
        ...


@dataclass
class SriGatewaySimulado:
    """Adaptador simulado. `disponible=False` reproduce la caída del SRI (E2)."""

    disponible: bool = True
    recibidos: list[str] = field(default_factory=list)
    intentos: int = 0

    def enviar(self, clave_acceso: str) -> str:
        self.intentos += 1
        if not self.disponible:
            raise SriNoDisponibleError("El SRI no respondió.")
        self.recibidos.append(clave_acceso)
        return clave_acceso  # en el SRI, el número de autorización coincide con la clave de acceso
