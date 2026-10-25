"""Modelo de datos. Cada tabla de negocio lleva emisor_id para aislar a los emisores (E1)."""

from datetime import date
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from facturaec.database import Base


class Emisor(Base):
    __tablename__ = "emisor"

    id: Mapped[int] = mapped_column(primary_key=True)
    ruc: Mapped[str] = mapped_column(String(13), unique=True)
    razon_social: Mapped[str] = mapped_column(String(300))
    clave_hash: Mapped[str] = mapped_column(String(200))
    ultimo_secuencial: Mapped[int] = mapped_column(default=0)


class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True)
    emisor_id: Mapped[int] = mapped_column(ForeignKey("emisor.id"), index=True)
    tipo_identificacion: Mapped[str] = mapped_column(String(20))
    identificacion: Mapped[str] = mapped_column(String(20))
    razon_social: Mapped[str] = mapped_column(String(300))
    direccion: Mapped[str | None] = mapped_column(String(300))


class Producto(Base):
    __tablename__ = "producto"

    id: Mapped[int] = mapped_column(primary_key=True)
    emisor_id: Mapped[int] = mapped_column(ForeignKey("emisor.id"), index=True)
    codigo: Mapped[str] = mapped_column(String(25))
    descripcion: Mapped[str] = mapped_column(String(300))
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    tarifa_iva: Mapped[int]


class Factura(Base):
    __tablename__ = "factura"
    __table_args__ = (
        # Red de seguridad de E6 (ADR-002): nunca dos facturas con el mismo número.
        UniqueConstraint(
            "emisor_id",
            "establecimiento",
            "punto_emision",
            "secuencial",
            name="uq_factura_secuencial",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    emisor_id: Mapped[int] = mapped_column(ForeignKey("emisor.id"), index=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    establecimiento: Mapped[str] = mapped_column(String(3))
    punto_emision: Mapped[str] = mapped_column(String(3))
    secuencial: Mapped[int]
    clave_acceso: Mapped[str] = mapped_column(String(49), unique=True)
    fecha_emision: Mapped[date]
    estado: Mapped[str] = mapped_column(String(20), default="CREADA")
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    iva: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    intentos_envio: Mapped[int] = mapped_column(default=0)
    numero_autorizacion: Mapped[str | None] = mapped_column(String(49))

    detalles: Mapped[list["DetalleFactura"]] = relationship(
        back_populates="factura", cascade="all, delete-orphan", lazy="selectin"
    )

    @property
    def numero(self) -> str:
        return f"{self.establecimiento}-{self.punto_emision}-{self.secuencial:09d}"


class DetalleFactura(Base):
    __tablename__ = "detalle_factura"

    id: Mapped[int] = mapped_column(primary_key=True)
    factura_id: Mapped[int] = mapped_column(ForeignKey("factura.id"), index=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("producto.id"))
    descripcion: Mapped[str] = mapped_column(String(300))
    cantidad: Mapped[int]
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    tarifa_iva: Mapped[int]
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    iva: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    factura: Mapped[Factura] = relationship(back_populates="detalles")
