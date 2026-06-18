"""
CAPA 5 - Orquestación: menú del administrador.

Cablea ui + dominio + persistencia para gestionar viajes, usuarios y reportes.
Orquesta: pide con ui, decide con el dominio, guarda con persistencia. No aplica
reglas por su cuenta ni imprime tablas a mano (eso es ui).

Guardado transaccional (3.1.D): se escribe a disco inmediatamente después de
cada mutación (alta/modificación/baja de viaje, crear/desactivar/resetear usuario).
"""

import persistencia
import ui
from logica_viajes import (buscar_viajes, alta_viaje, modificar_viaje,
                           cancelar_o_borrar_viaje, destinos_activos_unicos)
from logica_usuarios import (crear_usuario, desactivar_usuario, resetear_clave,
                            listar_usuarios)
from logica_ventas import precios_de_ventas
from finanzas import calcular_recaudacion

ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_VIAJES = "viajes.json"


def menu_admin(usuarios: dict, viajes: dict, ventas: dict, usuario_actual: str) -> None:
    """Bucle del menú de administrador. Cablea ui + dominio + persistencia."""
    while True:
        ui.mostrar_menu_admin()
        opcion = ui.pedir_opcion("Elegí una opción:",
                                 {"1", "2", "3", "4", "5", "6", "7", "0"})
        if opcion == "1":
            flujo_ver_cartelera(viajes, ventas)
        elif opcion == "2":
            flujo_alta_viaje(viajes)
        elif opcion == "3":
            flujo_modificar_viaje(viajes, ventas)
        elif opcion == "4":
            flujo_baja_viaje(viajes, ventas)
        elif opcion == "5":
            flujo_gestion_usuarios(usuarios)
        elif opcion == "6":
            flujo_recaudacion(ventas)
        elif opcion == "7":
            flujo_destinos(viajes)
        elif opcion == "0":
            ui.mostrar_info("Sesión cerrada.")
            break


# ============================================================================
#  Cartelera (vista total)
# ============================================================================

def flujo_ver_cartelera(viajes: dict, ventas: dict) -> None:
    """Cartelera del admin en VISTA TOTAL (ve activos, cancelados y llenos).
       Mismas tres consultas que el boletero; lo único que cambia es solo_vendibles=False."""
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
    resultado = buscar_viajes(viajes, ventas, origen, destino, fecha, solo_vendibles=False)
    ui.mostrar_cartelera(resultado)


# ============================================================================
#  Gestión de viajes
# ============================================================================

def flujo_alta_viaje(viajes: dict) -> None:
    """Alta de viaje: todos los campos obligatorios. '0' en cualquiera cancela."""
    print("\n--- ALTA DE VIAJE ---")
    empresa = ui.pedir_texto("Empresa")
    if empresa is None:
        return
    origen = ui.pedir_texto("Origen")
    if origen is None:
        return
    destino = ui.pedir_texto("Destino")
    if destino is None:
        return
    fecha = ui.pedir_fecha()
    if fecha is None:
        return
    hora = ui.pedir_hora()
    if hora is None:
        return
    precio = ui.pedir_precio()
    if precio is None:
        return
    exito, mensaje = alta_viaje(viajes, empresa, origen, destino, fecha, hora, precio)
    if exito:
        persistencia.guardar(ARCHIVO_VIAJES, viajes)   # punto transaccional
        ui.mostrar_exito(f"Viaje creado con ID {mensaje}.")
    else:
        ui.mostrar_error(mensaje)


def flujo_modificar_viaje(viajes: dict, ventas: dict) -> None:
    """Modificación campo por campo. Solo empresa/fecha/hora/precio (origen y destino
       NO son editables). Para cada campo se pregunta S/N: N deja igual (None), S pide
       el dato. Un '0' dentro de un pedir_X cancela TODA la modificación."""
    ui.mostrar_cartelera(buscar_viajes(viajes, ventas, None, None, None, solo_vendibles=False))
    entrada = ui.pedir_texto("ID del viaje a modificar")
    if entrada is None:
        return
    id_viaje = entrada.upper()
    if id_viaje not in viajes:
        ui.mostrar_error("No existe un viaje con ese ID.")
        return
    viaje = viajes[id_viaje]

    # Para cada campo editable: mostrar valor actual → preguntar si se cambia →
    # si S, pedir el dato (su '0' cancela toda la modificación → se devuelve sin guardar).
    nueva_empresa = None
    if ui.pedir_confirmacion(f"Empresa actual: '{viaje['empresa']}'. ¿Modificar?"):
        nueva_empresa = ui.pedir_texto("Nueva empresa")
        if nueva_empresa is None:
            ui.mostrar_info("Modificación cancelada.")
            return

    nueva_fecha = None
    if ui.pedir_confirmacion(f"Fecha actual: '{viaje['fecha']}'. ¿Modificar?"):
        nueva_fecha = ui.pedir_fecha()
        if nueva_fecha is None:
            ui.mostrar_info("Modificación cancelada.")
            return

    nueva_hora = None
    if ui.pedir_confirmacion(f"Hora actual: '{viaje['hora']}'. ¿Modificar?"):
        nueva_hora = ui.pedir_hora()
        if nueva_hora is None:
            ui.mostrar_info("Modificación cancelada.")
            return

    nuevo_precio = None
    if ui.pedir_confirmacion(f"Precio actual: ${viaje['precio_base']:,.2f}. ¿Modificar?"):
        nuevo_precio = ui.pedir_precio()
        if nuevo_precio is None:
            ui.mostrar_info("Modificación cancelada.")
            return

    # Si no se eligió cambiar nada, no se guarda.
    if nueva_empresa is None and nueva_fecha is None and nueva_hora is None and nuevo_precio is None:
        ui.mostrar_info("No se modificó ningún campo.")
        return

    exito, mensaje = modificar_viaje(viajes, id_viaje, nueva_empresa,
                                     nueva_fecha, nueva_hora, nuevo_precio)
    if exito:
        persistencia.guardar(ARCHIVO_VIAJES, viajes)   # punto transaccional
        ui.mostrar_exito(mensaje)
    else:
        ui.mostrar_error(mensaje)


def flujo_baja_viaje(viajes: dict, ventas: dict) -> None:
    """Baja de viaje: borra físico si no tiene ventas; soft-delete (cancelado) si tiene."""
    ui.mostrar_cartelera(buscar_viajes(viajes, ventas, None, None, None, solo_vendibles=False))
    entrada = ui.pedir_texto("ID del viaje a dar de baja")
    if entrada is None:
        return
    id_viaje = entrada.upper()
    exito, mensaje = cancelar_o_borrar_viaje(viajes, ventas, id_viaje)
    if exito:
        persistencia.guardar(ARCHIVO_VIAJES, viajes)   # punto transaccional
        ui.mostrar_exito(mensaje)
    else:
        ui.mostrar_error(mensaje)


# ============================================================================
#  Gestión de usuarios
# ============================================================================

def flujo_gestion_usuarios(usuarios: dict) -> None:
    """Entrada de gestión de usuarios: SIEMPRE muestra la lista primero
       (mostrar antes de pedir), luego ofrece crear / desactivar / resetear."""
    while True:
        ui.mostrar_lista_usuarios(listar_usuarios(usuarios))
        print("\n--- GESTIÓN DE USUARIOS ---")
        print("[1] Crear usuario")
        print("[2] Desactivar usuario")
        print("[3] Resetear clave (reactiva)")
        print("[0] Volver")
        opcion = ui.pedir_opcion("Elegí una opción:", {"1", "2", "3", "0"})
        if opcion == "1":
            flujo_crear_usuario(usuarios)
        elif opcion == "2":
            flujo_desactivar_usuario(usuarios)
        elif opcion == "3":
            flujo_resetear_clave(usuarios)
        elif opcion == "0":
            return


def flujo_crear_usuario(usuarios: dict) -> None:
    """Crea un usuario nuevo. El rol se elige por menú; la clave no se normaliza."""
    nombre = ui.pedir_texto("Nombre del nuevo usuario")
    if nombre is None:
        return
    clave = ui.pedir_clave("Clave")
    print("Rol: [1] Administrador  [2] Boletero")
    opcion_rol = ui.pedir_opcion("Elegí el rol:", {"1", "2"})
    rol = "administrador" if opcion_rol == "1" else "boletero"
    exito, mensaje = crear_usuario(usuarios, nombre, clave, rol)
    if exito:
        persistencia.guardar(ARCHIVO_USUARIOS, usuarios)   # punto transaccional
        ui.mostrar_exito(mensaje)
    else:
        ui.mostrar_error(mensaje)


def flujo_desactivar_usuario(usuarios: dict) -> None:
    """Desactiva (baja lógica) un usuario. El dominio aplica el anti-admin-suicida."""
    nombre = ui.pedir_texto("Nombre del usuario a desactivar")
    if nombre is None:
        return
    exito, mensaje = desactivar_usuario(usuarios, nombre)
    if exito:
        persistencia.guardar(ARCHIVO_USUARIOS, usuarios)   # punto transaccional
        ui.mostrar_exito(mensaje)
    else:
        ui.mostrar_error(mensaje)


def flujo_resetear_clave(usuarios: dict) -> None:
    """Asigna una clave nueva y reactiva al usuario (única vía de rehabilitación)."""
    nombre = ui.pedir_texto("Nombre del usuario a resetear")
    if nombre is None:
        return
    clave = ui.pedir_clave("Clave nueva")
    exito, mensaje = resetear_clave(usuarios, nombre, clave)
    if exito:
        persistencia.guardar(ARCHIVO_USUARIOS, usuarios)   # punto transaccional
        ui.mostrar_exito(mensaje)
    else:
        ui.mostrar_error(mensaje)


# ============================================================================
#  Reportes
# ============================================================================

def flujo_recaudacion(ventas: dict) -> None:
    """Reporte de recaudación total: suma todos los precio_pagado con reduce."""
    precios = precios_de_ventas(ventas)
    total = calcular_recaudacion(precios)
    ui.mostrar_recaudacion(total, len(precios))


def flujo_destinos(viajes: dict) -> None:
    """Reporte de destinos activos únicos (conjunto derivado de los viajes activos)."""
    ui.mostrar_destinos(destinos_activos_unicos(viajes))
