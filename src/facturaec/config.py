"""Configuración leída de variables de entorno o archivo .env (sin credenciales en el código)."""

import os
from dataclasses import dataclass, field
from pathlib import Path


def _cargar_archivo_env() -> None:
    """Carga variables desde el archivo .env en la raíz del proyecto si existe."""
    # Busca .env en la raíz del repositorio
    raiz = Path(__file__).resolve().parents[2]
    env_file = raiz / ".env"
    if env_file.is_file():
        for linea in env_file.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#") and "=" in linea:
                clave, valor = linea.split("=", 1)
                os.environ.setdefault(clave.strip(), valor.strip().strip("'\""))


_cargar_archivo_env()


@dataclass(frozen=True)
class Settings:
    """Parámetros del servicio. Los valores por defecto sirven solo para desarrollo local."""

    database_url: str = field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./facturaec.db")
    )
    jwt_secret: str = field(
        default_factory=lambda: os.getenv(
            "JWT_SECRET", "solo-para-desarrollo-local-cambiar-en-produccion"
        )
    )
    jwt_minutos: int = field(default_factory=lambda: int(os.getenv("JWT_MINUTOS", "60")))
    sri_gateway_url: str = field(default_factory=lambda: os.getenv("SRI_GATEWAY_URL", ""))
    supabase_anon_key: str = field(default_factory=lambda: os.getenv("SUPABASE_ANON_KEY", ""))
    sri_timeout_segundos: float = field(
        default_factory=lambda: float(os.getenv("SRI_TIMEOUT_SEGUNDOS", "15"))
    )
    # Pide al microservicio que simule la caída del SRI, para demostrar E2.
    sri_simular_caida: bool = field(
        default_factory=lambda: os.getenv("SRI_SIMULAR_CAIDA", "false").lower() == "true"
    )
    cors_origins: str = field(
        default_factory=lambda: os.getenv(
            "CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
        )
    )
    establecimiento: str = "001"
    punto_emision: str = "001"
    ambiente_sri: str = "1"  # 1 = pruebas (supuesto 1.4 del dossier)
    db_pool_size: int = field(default_factory=lambda: int(os.getenv("DB_POOL_SIZE", "10")))
