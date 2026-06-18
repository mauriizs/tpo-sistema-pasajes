"""
CAPA 1 - Lógica pura: cálculos de dinero (recargo, recaudación con reduce y
normalización del input de precio).
"""

from functools import reduce

RECARGO_SERVICIO: float = 1.16   # constante: 16% de recargo


def aplicar_recargo(precio_base: float) -> float:
    """Devuelve el precio con el 16% de recargo aplicado (precio_base * RECARGO_SERVICIO)."""
    return precio_base * RECARGO_SERVICIO


def calcular_recaudacion(precios: list[float]) -> float:
    """Suma una lista de precios con reduce. Devuelve 0.0 si la lista está vacía."""
    return reduce(lambda acumulado, precio: acumulado + precio, precios, 0.0)


def normalizar_precio(texto: str) -> str:
    """Prepara un input de precio para conversión: strip + reemplazo de coma por punto.
       NO convierte a float (eso lo hace pedir_precio con try/except)."""
    return texto.strip().replace(",", ".")
