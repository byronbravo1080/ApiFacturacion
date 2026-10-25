"""Casos de uso de facturación.

Totales con IVA (HU4), numeración (HU5, E6) y envío al SRI (HU6, E2).
"""

import secrets
from collections import defaultdict
from collections.abc import Callable
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import Session

from facturaec import clave_acceso
from facturaec.config import Settings
from facturaec.errors import ApiError, no_encontrado
from facturaec.models import Cliente, DetalleFactura, Emisor, Factura, Producto
from facturaec.schemas import FacturaNueva
from facturaec.sri_gateway import SriGateway, SriNoDisponibleError

CENTAVO = Decimal("0.01")
MAX_INTENTOS = 3
ESPERAS_SEGUNDOS = (1, 2)  # espera exponencial entre intentos (E2)
ZONA_ECUADOR = ZoneInfo("America/Guayaquil")


def _redondear(valor: Decimal) -> Decimal:
    return valor.quantize(CENTAVO, rounding=ROUND_HALF_UP)


def calcular_linea(precio: Decimal, cantidad: int, tarifa: int) -> tuple[Decimal, Decimal]:
    """Subtotal e IVA de una línea, redondeados a centavos."""
    subtotal = _redondear(precio * cantidad)
    return subtotal, _redondear(subtotal * tarifa / Decimal(100))


def obtener_propio(db: Session, modelo: type, recurso_id: int, emisor_id: int):
    """Busca un recurso del emisor; si no existe o es ajeno, responde el mismo 404 (E1)."""
    recurso = db.get(modelo, recurso_id)
    if recurso is None or recurso.emisor_id != emisor_id:
        raise no_encontrado()
    return recurso


def crear_factura(db: Session, emisor_id: int, datos: FacturaNueva, settings: Settings) -> Factura:
    obtener_propio(db, Cliente, datos.cliente_id, emisor_id)

    detalles: list[DetalleFactura] = []
    base_por_tarifa: dict[int, Decimal] = defaultdict(Decimal)
    for linea in datos.detalles:
        producto: Producto = obtener_propio(db, Producto, linea.producto_id, emisor_id)
        subtotal, iva = calcular_linea(
            producto.precio_unitario, linea.cantidad, producto.tarifa_iva
        )
        base_por_tarifa[producto.tarifa_iva] += subtotal
        detalles.append(
            DetalleFactura(
                producto_id=producto.id,
                descripcion=producto.descripcion,
                cantidad=linea.cantidad,
                precio_unitario=producto.precio_unitario,
                tarifa_iva=producto.tarifa_iva,
                subtotal=subtotal,
                iva=iva,
            )
        )
    subtotal_total = sum(base_por_tarifa.values(), Decimal("0"))
    # El IVA total se calcula por tarifa sobre la base acumulada (bloque totalConImpuestos).
    iva_total = sum(
        (_redondear(base * tarifa / Decimal(100)) for tarifa, base in base_por_tarifa.items()),
        Decimal("0"),
    )

    # Asignación del secuencial bajo bloqueo de la fila del emisor (ADR-002, E6).
    # El incremento y la inserción van en la misma transacción: si algo falla, no queda un salto.
    # populate_existing obliga a releer la fila ya bloqueada: el emisor está en la sesión desde la
    # autenticación y, sin esta opción, SQLAlchemy reutiliza el valor viejo de ultimo_secuencial
    # (defecto detectado por la prueba concurrente CA5.3 contra PostgreSQL).
    emisor = db.execute(
        select(Emisor)
        .where(Emisor.id == emisor_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    ).scalar_one()
    emisor.ultimo_secuencial += 1
    secuencial = emisor.ultimo_secuencial
    fecha = datetime.now(ZONA_ECUADOR).date()

    factura = Factura(
        emisor_id=emisor_id,
        cliente_id=datos.cliente_id,
        establecimiento=settings.establecimiento,
        punto_emision=settings.punto_emision,
        secuencial=secuencial,
        clave_acceso=clave_acceso.generar(
            fecha=fecha,
            ruc=emisor.ruc,
            ambiente=settings.ambiente_sri,
            establecimiento=settings.establecimiento,
            punto_emision=settings.punto_emision,
            secuencial=secuencial,
            codigo_numerico=secrets.randbelow(10**8),
        ),
        fecha_emision=fecha,
        estado="CREADA",
        subtotal=subtotal_total,
        iva=iva_total,
        total=subtotal_total + iva_total,
        intentos_envio=0,
        detalles=detalles,
    )
    db.add(factura)
    db.commit()
    return factura


def enviar_al_sri(
    db: Session,
    emisor_id: int,
    factura_id: int,
    gateway: SriGateway,
    esperar: Callable[[float], None],
) -> tuple[Factura, int, str]:
    """Envía con hasta 3 intentos.

    Devuelve la factura, los intentos de esta solicitud y un mensaje.
    """
    factura: Factura = obtener_propio(db, Factura, factura_id, emisor_id)
    if factura.estado == "AUTORIZADA":
        raise ApiError(409, "CONFLICTO", "La factura ya está autorizada.")

    for intento in range(1, MAX_INTENTOS + 1):
        factura.intentos_envio += 1
        try:
            factura.numero_autorizacion = gateway.enviar(factura.clave_acceso)
        except SriNoDisponibleError:
            if intento < MAX_INTENTOS:
                esperar(ESPERAS_SEGUNDOS[intento - 1])
            continue
        factura.estado = "AUTORIZADA"
        db.commit()
        return factura, intento, "Factura autorizada por el SRI."

    # La factura se conserva con sus datos; solo cambia el estado (0 facturas perdidas, E2).
    factura.estado = "PENDIENTE"
    db.commit()
    return factura, MAX_INTENTOS, "El SRI no respondió; la factura quedó PENDIENTE para reenviarla."
