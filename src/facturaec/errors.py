"""Errores con el formato Error / ErrorValidacion del contrato."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ApiError(Exception):
    """Error de negocio que se responde con {codigo, mensaje}."""

    def __init__(self, estado_http: int, codigo: str, mensaje: str) -> None:
        super().__init__(mensaje)
        self.estado_http = estado_http
        self.codigo = codigo
        self.mensaje = mensaje


def no_encontrado() -> ApiError:
    """404 idéntico para 'no existe' y 'es de otro emisor': no se revela cuál ocurre (E1)."""
    return ApiError(404, "NO_ENCONTRADO", "Recurso no encontrado.")


def registrar_manejadores(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def _error_api(_: Request, exc: ApiError) -> JSONResponse:
        cabeceras = {"WWW-Authenticate": "Bearer"} if exc.estado_http == 401 else None
        return JSONResponse(
            status_code=exc.estado_http,
            content={"codigo": exc.codigo, "mensaje": exc.mensaje},
            headers=cabeceras,
        )

    @app.exception_handler(RequestValidationError)
    async def _validacion(_: Request, exc: RequestValidationError) -> JSONResponse:
        detalles = [
            {"campo": ".".join(str(p) for p in e["loc"] if p != "body"), "mensaje": e["msg"]}
            for e in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={
                "codigo": "VALIDACION",
                "mensaje": "Los datos de entrada no cumplen el contrato.",
                "detalles": detalles,
            },
        )
