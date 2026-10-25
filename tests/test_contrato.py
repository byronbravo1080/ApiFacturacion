"""Prueba de conformidad: el esqueleto implementa exactamente las operaciones del contrato.

Evita el error común de la sesión 5: editar el código y olvidar el contrato (o al revés).
"""

from pathlib import Path

import yaml
from fastapi.openapi.utils import get_openapi

CONTRATO = Path(__file__).resolve().parents[1] / "api" / "openapi.yaml"
METODOS = {"get", "post", "put", "patch", "delete"}


def operaciones_del_contrato() -> set[tuple[str, str, str]]:
    contrato = yaml.safe_load(CONTRATO.read_text(encoding="utf-8"))
    return {
        (metodo.upper(), ruta, op["operationId"])
        for ruta, item in contrato["paths"].items()
        for metodo, op in item.items()
        if metodo in METODOS
    }


def operaciones_del_codigo(app) -> set[tuple[str, str, str]]:
    """Operaciones que FastAPI infiere del código (no del contrato que se publica en /docs)."""
    inferido = get_openapi(title="codigo", version="0", routes=app.routes)
    return {
        (metodo.upper(), ruta, op["operationId"])
        for ruta, item in inferido["paths"].items()
        for metodo, op in item.items()
        if metodo in METODOS
    }


def test_el_codigo_implementa_todas_y_solo_las_operaciones_del_contrato(app):
    assert operaciones_del_codigo(app) == operaciones_del_contrato()


def test_el_contrato_tiene_al_menos_cuatro_endpoints_de_negocio():
    negocio = [op for op in operaciones_del_contrato() if op[1].startswith("/api/v1/")]
    assert len(negocio) >= 4


def test_docs_publica_el_contrato_y_no_el_esquema_inferido(client):
    contrato = yaml.safe_load(CONTRATO.read_text(encoding="utf-8"))
    assert client.get("/openapi.json").json() == contrato
