"""El documento de historias (docs/07) debe mostrar los mismos criterios que se ejecutan."""

from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
FEATURES = sorted((RAIZ / "tests" / "features").glob("*.feature"))


def sin_lineas_vacias(texto: str) -> str:
    return "\n".join(linea for linea in texto.splitlines() if linea.strip())


DOC_HISTORIAS = sin_lineas_vacias(
    (RAIZ / "docs" / "07-historias-y-criterios.md").read_text(encoding="utf-8")
)


def gherkin_sin_comentarios(archivo: Path) -> str:
    """Quita los comentarios de cabecera (salvo la directiva de idioma) y las líneas vacías."""
    lineas = archivo.read_text(encoding="utf-8").splitlines()
    return sin_lineas_vacias(
        "\n".join(x for x in lineas if not x.startswith("#") or x.startswith("# language"))
    )


@pytest.mark.parametrize("archivo", FEATURES, ids=lambda f: f.name)
def test_docs07_contiene_el_gherkin_ejecutable(archivo):
    assert gherkin_sin_comentarios(archivo) in DOC_HISTORIAS
