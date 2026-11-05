"""Fixtures comunes. Por defecto las pruebas usan SQLite en un archivo temporal.

Para ejecutar también la prueba concurrente de E6 (CA5.3) se necesita PostgreSQL:
    TEST_DATABASE_URL=postgresql+psycopg://usuario:clave@host:5432/base pytest
"""

import os
from dataclasses import dataclass, field

import pytest
from fastapi.testclient import TestClient

from facturaec.config import Settings
from facturaec.database import Base
from facturaec.main import crear_app
from facturaec.sri_gateway import SriNoDisponibleError, SriRechazoError

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


def usa_postgresql() -> bool:
    return bool(TEST_DATABASE_URL and TEST_DATABASE_URL.startswith("postgresql"))


def pytest_collection_modifyitems(config, items):
    if usa_postgresql():
        return
    omitir = pytest.mark.skip(
        reason="CA5.3 requiere PostgreSQL: defina TEST_DATABASE_URL (ADR-002)"
    )
    for item in items:
        if "postgresql" in item.keywords:
            item.add_marker(omitir)


class EsperaRegistrada:
    """Sustituye a time.sleep: registra las esperas pedidas sin detener la prueba."""

    def __init__(self) -> None:
        self.esperas: list[float] = []

    def __call__(self, segundos: float) -> None:
        self.esperas.append(segundos)


@dataclass
class SriFalso:
    """Doble de prueba del puerto SriGateway: evita depender de la red en las pruebas."""

    disponible: bool = True
    rechazo: str | None = None
    recibidos: list[str] = field(default_factory=list)
    intentos: int = 0

    def enviar(self, clave_acceso: str) -> str:
        self.intentos += 1
        if not self.disponible:
            raise SriNoDisponibleError("El SRI no respondió.")
        if self.rechazo is not None:
            raise SriRechazoError(self.rechazo)
        self.recibidos.append(clave_acceso)
        return clave_acceso


@pytest.fixture
def sri() -> SriFalso:
    return SriFalso()


@pytest.fixture
def espera() -> EsperaRegistrada:
    return EsperaRegistrada()


@pytest.fixture
def app(tmp_path, sri, espera):
    url = TEST_DATABASE_URL or f"sqlite:///{tmp_path / 'pruebas.db'}"
    settings = Settings(
        database_url=url, jwt_secret="secreto-de-pruebas-de-al-menos-32-bytes", db_pool_size=60
    )
    aplicacion = crear_app(settings=settings, sri_gateway=sri, esperar=espera)
    if usa_postgresql():  # base limpia en cada escenario
        Base.metadata.drop_all(aplicacion.state.engine)
        Base.metadata.create_all(aplicacion.state.engine)
    yield aplicacion
    aplicacion.state.engine.dispose()


@pytest.fixture
def client(app):
    with TestClient(app) as cliente:
        yield cliente


@pytest.fixture
def ctx() -> dict:
    """Estado compartido entre los pasos de un escenario."""
    return {"emisores": {}, "respuesta": None}
