"""
CAPA 3 - Dominio: reglas de negocio de ventas (la fuente de verdad).
Opera sobre el diccionario `ventas`; no hace I/O ni toca disco. registrar_venta
modifica el dict en memoria y el flujo (Capa 5) guarda después.
"""


def proximo_id_venta(ventas: dict) -> str:
    """Siguiente ID de venta: 'T' + (max+1), padding mínimo 4 dígitos. Vacío → 'T0001'."""
    # Máximo de los números existentes (no la cantidad), por si quedaron huecos.
    maximo = 0
    for id_venta in ventas:
        numero = int(id_venta[1:])  # saca la 'T' del principio
        if numero > maximo:
            maximo = numero
    return "T" + str(maximo + 1).zfill(4)


def registrar_venta(ventas: dict, id_viaje: str, dni: str, email: str, telefono: str,
                    fila: int, columna: int, precio_pagado: float,
                    boletero: str) -> str:
    """Crea UNA venta con ID autogenerado (T + max+1) en el dict ventas.
       Devuelve el id_venta generado. NO guarda a disco (eso lo hace el flujo)."""
    nuevo_id = proximo_id_venta(ventas)
    ventas[nuevo_id] = {
        "id_viaje": id_viaje,
        "dni": dni,
        "email": email,
        "telefono": telefono,
        "fila": fila,
        "columna": columna,
        "precio_pagado": precio_pagado,
        "boletero": boletero,
    }
    return nuevo_id


def dni_ya_en_viaje(ventas: dict, id_viaje: str, dni: str) -> bool:
    """True si el DNI ya tiene una venta en ese viaje (chequeo puntual contra lo persistido)."""
    for venta in ventas.values():
        if venta["id_viaje"] == id_viaje and venta["dni"] == dni:
            return True
    return False


def precios_de_ventas(ventas: dict) -> list[float]:
    """Lista de todos los precio_pagado (para recaudación total con reduce)."""
    return [venta["precio_pagado"] for venta in ventas.values()]


def ventas_de_boletero(ventas: dict, boletero: str) -> list[dict]:
    """Filtra las ventas de un boletero (filter + lambda), para 'Mis Ventas'."""
    return list(filter(lambda venta: venta["boletero"] == boletero, ventas.values()))


def construir_ticket(id_venta: str, id_viaje: str, viaje: dict, dni: str,
                     fila: int, columna: int, precio_pagado: float) -> tuple:
    """Arma la tupla inmutable del ticket para imprimir el comprobante.
       Recibe id_viaje explícito porque el ID es la clave externa del diccionario
       de viajes y NO vive dentro del dict viaje (de ahí se sacan empresa, origen,
       destino, fecha y hora).
       (id_venta, id_viaje, empresa, origen, destino, fecha, hora, dni, fila, columna, precio)."""
    return (
        id_venta,
        id_viaje,
        viaje["empresa"],
        viaje["origen"],
        viaje["destino"],
        viaje["fecha"],
        viaje["hora"],
        dni,
        fila,
        columna,
        precio_pagado,
    )
