"""
CAPA 4 - Presentación: todo lo que el usuario VE y TIPEA.

Banners, menús, tablas, mapa de asientos, ticket, mensajes y las funciones
pedir_X(). NUNCA aplica una regla de negocio: muestra lo que le pasan y captura
lo que el usuario tipea. Recibe los datos YA cocinados por el dominio.

Importa de la Capa 1: validaciones (validadores reusados en las pedir_X) y
finanzas (normalizar_precio). NO conoce el dominio ni la persistencia.

Convención '0' (arquitectura 3.1.A): en las pedir_X, '0' significa cancelar y
subir un nivel → devuelve None. El parámetro permitir_cancelar lo desactiva
cuando el flujo no debe ofrecer salida (p. ej. crear el admin en modo fábrica).
"""

import validaciones
import finanzas


# ============================================================================
#  Banners y mensajes
# ============================================================================

def mostrar_bienvenida() -> None:
    print("\n" + "=" * 50)
    print("        NEXUS VIAJES - Gestión de Micros")
    print("=" * 50)


def mostrar_banner_fabrica() -> None:
    print("\n" + "*" * 50)
    print("  SISTEMA EN ESTADO DE FÁBRICA")
    print("  No hay administrador real todavía.")
    print("  Vamos a crear el primer administrador.")
    print("*" * 50)


def mostrar_menu_principal() -> None:
    print("\n----- MENÚ PRINCIPAL -----")
    print("[1] Iniciar sesión")
    print("[2] Ayuda")
    print("[3] Salir")


def mostrar_menu_admin() -> None:
    print("\n----- MENÚ ADMINISTRADOR -----")
    print("[1] Ver cartelera")
    print("[2] Alta de viaje")
    print("[3] Modificar viaje")
    print("[4] Baja de viaje")
    print("[5] Gestión de usuarios")
    print("[6] Reporte: recaudación total")
    print("[7] Reporte: destinos activos únicos")
    print("[0] Cerrar sesión")


def mostrar_menu_boletero() -> None:
    print("\n----- MENÚ BOLETERO -----")
    print("[1] Ver cartelera")
    print("[2] Venta múltiple")
    print("[3] Mis ventas (historial)")
    print("[0] Cerrar sesión")


def mostrar_ayuda() -> None:
    print("\n----- AYUDA -----")
    print("Nexus Viajes es un sistema de gestión y venta de pasajes de micro.")
    print("- Para operar, iniciá sesión con el usuario que te asignó el admin.")
    print("- No hay auto-registro: el personal nuevo lo da de alta el administrador.")
    print("- En cualquier dato que se te pida, ingresá '0' para cancelar y volver.")


def mostrar_error(mensaje: str) -> None:
    print(f"\n[ERROR] {mensaje}")


def mostrar_info(mensaje: str) -> None:
    print(f"\n[INFO] {mensaje}")


def mostrar_exito(mensaje: str) -> None:
    print(f"\n[OK] {mensaje}")


# ============================================================================
#  Presentación de datos (reciben datos ya cocinados por el dominio)
# ============================================================================

def mostrar_cartelera(viajes_enriquecidos: list[dict]) -> None:
    """Imprime la tabla de viajes. Lee la clave `ocupacion` (int) y la muestra
       como f"{ocupacion}%". Si la lista está vacía, muestra mensaje, no tabla rota."""
    if not viajes_enriquecidos:
        mostrar_info("No hay viajes para mostrar.")
        return
    print("\n" + "-" * 92)
    print(f"{'ID':<6}{'Empresa':<16}{'Origen':<16}{'Destino':<16}"
          f"{'Fecha':<12}{'Hora':<7}{'Precio':>12}{'Ocup.':>7}")
    print("-" * 92)
    for viaje in viajes_enriquecidos:
        # El destino se guarda normalizado (minúsculas); se capitaliza al mostrar.
        destino = viaje["destino"].capitalize()
        estado = viaje.get("estado", "")
        # Marca visual para los cancelados (los ve el admin en vista total).
        etiqueta_id = viaje["id_viaje"]
        if estado == "cancelado":
            etiqueta_id += "*"
        print(f"{etiqueta_id:<6}{viaje['empresa']:<16}{viaje['origen']:<16}"
              f"{destino:<16}{viaje['fecha']:<12}{viaje['hora']:<7}"
              f"${viaje['precio_base']:>10,.2f}{str(viaje['ocupacion']) + '%':>7}")
    print("-" * 92)
    # Solo se aclara el asterisco si hay algún cancelado en la tabla.
    if any(v.get("estado") == "cancelado" for v in viajes_enriquecidos):
        print("(*) viaje cancelado")


def mostrar_mapa_asientos(grilla: list[list[str]]) -> None:
    """Imprime la grilla 5x4 visual (L = libre, O = ocupado)."""
    columnas = len(grilla[0]) if grilla else 0
    print("\n        MAPA DE ASIENTOS   (L=libre  O=ocupado)")
    # Encabezado de columnas.
    encabezado = "        " + "".join(f"C{c:<4}" for c in range(1, columnas + 1))
    print(encabezado)
    for indice, fila in enumerate(grilla, start=1):
        celdas = "".join(f"{celda:<5}" for celda in fila)
        print(f"  Fila {indice}  {celdas}")


def mostrar_lista_usuarios(usuarios_listados: list[tuple[str, str, str]]) -> None:
    """Muestra el 'mapa' de usuarios: (nombre, rol, estado)."""
    if not usuarios_listados:
        mostrar_info("No hay usuarios cargados.")
        return
    print("\n" + "-" * 48)
    print(f"{'Usuario':<22}{'Rol':<16}{'Estado':<10}")
    print("-" * 48)
    for nombre, rol, estado in usuarios_listados:
        print(f"{nombre:<22}{rol:<16}{estado:<10}")
    print("-" * 48)


def mostrar_ticket(ticket: tuple) -> None:
    """Imprime el comprobante a partir de la tupla del ticket.
       (id_venta, id_viaje, empresa, origen, destino, fecha, hora,
        dni, fila, columna, precio_pagado)."""
    (id_venta, id_viaje, empresa, origen, destino, fecha, hora,
     dni, fila, columna, precio) = ticket
    print("\n" + "=" * 44)
    print("           COMPROBANTE DE PASAJE")
    print("=" * 44)
    print(f"  Ticket : {id_venta}        Viaje: {id_viaje}")
    print(f"  Empresa: {empresa}")
    print(f"  Tramo  : {origen} -> {destino.capitalize()}")
    print(f"  Fecha  : {fecha}   Hora: {hora}")
    print(f"  DNI    : {dni}")
    print(f"  Asiento: fila {fila}, columna {columna}")
    print(f"  Precio : ${precio:,.2f}")
    print("=" * 44)


def mostrar_resumen_compra(carrito: list[dict], total: float) -> None:
    """Muestra los pasajes cargados en el carrito y el total a cobrar."""
    print("\n" + "-" * 56)
    print("           RESUMEN DE LA COMPRA")
    print("-" * 56)
    print(f"{'#':<3}{'DNI':<12}{'Asiento':<12}{'Precio':>12}")
    print("-" * 56)
    for indice, pasajero in enumerate(carrito, start=1):
        asiento = f"F{pasajero['fila']} C{pasajero['columna']}"
        print(f"{indice:<3}{pasajero['dni']:<12}{asiento:<12}"
              f"${pasajero['precio_pagado']:>10,.2f}")
    print("-" * 56)
    print(f"{'TOTAL':<27}${total:>10,.2f}")
    print("-" * 56)


def mostrar_recaudacion(total: float, cantidad: int) -> None:
    """Muestra el reporte de recaudación total."""
    print("\n" + "-" * 40)
    print("        RECAUDACIÓN TOTAL")
    print("-" * 40)
    print(f"  Ventas registradas: {cantidad}")
    print(f"  Total recaudado   : ${total:,.2f}")
    print("-" * 40)


def mostrar_destinos(destinos: set[str]) -> None:
    """Muestra el conjunto de destinos activos únicos."""
    if not destinos:
        mostrar_info("No hay destinos activos para mostrar.")
        return
    print("\n----- DESTINOS ACTIVOS ÚNICOS -----")
    for destino in sorted(destinos):
        print(f"  - {destino.capitalize()}")


# ============================================================================
#  Captura de input (con bucle de validación y salida '0')
# ============================================================================

def pedir_opcion(prompt: str, opciones_validas: set[str]) -> str:
    """Pide una opción de menú (comparación de string). Repregunta hasta una válida."""
    while True:
        entrada = input(prompt + " ").strip()
        if entrada in opciones_validas:
            return entrada
        mostrar_error("Opción inválida. Probá de nuevo.")


def pedir_texto(prompt: str, permitir_cancelar: bool = True) -> str | None:
    """Pide texto no vacío. Devuelve None si el usuario ingresa '0' (cancelar)."""
    sufijo = " (0 = cancelar)" if permitir_cancelar else ""
    while True:
        entrada = input(f"{prompt}{sufijo}: ").strip()
        if permitir_cancelar and entrada == "0":
            return None
        if validaciones.texto_no_vacio(entrada):
            return entrada
        mostrar_error("El dato no puede estar vacío.")


def pedir_dni(permitir_cancelar: bool = True) -> str | None:
    """Pide DNI hasta que sea válido (regex). '0' → None."""
    sufijo = " (0 = cancelar)" if permitir_cancelar else ""
    while True:
        entrada = input(f"DNI (7-8 dígitos){sufijo}: ").strip()
        if permitir_cancelar and entrada == "0":
            return None
        if validaciones.es_dni_valido(entrada):
            return entrada
        mostrar_error("DNI inválido. Debe tener 7 u 8 dígitos numéricos.")


def pedir_email(permitir_cancelar: bool = True) -> str | None:
    """Pide email hasta que tenga formato válido (regex). '0' → None."""
    sufijo = " (0 = cancelar)" if permitir_cancelar else ""
    while True:
        entrada = input(f"Email{sufijo}: ").strip()
        if permitir_cancelar and entrada == "0":
            return None
        if validaciones.es_email_valido(entrada):
            return entrada
        mostrar_error("Email inválido. Formato esperado: usuario@dominio.ext")


def pedir_telefono(permitir_cancelar: bool = True) -> str | None:
    """Pide teléfono hasta que sea válido (regex). '0' → None."""
    sufijo = " (0 = cancelar)" if permitir_cancelar else ""
    while True:
        entrada = input(f"Teléfono (8-15 dígitos){sufijo}: ").strip()
        if permitir_cancelar and entrada == "0":
            return None
        if validaciones.es_telefono_valido(entrada):
            return entrada
        mostrar_error("Teléfono inválido. Debe tener entre 8 y 15 dígitos.")


def pedir_fecha(permitir_cancelar: bool = True) -> str | None:
    """Pide fecha DD/MM/AAAA hasta que sea válida. '0' → None."""
    sufijo = " (0 = cancelar)" if permitir_cancelar else ""
    while True:
        entrada = input(f"Fecha (DD/MM/AAAA){sufijo}: ").strip()
        if permitir_cancelar and entrada == "0":
            return None
        if validaciones.es_fecha_valida(entrada):
            return entrada
        mostrar_error("Fecha inválida. Formato DD/MM/AAAA con día válido para el mes.")


def pedir_hora(permitir_cancelar: bool = True) -> str | None:
    """Pide hora HH:MM hasta que sea válida. '0' → None."""
    sufijo = " (0 = cancelar)" if permitir_cancelar else ""
    while True:
        entrada = input(f"Hora (HH:MM){sufijo}: ").strip()
        if permitir_cancelar and entrada == "0":
            return None
        if validaciones.es_hora_valida(entrada):
            return entrada
        mostrar_error("Hora inválida. Formato HH:MM (00-23 / 00-59).")


def pedir_precio(permitir_cancelar: bool = True) -> float | None:
    """Pide precio: normaliza coma→punto, try/except float, valida > 0.
       '0' → None (cancelar). Un precio válido es siempre > 0, así que '0'
       nunca es un precio legítimo y puede usarse como código de cancelación."""
    sufijo = " (0 = cancelar)" if permitir_cancelar else ""
    while True:
        entrada = input(f"Precio base{sufijo}: ").strip()
        if permitir_cancelar and entrada == "0":
            return None
        # Normalización ANTES de convertir (coma→punto); el try envuelve solo float().
        texto = finanzas.normalizar_precio(entrada)
        try:
            valor = float(texto)
        except ValueError:
            mostrar_error("Precio inválido. Ingresá un número (ej: 50000 o 50000,50).")
            continue
        if valor > 0:
            return valor
        mostrar_error("El precio debe ser mayor a 0.")


def pedir_entero(prompt: str, minimo: int, maximo: int,
                 permitir_cancelar: bool = True) -> int | None:
    """Pide un entero en [minimo, maximo] con try/except. '0' → None (cancelar).
       En todos sus usos el rango válido empieza en 1, así que '0' nunca colisiona
       con un valor legítimo y funciona limpio como cancelación."""
    sufijo = " (0 = cancelar)" if permitir_cancelar else ""
    while True:
        entrada = input(f"{prompt} [{minimo}-{maximo}]{sufijo}: ").strip()
        if permitir_cancelar and entrada == "0":
            return None
        try:
            valor = int(entrada)
        except ValueError:
            mostrar_error("Ingresá un número entero.")
            continue
        if minimo <= valor <= maximo:
            return valor
        mostrar_error(f"El valor debe estar entre {minimo} y {maximo}.")


def pedir_clave(prompt: str) -> str:
    """Pide una clave SIN normalizar. Solo valida que no esté vacía."""
    while True:
        entrada = input(f"{prompt}: ")
        # La clave NO se normaliza: se valida solo que no esté vacía tras strip,
        # pero se devuelve TAL CUAL se tipeó (case-sensitive, sin recortar).
        if entrada.strip() != "":
            return entrada
        mostrar_error("La clave no puede estar vacía.")


def pedir_confirmacion(prompt: str) -> bool:
    """Confirmación con LISTA BLANCA: True solo si la respuesta normalizada
       está en {'s', 'si', 'sí'}. Cualquier otra cosa → False."""
    respuesta = input(f"{prompt} (S/N): ").strip().lower()
    return respuesta in {"s", "si", "sí"}
