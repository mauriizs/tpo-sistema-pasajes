"""
CAPA 5 - Orquestación: menú del boletero, con la venta múltiple atómica.
Durante la carga nada se registra ni se toca ningún asiento real: todo vive en
estructuras temporales (carrito, conjunto_sesion, matriz_trabajo). Recién al
confirmar se crean las N ventas y se guarda una sola vez; por eso cancelar es gratis.
"""

import persistencia
import ui
from logica_viajes import buscar_viajes, ventas_de_viaje
from logica_ventas import registrar_venta, construir_ticket, ventas_de_boletero
from asientos import (construir_grilla, contar_libres, dnis_del_viaje,
                      asiento_esta_libre, FILAS, COLUMNAS, OCUPADO)
from finanzas import aplicar_recargo, calcular_recaudacion

ARCHIVO_VENTAS = "ventas.json"


def menu_boletero(usuarios: dict, viajes: dict, ventas: dict, usuario_actual: str) -> None:
    """Bucle del menú de boletero. Contiene el flujo de venta múltiple."""
    while True:
        ui.mostrar_menu_boletero()
        opcion = ui.pedir_opcion("Elegí una opción:", {"1", "2", "3", "0"})
        if opcion == "1":
            flujo_ver_cartelera(viajes, ventas)
        elif opcion == "2":
            flujo_venta_multiple(viajes, ventas, usuario_actual)
        elif opcion == "3":
            flujo_mis_ventas(ventas, usuario_actual)
        elif opcion == "0":
            ui.mostrar_info("Sesión cerrada.")
            break


def flujo_ver_cartelera(viajes: dict, ventas: dict) -> None:
    """Cartelera del boletero en VISTA VENDIBLE (solo activos con asientos libres).
       Tres formas de consulta (ver todo / por destino / búsqueda exacta), las mismas
       que usa el admin; lo único que cambia es solo_vendibles=True."""
    print("\n--- CONSULTAR CARTELERA ---")
    print("[1] Ver todos")
    print("[2] Buscar por destino")
    print("[3] Búsqueda exacta (origen + destino + fecha)")
    print("[0] Volver")
    opcion = ui.pedir_opcion("Elegí una opción:", {"1", "2", "3", "0"})
    if opcion == "0":
        return
    origen = destino = fecha = None
    if opcion == "2":
        destino = ui.pedir_texto("Destino")
        if destino is None:
            return
    elif opcion == "3":
        origen = ui.pedir_texto("Origen")
        if origen is None:
            return
        destino = ui.pedir_texto("Destino")
        if destino is None:
            return
        fecha = ui.pedir_fecha()
        if fecha is None:
            return
    resultado = buscar_viajes(viajes, ventas, origen, destino, fecha, solo_vendibles=True)
    ui.mostrar_cartelera(resultado)


def flujo_venta_multiple(viajes: dict, ventas: dict, usuario_actual: str) -> None:
    """Venta múltiple atómica. Cualquier '0' durante la carga cancela toda la venta:
       como nada se escribió, no hay nada que deshacer."""

    # ---- PASO 0 · Seleccionar viaje (vista vendible) ----
    vendibles = buscar_viajes(viajes, ventas, None, None, None, solo_vendibles=True)
    if not vendibles:
        ui.mostrar_info("No hay viajes disponibles para vender en este momento.")
        return
    ui.mostrar_cartelera(vendibles)
    id_viaje = _pedir_id_viaje_vendible(viajes, ventas)
    if id_viaje is None:
        ui.mostrar_info("Venta cancelada.")
        return
    viaje = viajes[id_viaje]

    # ---- PASO 1 · ¿Cuántos pasajeros? ----
    ventas_viaje = ventas_de_viaje(ventas, id_viaje)
    matriz_trabajo = construir_grilla(ventas_viaje)
    libres = contar_libres(matriz_trabajo)
    cantidad = ui.pedir_entero("Cantidad de pasajeros", 1, libres)
    if cantidad is None:
        ui.mostrar_info("Venta cancelada.")
        return

    # Estructuras temporales de la sesión (todo efímero hasta confirmar).
    conjunto_viaje = dnis_del_viaje(ventas_viaje)   # DNIs que ya compraron antes
    conjunto_sesion = set()                         # DNIs cargados en esta venta
    carrito = []                                    # pasajeros de esta venta

    # ---- PASO 2 · Loop por cada pasajero ----
    for numero in range(1, cantidad + 1):
        print(f"\n===== PASAJERO {numero} de {cantidad} =====")

        # 2a + 2b · Elegir asiento libre (mostrando el mapa actualizado).
        asiento = _elegir_asiento(matriz_trabajo)
        if asiento is None:
            ui.mostrar_info("Venta cancelada. No se registró nada.")
            return
        fila, columna = asiento

        # 2c · DNI con doble anti-duplicados (conjunto del viaje + de la sesión).
        dni = _pedir_dni_no_duplicado(conjunto_viaje, conjunto_sesion)
        if dni is None:
            ui.mostrar_info("Venta cancelada. No se registró nada.")
            return

        # 2d · Email y teléfono.
        email = ui.pedir_email()
        if email is None:
            ui.mostrar_info("Venta cancelada. No se registró nada.")
            return
        telefono = ui.pedir_telefono()
        if telefono is None:
            ui.mostrar_info("Venta cancelada. No se registró nada.")
            return

        # 2e · Precio de ESTE pasaje (precio_base + 16%).
        precio = aplicar_recargo(viaje["precio_base"])

        # 2f · Agregar al carrito y marcar el asiento como tomado en la matriz de trabajo.
        carrito.append({
            "fila": fila, "columna": columna, "dni": dni,
            "email": email, "telefono": telefono, "precio_pagado": precio,
        })
        conjunto_sesion.add(dni)
        matriz_trabajo[fila - 1][columna - 1] = OCUPADO

    # ---- PASO 3 · Resumen y confirmación ----
    # map: proyecta el carrito a la lista de precios; reduce: suma (en calcular_recaudacion).
    total = calcular_recaudacion(list(map(lambda p: p["precio_pagado"], carrito)))
    ui.mostrar_resumen_compra(carrito, total)
    if not ui.pedir_confirmacion("¿Confirmar la compra completa?"):
        ui.mostrar_info("Venta cancelada. No se registró nada.")
        return

    # ---- PASO 4 · Commit (solo si confirmó) ----
    tickets = []
    for pasajero in carrito:
        id_venta = registrar_venta(
            ventas, id_viaje, pasajero["dni"], pasajero["email"],
            pasajero["telefono"], pasajero["fila"], pasajero["columna"],
            pasajero["precio_pagado"], usuario_actual)
        tickets.append(construir_ticket(
            id_venta, id_viaje, viaje, pasajero["dni"],
            pasajero["fila"], pasajero["columna"], pasajero["precio_pagado"]))
    persistencia.guardar(ARCHIVO_VENTAS, ventas)   # una sola escritura
    for ticket in tickets:
        ui.mostrar_ticket(ticket)
    ui.mostrar_exito(f"Venta registrada: {len(carrito)} pasaje(s).")


def _pedir_id_viaje_vendible(viajes: dict, ventas: dict) -> str | None:
    """Pide un ID de viaje y valida que exista, esté activo y tenga asientos libres.
       Repregunta hasta un ID válido. '0' → None (cancela)."""
    while True:
        entrada = ui.pedir_texto("ID del viaje a vender")
        if entrada is None:
            return None
        id_viaje = entrada.upper()   # las claves son tipo 'V001'
        if id_viaje not in viajes:
            ui.mostrar_error("No existe un viaje con ese ID.")
            continue
        if viajes[id_viaje]["estado"] != "activo":
            ui.mostrar_error("Ese viaje no está activo.")
            continue
        if contar_libres(construir_grilla(ventas_de_viaje(ventas, id_viaje))) == 0:
            ui.mostrar_error("Ese viaje no tiene asientos libres.")
            continue
        return id_viaje


def _elegir_asiento(matriz_trabajo: list[list[str]]) -> tuple[int, int] | None:
    """Muestra el mapa y pide un asiento LIBRE en la matriz de trabajo.
       Devuelve la tupla (fila, columna) o None si se cancela con '0'."""
    while True:
        ui.mostrar_mapa_asientos(matriz_trabajo)
        fila = ui.pedir_entero("Fila", 1, FILAS)
        if fila is None:
            return None
        columna = ui.pedir_entero("Columna", 1, COLUMNAS)
        if columna is None:
            return None
        if asiento_esta_libre(matriz_trabajo, fila, columna):
            return (fila, columna)
        ui.mostrar_error("Ese asiento ya está ocupado. Elegí otro.")


def _pedir_dni_no_duplicado(conjunto_viaje: set, conjunto_sesion: set) -> str | None:
    """Pide un DNI y lo chequea contra los DOS conjuntos anti-duplicados.
       Devuelve el DNI válido o None si se cancela con '0'."""
    while True:
        dni = ui.pedir_dni()
        if dni is None:
            return None
        if dni in conjunto_viaje:
            ui.mostrar_error("Ese DNI ya tiene pasaje en este viaje.")
            continue
        if dni in conjunto_sesion:
            ui.mostrar_error("Ya cargaste ese DNI en esta compra.")
            continue
        return dni


def flujo_mis_ventas(ventas: dict, usuario_actual: str) -> None:
    """Mis Ventas (Historial): filtra las ventas del boletero logueado y muestra
       la lista + su total propio (filter + lambda en el dominio, reduce en el total)."""
    propias = ventas_de_boletero(ventas, usuario_actual)
    # El dominio ya filtró por boletero; el total propio se suma con reduce.
    total = calcular_recaudacion([venta["precio_pagado"] for venta in propias])
    ui.mostrar_historial_ventas(propias, total)
