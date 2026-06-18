"""
CAPA 3 - Dominio: reglas de negocio de usuarios.
Opera sobre el diccionario `usuarios`; no hace I/O ni toca disco. Las reglas que
pueden fallar devuelven (exito: bool, mensaje: str). Toda función normaliza el
nombre internamente (strip+lower) antes de buscar; la clave nunca se normaliza.
"""

from validaciones import normalizar_texto


def credencial_valida(usuarios: dict, usuario: str, clave: str) -> tuple[bool, str]:
    """Verifica login: que el usuario exista, la clave coincida y el estado sea 'activo'.
       Devuelve (True, rol) si es válido, (False, motivo) si no. Es el único caso donde
       el 2º campo, con exito=True, transporta el ROL (no un mensaje) para que el flujo rutee."""
    nombre = normalizar_texto(usuario)
    if nombre not in usuarios:
        return (False, "Usuario o clave incorrectos")
    datos = usuarios[nombre]
    if datos["clave"] != clave:
        return (False, "Usuario o clave incorrectos")
    if datos["estado"] != "activo":
        return (False, "El usuario se encuentra inactivo")
    return (True, datos["rol"])


def crear_usuario(usuarios: dict, nombre: str, clave: str, rol: str) -> tuple[bool, str]:
    """Alta de usuario. Normaliza el nombre → rechaza el nombre reservado "admin" →
       control de unicidad. Si no pasa → (False, motivo); si pasa → lo crea activo y
       (True, mensaje). La clave no se normaliza."""
    nombre_norm = normalizar_texto(nombre)
    if nombre_norm == "admin":
        return (False, 'El nombre "admin" está reservado y no puede usarse')
    if nombre_norm in usuarios:
        return (False, "Ya existe un usuario con ese nombre")
    usuarios[nombre_norm] = {
        "clave": clave,
        "rol": rol,
        "estado": "activo",
    }
    return (True, f'Usuario "{nombre_norm}" creado correctamente')


def desactivar_usuario(usuarios: dict, nombre: str) -> tuple[bool, str]:
    """Baja lógica. Si no existe o ya está inactivo → (False, motivo). Anti-admin-suicida:
       si es el último admin activo → (False, motivo) sin tocar nada. Si no, pasa a
       'inactivo' y (True, mensaje)."""
    nombre_norm = normalizar_texto(nombre)
    if nombre_norm not in usuarios:
        return (False, "El usuario no existe")
    datos = usuarios[nombre_norm]
    if datos["estado"] == "inactivo":
        return (False, "El usuario ya se encuentra inactivo")
    # Anti-admin-suicida: no se puede desactivar al último admin ACTIVO.
    if datos["rol"] == "administrador" and contar_admins_activos(usuarios) == 1:
        return (False, "No se puede desactivar al último administrador activo")
    datos["estado"] = "inactivo"
    return (True, f'Usuario "{nombre_norm}" desactivado')


def resetear_clave(usuarios: dict, nombre: str, clave_nueva: str) -> tuple[bool, str]:
    """Asigna la clave nueva y reactiva al usuario (estado = 'activo'). Es la única vía
       de rehabilitar a un usuario inactivo. La clave_nueva no se normaliza."""
    nombre_norm = normalizar_texto(nombre)
    if nombre_norm not in usuarios:
        return (False, "El usuario no existe")
    datos = usuarios[nombre_norm]
    datos["clave"] = clave_nueva
    datos["estado"] = "activo"
    return (True, f'Clave de "{nombre_norm}" restablecida y usuario reactivado')


def contar_admins_activos(usuarios: dict) -> int:
    """Cuenta usuarios con rol 'administrador' y estado 'activo'."""
    total = 0
    for datos in usuarios.values():
        if datos["rol"] == "administrador" and datos["estado"] == "activo":
            total += 1
    return total


def existe_usuario(usuarios: dict, nombre: str) -> bool:
    """True si el nombre (normalizado) ya es clave en el dict."""
    return normalizar_texto(nombre) in usuarios


def listar_usuarios(usuarios: dict) -> list[tuple[str, str, str]]:
    """Devuelve [(nombre, rol, estado), ...] para que ui muestre la lista de usuarios."""
    return [
        (nombre, datos["rol"], datos["estado"])
        for nombre, datos in usuarios.items()
    ]
