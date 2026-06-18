# Punto de entrada del sistema Nexus Viajes - TPO Grupo

"""
CAPA 5 - Orquestación: punto de entrada del sistema.
Carga el estado, decide modo fábrica/normal, pide datos con ui, aplica reglas
con el dominio y rutea según el rol. El estado (los tres diccionarios) vive acá
y se pasa por parámetro hacia abajo: una sola fuente de estado, sin globales.
"""

import sys

import persistencia
import ui
import validaciones
import logica_usuarios

# Nombres de archivo como constantes.
ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_VIAJES = "viajes.json"
ARCHIVO_VENTAS = "ventas.json"


def cargar_estado() -> tuple[dict, dict, dict]:
    """Carga usuarios, viajes, ventas desde disco. Auto-reparación: si usuarios
       quedó vacío, inyecta admin/admin (inserción directa, no pasa por crear_usuario)."""
    usuarios = persistencia.cargar(ARCHIVO_USUARIOS)
    viajes = persistencia.cargar(ARCHIVO_VIAJES)
    ventas = persistencia.cargar(ARCHIVO_VENTAS)
    if not usuarios:
        # Sin usuarios el sistema quedaría muerto: se inyecta el admin/admin de
        # fábrica en memoria (lo persiste el flujo de fábrica).
        usuarios["admin"] = {
            "clave": "admin",
            "rol": "administrador",
            "estado": "activo",
        }
    return usuarios, viajes, ventas


def esta_en_modo_fabrica(usuarios: dict) -> bool:
    """True si existe el admin/admin de fábrica (credenciales por defecto)."""
    admin = usuarios.get("admin")
    return admin is not None and admin["clave"] == "admin"


def flujo_modo_fabrica(usuarios: dict) -> None:
    """Crea el admin real, elimina admin/admin, guarda. Ocurre una sola vez en
       la vida del sistema. No se permite cancelar: el sistema no puede quedar
       sin un administrador real."""
    ui.mostrar_banner_fabrica()
    # Bucle hasta crear con éxito el administrador real.
    while True:
        # permitir_cancelar=False: salir de fábrica sin admin dejaría el sistema muerto.
        nombre = ui.pedir_texto("Nombre del nuevo administrador", permitir_cancelar=False)
        clave = ui.pedir_clave("Clave")
        repetir = ui.pedir_clave("Repetir clave")
        if clave != repetir:
            ui.mostrar_error("Las claves no coinciden. Probá de nuevo.")
            continue
        exito, mensaje = logica_usuarios.crear_usuario(
            usuarios, nombre, clave, "administrador")
        if not exito:
            ui.mostrar_error(mensaje)
            continue
        break
    # El admin real ya está creado: se elimina el admin/admin de fábrica.
    del usuarios["admin"]
    persistencia.guardar(ARCHIVO_USUARIOS, usuarios)
    ui.mostrar_exito("Administrador creado. El sistema está listo para usarse.")


def flujo_login(usuarios: dict) -> tuple[str, str] | None:
    """Maneja login con contador de 3 intentos. Devuelve (usuario_normalizado, rol)
       o None (si canceló con '0' o agotó los intentos). El bloqueo al 3er fallo
       es robustez/UX, no seguridad real: no se hace exit(), se vuelve al menú."""
    intentos = 0
    while intentos < 3:
        usuario = ui.pedir_texto("Usuario", permitir_cancelar=True)
        if usuario is None:
            return None  # canceló con '0'
        clave = ui.pedir_clave("Clave")
        exito, resultado = logica_usuarios.credencial_valida(usuarios, usuario, clave)
        if exito:
            # resultado transporta el ROL cuando exito=True. El usuario_actual se
            # devuelve normalizado: es la clave del dict y lo que se estampa en las ventas.
            return (validaciones.normalizar_texto(usuario), resultado)
        intentos += 1
        ui.mostrar_error(resultado)
        if intentos < 3:
            ui.mostrar_info(f"Intentos restantes: {3 - intentos}")
    ui.mostrar_error("Demasiados intentos fallidos. Volviendo al menú principal.")
    return None


def main() -> None:
    """Punto de entrada. Carga los 3 archivos, decide modo fábrica/normal,
       corre el bucle del menú principal."""
    # Fuerza UTF-8 en la consola para que tildes/ñ se vean bien en Windows.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    ui.mostrar_bienvenida()
    usuarios, viajes, ventas = cargar_estado()

    if esta_en_modo_fabrica(usuarios):
        flujo_modo_fabrica(usuarios)

    # Bucle del Menú Principal "ciego".
    while True:
        ui.mostrar_menu_principal()
        opcion = ui.pedir_opcion("Elegí una opción:", {"1", "2", "3"})
        if opcion == "1":
            credenciales = flujo_login(usuarios)
            if credenciales is not None:
                usuario_actual, rol = credenciales
                ui.mostrar_exito(f"Sesión iniciada como {usuario_actual} ({rol}).")
                # Import diferido: los menús solo se necesitan tras un login exitoso.
                if rol == "administrador":
                    import menu_admin
                    menu_admin.menu_admin(usuarios, viajes, ventas, usuario_actual)
                else:
                    import menu_boletero
                    menu_boletero.menu_boletero(usuarios, viajes, ventas, usuario_actual)
        elif opcion == "2":
            ui.mostrar_ayuda()
        elif opcion == "3":
            ui.mostrar_info("¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
