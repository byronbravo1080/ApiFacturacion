"""Configuración leída de variables de entorno (sin credenciales en el código)."""

import os
from dataclasses import dataclass, field


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
    sri_simular_caida: bool = field(
        default_factory=lambda: os.getenv("SRI_SIMULAR_CAIDA", "false").lower() == "true"
    )
    establecimiento: str = "001"
    punto_emision: str = "001"
    ambiente_sri: str = "1"  # 1 = pruebas (supuesto 1.4 del dossier)
    db_pool_size: int = field(default_factory=lambda: int(os.getenv("DB_POOL_SIZE", "10")))
