"""Rutas HTTP. Cada función corresponde a un operationId de api/openapi.yaml.

Las firmas, rutas y códigos de respuesta se tomaron de los stubs generados por OpenAPI Generator
(generated/stubs-fastapi). La implementación se escribe aquí porque el stub generado no entrega
el token a la implementación, y sin el token no se puede filtrar por emisor (E1).
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from facturaec import facturacion
from facturaec.database import get_db
from facturaec.errors import ApiError
from facturaec.models import Cliente as ClienteDB
from facturaec.models import Emisor
from facturaec.models import Factura as FacturaDB
from facturaec.models import Producto as ProductoDB
from facturaec.schemas import (
    Cliente,
    ClienteNuevo,
    Estado,
    Factura,
    FacturaNueva,
    Producto,
    ProductoNuevo,
    RegistroEmisor,
    ResultadoEnvio,
    Token,
)
from facturaec.security import crear_token, emisor_actual, hash_clave

router = APIRouter()

# Dependencias con Annotated (forma recomendada por FastAPI; evita llamadas en valores por defecto)
SesionDB = Annotated[Session, Depends(get_db)]
EmisorActual = Annotated[Emisor, Depends(emisor_actual)]


@router.get("/health", tags=["Sistema"], operation_id="verificarEstado")
def verificar_estado() -> Estado:
    return Estado(estado="ok")


@router.post(
    "/api/v1/auth/registro",
    tags=["Auth"],
    operation_id="registrarEmisor",
    status_code=status.HTTP_201_CREATED,
)
def registrar_emisor(datos: RegistroEmisor, request: Request, db: SesionDB) -> Token:
    if db.scalar(select(Emisor.id).where(Emisor.ruc == datos.ruc)) is not None:
        raise ApiError(409, "CONFLICTO", "El RUC ya está registrado.")
    emisor = Emisor(
        ruc=datos.ruc, razon_social=datos.razon_social, clave_hash=hash_clave(datos.clave)
    )
    db.add(emisor)
    db.commit()
    settings = request.app.state.settings
    return Token(
        access_token=crear_token(emisor.id, settings.jwt_secret, settings.jwt_minutos),
        emisor_id=emisor.id,
    )


@router.post(
    "/api/v1/clientes",
    tags=["Clientes"],
    operation_id="registrarCliente",
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,  # direccion es opcional: se omite en lugar de enviar null
)
def registrar_cliente(datos: ClienteNuevo, emisor: EmisorActual, db: SesionDB) -> Cliente:
    cliente = ClienteDB(emisor_id=emisor.id, **datos.model_dump())
    db.add(cliente)
    db.commit()
    return Cliente.model_validate(cliente)


@router.get(
    "/api/v1/clientes/{clienteId}",
    tags=["Clientes"],
    operation_id="obtenerCliente",
    response_model_exclude_none=True,
)
def obtener_cliente(
    clienteId: int,  # noqa: N803 (nombre del parámetro en el contrato)
    emisor: EmisorActual,
    db: SesionDB,
) -> Cliente:
    return Cliente.model_validate(facturacion.obtener_propio(db, ClienteDB, clienteId, emisor.id))


@router.post(
    "/api/v1/productos",
    tags=["Productos"],
    operation_id="registrarProducto",
    status_code=status.HTTP_201_CREATED,
)
def registrar_producto(datos: ProductoNuevo, emisor: EmisorActual, db: SesionDB) -> Producto:
    producto = ProductoDB(emisor_id=emisor.id, **datos.model_dump())
    db.add(producto)
    db.commit()
    return Producto.model_validate(producto)


@router.post(
    "/api/v1/facturas",
    tags=["Facturas"],
    operation_id="crearFactura",
    status_code=status.HTTP_201_CREATED,
)
def crear_factura(
    datos: FacturaNueva,
    request: Request,
    emisor: EmisorActual,
    db: SesionDB,
) -> Factura:
    factura = facturacion.crear_factura(db, emisor.id, datos, request.app.state.settings)
    return Factura.model_validate(factura)


@router.get("/api/v1/facturas/{facturaId}", tags=["Facturas"], operation_id="obtenerFactura")
def obtener_factura(
    facturaId: int,  # noqa: N803
    emisor: EmisorActual,
    db: SesionDB,
) -> Factura:
    return Factura.model_validate(facturacion.obtener_propio(db, FacturaDB, facturaId, emisor.id))


@router.post(
    "/api/v1/facturas/{facturaId}/enviar-sri",
    tags=["Facturas"],
    operation_id="enviarFacturaSri",
    responses={202: {"model": ResultadoEnvio}},
)
def enviar_factura_sri(
    facturaId: int,  # noqa: N803
    request: Request,
    response: Response,
    emisor: EmisorActual,
    db: SesionDB,
) -> ResultadoEnvio:
    factura, intentos, mensaje = facturacion.enviar_al_sri(
        db, emisor.id, facturaId, request.app.state.sri_gateway, request.app.state.esperar
    )
    if factura.estado == "PENDIENTE":
        response.status_code = status.HTTP_202_ACCEPTED
    return ResultadoEnvio(
        factura_id=factura.id,
        estado=factura.estado,
        intentos_en_este_envio=intentos,
        mensaje=mensaje,
        numero_autorizacion=factura.numero_autorizacion,
    )
