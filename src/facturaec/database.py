"""Motor y sesiones de SQLAlchemy (ADR-002: PostgreSQL; SQLite solo en desarrollo)."""

from collections.abc import Iterator

from fastapi import Request
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Base declarativa de los modelos."""


def crear_engine(database_url: str, pool_size: int = 10) -> Engine:
    """Crea el motor; en PostgreSQL ajusta el pool para soportar carga concurrente (E6)."""
    if database_url.startswith("sqlite"):
        return create_engine(database_url, connect_args={"check_same_thread": False})
    return create_engine(database_url, pool_size=pool_size, max_overflow=0, pool_pre_ping=True)


def crear_sessionmaker(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)


def get_db(request: Request) -> Iterator[Session]:
    """Dependencia de FastAPI: una sesión por solicitud."""
    session: Session = request.app.state.sessionmaker()
    try:
        yield session
    finally:
        session.close()
