"""Esquemas de entrada y salida.

Reflejan components/schemas de api/openapi.yaml, que es la fuente de verdad.
"""

from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_serializer
from pydantic.alias_generators import to_camel

MONTO = r"^[0-9]{1,10}\.[0-9]{2}$"


class Esquema(BaseModel):
    """Base: nombres en camelCase en el JSON, como en el contrato."""

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=True, extra="forbid"
    )


class Estado(Esquema):
    estado: str


class RegistroEmisor(Esquema):
    ruc: str = Field(pattern=r"^[0-9]{10}001$")
    razon_social: str = Field(min_length=1, max_length=300)
    clave: str = Field(min_length=8)


class Token(Esquema):
    access_token: str
    token_type: Literal["bearer"] = "bearer"  # noqa: S105 (tipo de token, no una clave)
    emisor_id: int


class ClienteNuevo(Esquema):
    tipo_identificacion: Literal["CEDULA", "RUC", "PASAPORTE"]
    identificacion: str = Field(min_length=3, max_length=20)
    razon_social: str = Field(min_length=1, max_length=300)
    direccion: str | None = Field(default=None, max_length=300)


class Cliente(ClienteNuevo):
    id: int


class ProductoNuevo(Esquema):
    codigo: str = Field(min_length=1, max_length=25)
    descripcion: str = Field(min_length=1, max_length=300)
    precio_unitario: str = Field(pattern=MONTO)
    tarifa_iva: Literal[0, 5, 15]


class Producto(Esquema):
    id: int
    codigo: str
    descripcion: str
    precio_unitario: Decimal
    tarifa_iva: int

    @field_serializer("precio_unitario")
    def _monto(self, valor: Decimal) -> str:
        return f"{valor:.2f}"


class DetalleNuevo(Esquema):
    producto_id: int = Field(ge=1)
    cantidad: int = Field(ge=1, le=100_000)


class FacturaNueva(Esquema):
    cliente_id: int = Field(ge=1)
    detalles: list[DetalleNuevo] = Field(min_length=1, max_length=100)


class Detalle(Esquema):
    producto_id: int
    descripcion: str
    cantidad: int
    precio_unitario: Decimal
    tarifa_iva: int
    subtotal: Decimal
    iva: Decimal

    @field_serializer("precio_unitario", "subtotal", "iva")
    def _monto(self, valor: Decimal) -> str:
        return f"{valor:.2f}"


class Factura(Esquema):
    id: int
    numero: str
    clave_acceso: str
    fecha_emision: date
    cliente_id: int
    estado: Literal["CREADA", "PENDIENTE", "AUTORIZADA"]
    subtotal: Decimal
    iva: Decimal
    total: Decimal
    intentos_envio: int
    detalles: list[Detalle]

    @field_serializer("subtotal", "iva", "total")
    def _monto(self, valor: Decimal) -> str:
        return f"{valor:.2f}"


class ResultadoEnvio(Esquema):
    factura_id: int
    estado: Literal["CREADA", "PENDIENTE", "AUTORIZADA"]
    intentos_en_este_envio: int
    mensaje: str
    numero_autorizacion: str | None = None
