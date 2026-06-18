"""
CAPA 1 - Lógica pura: la grilla de asientos del micro (matriz 5x4).

Funciones puras: reciben datos y devuelven datos. No imprimen, no piden input,
no tocan archivos. No dependen de ningún otro módulo del proyecto.

La matriz NO se persiste: se deriva de las ventas de un viaje cada vez que se
necesita (ver arquitectura 2.2). Estas funciones reciben SOLO las ventas de ese
viaje (ya filtradas por el dominio) para mantenerse puras y simples.
"""

FILAS: int = 5       # constante del sistema
COLUMNAS: int = 4    # constante del sistema (total 20 asientos)
LIBRE: str = "L"
OCUPADO: str = "O"


def construir_grilla(ventas_del_viaje: list[dict]) -> list[list[str]]:
    """Construye una matriz 5x4 de 'L'/'O' a partir de las ventas de UN viaje.
       Cada venta con (fila, columna) marca esa celda como 'O'. El resto queda 'L'.
       Una lista vacía produce una grilla toda 'L'."""
    # Grilla nueva toda libre. Se crea fila por fila para no compartir la misma
    # lista interna entre filas (evita el bug de la referencia repetida).
    grilla = [[LIBRE for _ in range(COLUMNAS)] for _ in range(FILAS)]
    for venta in ventas_del_viaje:
        fila = venta["fila"]
        columna = venta["columna"]
        # Las coordenadas vienen en base 1 (el usuario piensa en base 1).
        if asiento_en_rango(fila, columna):
            grilla[fila - 1][columna - 1] = OCUPADO
    return grilla


def asiento_en_rango(fila: int, columna: int) -> bool:
    """True si (fila, columna) está dentro de los límites 5x4 (base 1)."""
    return 1 <= fila <= FILAS and 1 <= columna <= COLUMNAS


def asiento_esta_libre(grilla: list[list[str]], fila: int, columna: int) -> bool:
    """True si la celda (fila, columna) de la grilla está libre.
       fila y columna en base 1 (el usuario piensa en base 1).
       Usa asiento_en_rango como guarda previa: si la coordenada está fuera de los
       límites 5x4, devuelve False en vez de indexar (evita el wraparound silencioso
       de un índice negativo, p.ej. columna 0 → -1 → última columna)."""
    if not asiento_en_rango(fila, columna):
        return False
    return grilla[fila - 1][columna - 1] == LIBRE


def contar_libres(grilla: list[list[str]]) -> int:
    """Cuenta cuántas celdas 'L' hay en la grilla."""
    total = 0
    for fila in grilla:
        for celda in fila:
            if celda == LIBRE:
                total += 1
    return total


def dnis_del_viaje(ventas_del_viaje: list[dict]) -> set[str]:
    """Devuelve el conjunto de DNIs presentes en las ventas de un viaje.
       Es el conjunto anti-duplicados, derivado de las ventas."""
    return {venta["dni"] for venta in ventas_del_viaje}
