"""Contraseñas, token JWT y resolución del emisor autenticado (E1)."""

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from facturaec.database import get_db
from facturaec.errors import ApiError
from facturaec.models import Emisor

_ITERACIONES = 200_000
_bearer = HTTPBearer(auto_error=False)


def hash_clave(clave: str) -> str:
    sal = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", clave.encode(), bytes.fromhex(sal), _ITERACIONES)
    return f"pbkdf2_sha256${_ITERACIONES}${sal}${digest.hex()}"


def verificar_clave(clave: str, guardado: str) -> bool:
    _, iteraciones, sal, digest = guardado.split("$")
    calculado = hashlib.pbkdf2_hmac("sha256", clave.encode(), bytes.fromhex(sal), int(iteraciones))
    return hmac.compare_digest(calculado.hex(), digest)


def crear_token(emisor_id: int, secreto: str, minutos: int) -> str:
    ahora = datetime.now(UTC)
    datos = {"sub": str(emisor_id), "iat": ahora, "exp": ahora + timedelta(minutes=minutos)}
    return jwt.encode(datos, secreto, algorithm="HS256")


def emisor_actual(
    request: Request,
    credenciales: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    db: Annotated[Session, Depends(get_db)],
) -> Emisor:
    """Devuelve el emisor del token. Sin token o con token inválido responde 401 (E1)."""
    if credenciales is None:
        raise ApiError(401, "NO_AUTENTICADO", "Falta el token o no es válido.")
    try:
        datos = jwt.decode(
            credenciales.credentials, request.app.state.settings.jwt_secret, algorithms=["HS256"]
        )
        emisor = db.get(Emisor, int(datos["sub"]))
    except (jwt.PyJWTError, KeyError, ValueError):
        emisor = None
    if emisor is None:
        raise ApiError(401, "NO_AUTENTICADO", "Falta el token o no es válido.")
    return emisor
