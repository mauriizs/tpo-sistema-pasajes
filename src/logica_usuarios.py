"""
CAPA 3 - Dominio: reglas de negocio de usuarios.

Opera sobre el diccionario `usuarios` (lo recibe por parámetro) y devuelve
resultados. NUNCA hace print() ni input(), NUNCA toca disco (eso lo orquesta
la Capa 5). Las reglas que pueden "fallar por regla" devuelven una tupla
(exito: bool, mensaje: str).

Regla del módulo (arquitectura 4.5): TODA función que recibe un nombre de
usuario lo normaliza internamente con normalizar_texto (strip+lower) ANTES de
tocar el diccionario. La clave NUNCA se normaliza.
"""

from validaciones import normalizar_texto


def credencial_valida(usuarios: dict, usuario: str, clave: str) -> tuple[bool, str]:
    """Verifica login: que el usuario exista, la clave coincida y el estado sea 'activo'.
       Normaliza el usuario internamente (strip+lower) antes del lookup; la clave NO se normaliza.
       Devuelve (True, rol) si es válido, (False, motivo) si no.
       NOTA: este es el único caso donde el 2º campo de la tupla, cuando exito=True,
       transporta el ROL (no un mensaje), porque el flujo lo necesita para rutear."""
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
    """Alta de usuario. Orden interno: normaliza el nombre (strip+lower) →
       rechaza el nombre reservado "admin" (no recreable, protege el bootstrap de
       modo fábrica) → control de unicidad (anti-clones).
       Si el nombre es "admin" o ya existe → (False, motivo). Si no → lo crea activo y (True, mensaje).
       La clave NO se normaliza. Modifica el dict usuarios en memoria."""
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
    """Baja lógica. Orden interno: normaliza el nombre → si no existe → (False, motivo) →
       si YA está inactivo → (False, "El usuario ya se encuentra inactivo") sin tocar nada →
       anti-admin-suicida: si es el último admin ACTIVO → (False, motivo) sin tocar nada →
       en otro caso pasa estado a 'inactivo' y (True, mensaje). La guarda de "ya inactivo" va
       ANTES del anti-admin porque un usuario inactivo nunca puede ser el último admin activo."""
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
    """Normaliza el nombre internamente, ubica al usuario, le asigna la clave nueva
       Y lo reactiva (estado = 'activo'). Reactivar implica SIEMPRE clave nueva: es la única
       vía de rehabilitar a un usuario inactivo (no hay opción de menú "reactivar" aparte).
       La clave_nueva NO se normaliza."""
    nombre_norm = normalizar_texto(nombre)
    if nombre_norm not in usuarios:
        return (False, "El usuario no existe")
    datos = usuarios[nombre_norm]
    datos["clave"] = clave_nueva
    datos["estado"] = "activo"
    return (True, f'Clave de "{nombre_norm}" restablecida y usuario reactivado')


def contar_admins_activos(usuarios: dict) -> int:
    """Cuenta usuarios con rol 'administrador' Y estado 'activo'.
       Base del anti-admin-suicida."""
    total = 0
    for datos in usuarios.values():
        if datos["rol"] == "administrador" and datos["estado"] == "activo":
            total += 1
    return total


def existe_usuario(usuarios: dict, nombre: str) -> bool:
    """True si el nombre (normalizado internamente strip+lower) ya es clave en el dict (para anti-clones)."""
    return normalizar_texto(nombre) in usuarios


def listar_usuarios(usuarios: dict) -> list[tuple[str, str, str]]:
    """Devuelve [(nombre, rol, estado), ...] para que ui muestre el 'mapa' de usuarios."""
    return [
        (nombre, datos["rol"], datos["estado"])
        for nombre, datos in usuarios.items()
    ]
