"""Clave de acceso de 49 dígitos con dígito verificador módulo 11 (D1, R1).

Estructura usada (contrastar con la ficha técnica vigente del SRI antes de producción):
fecha ddmmaaaa (8) + tipo de comprobante (2) + RUC (13) + ambiente (1) + serie (6)
+ secuencial (9) + código numérico (8) + tipo de emisión (1) + dígito verificador (1).
"""

from datetime import date

TIPO_FACTURA = "01"
EMISION_NORMAL = "1"


def digito_modulo11(digitos: str) -> int:
    """Pesos 2 a 7 de derecha a izquierda; 11 se convierte en 0 y 10 en 1."""
    pesos = (2, 3, 4, 5, 6, 7)
    suma = sum(int(d) * pesos[i % 6] for i, d in enumerate(reversed(digitos)))
    resultado = 11 - (suma % 11)
    return {11: 0, 10: 1}.get(resultado, resultado)


def generar(
    fecha: date,
    ruc: str,
    ambiente: str,
    establecimiento: str,
    punto_emision: str,
    secuencial: int,
    codigo_numerico: int,
) -> str:
    base = (
        f"{fecha:%d%m%Y}{TIPO_FACTURA}{ruc}{ambiente}{establecimiento}{punto_emision}"
        f"{secuencial:09d}{codigo_numerico:08d}{EMISION_NORMAL}"
    )
    if len(base) != 48 or not base.isdigit():
        raise ValueError("La base de la clave de acceso debe tener 48 dígitos.")
    return base + str(digito_modulo11(base))


def es_valida(clave: str) -> bool:
    return len(clave) == 49 and clave.isdigit() and digito_modulo11(clave[:48]) == int(clave[48])
