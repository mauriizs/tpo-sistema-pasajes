"""
CAPA 1 - Lógica pura: cálculos de dinero del sistema.

Funciones puras: reciben datos y devuelven datos. No imprimen, no piden input,
no tocan archivos. No dependen de ningún otro módulo del proyecto.

Acá vive el recargo de servicio, la suma de recaudación (con reduce) y la
normalización del input de precio (sin convertir: eso lo hace pedir_precio).
"""

from functools import reduce

RECARGO_SERVICIO: float = 1.16   # constante: 16% de recargo


def aplicar_recargo(precio_base: float) -> float:
    """Devuelve el precio con el 16% de recargo aplicado (precio_base * RECARGO_SERVICIO).
       Función escalar pura: recibe un precio, devuelve un precio. El uso de map vive en el
       flujo de venta (proyecta el carrito de N pasajeros a su lista de precios), no acá."""
    return precio_base * RECARGO_SERVICIO


def calcular_recaudacion(precios: list[float]) -> float:
    """Suma una lista de precios con reduce. Devuelve 0.0 si la lista está vacía."""
    return reduce(lambda acumulado, precio: acumulado + precio, precios, 0.0)


def normalizar_precio(texto: str) -> str:
    """Prepara un input de precio para conversión: strip + reemplazo de coma por punto.
       NO convierte a float (eso lo hace pedir_precio con try/except)."""
    return texto.strip().replace(",", ".")
