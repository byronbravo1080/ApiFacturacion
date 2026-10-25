"""Punto de entrada de la API.

Ejecución local (desde la raíz del repositorio):
    PYTHONPATH=src uvicorn facturaec.main:crear_app --factory --reload
"""

import time
from collections.abc import Callable
from pathlib import Path

import yaml
from fastapi import FastAPI

from facturaec.config import Settings
from facturaec.database import Base, crear_engine, crear_sessionmaker
from facturaec.errors import registrar_manejadores
from facturaec.routers import router
from facturaec.sri_gateway import SriGateway, SriGatewaySimulado

CONTRATO = Path(__file__).resolve().parents[2] / "api" / "openapi.yaml"


def crear_app(
    settings: Settings | None = None,
    sri_gateway: SriGateway | None = None,
    esperar: Callable[[float], None] = time.sleep,
) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(title="FacturaEC API", version="0.2.0")
    app.state.settings = settings
    app.state.engine = crear_engine(settings.database_url, settings.db_pool_size)
    app.state.sessionmaker = crear_sessionmaker(app.state.engine)
    app.state.sri_gateway = sri_gateway or SriGatewaySimulado(
        disponible=not settings.sri_simular_caida
    )
    app.state.esperar = esperar
    # Las tablas se crean al arrancar; las migraciones con Alembic quedan como evolución (ADR-002).
    Base.metadata.create_all(app.state.engine)
    registrar_manejadores(app)
    app.include_router(router)

    # /docs muestra el contrato API-first (fuente de verdad), no el esquema que infiere FastAPI.
    if CONTRATO.exists():
        contrato = yaml.safe_load(CONTRATO.read_text(encoding="utf-8"))
        app.openapi = lambda: contrato  # type: ignore[method-assign]
    return app
