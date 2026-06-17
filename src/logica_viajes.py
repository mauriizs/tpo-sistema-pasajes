"""
CAPA 3 - Dominio: reglas de negocio de viajes.

Opera sobre los diccionarios `viajes` y `ventas` (los recibe por parámetro) y
devuelve resultados. NUNCA hace print()/input(), NUNCA toca disco (lo orquesta
la Capa 5). Las reglas que pueden "fallar por regla" devuelven (exito, mensaje).

Importa de la Capa 1 (validaciones, asientos) para normalizar texto y derivar la
ocupación desde las ventas. NO importa persistencia (el dominio no persiste).
"""

from validaciones import normalizar_texto
from asientos import construir_grilla, contar_libres, FILAS, COLUMNAS

# Total de asientos del micro (constante del sistema, 5x4 = 20).
_TOTAL_ASIENTOS = FILAS * COLUMNAS


def proximo_id_viaje(viajes: dict) -> str:
    """Calcula el siguiente ID de viaje: 'V' + (max número existente + 1),
       con padding mínimo de 3 dígitos. Dict vacío → 'V001'."""
    # Se toma el MÁXIMO de los números existentes (no la cantidad): contar
    # fallaría si alguna vez se borró un viaje y quedaron huecos.
    maximo = 0
    for id_viaje in viajes:
        numero = int(id_viaje[1:])  # saca la 'V' del principio
        if numero > maximo:
            maximo = numero
    return "V" + str(maximo + 1).zfill(3)


def alta_viaje(viajes: dict, empresa: str, origen: str, destino: str,
               fecha: str, hora: str, precio_base: float) -> tuple[bool, str]:
    """Crea un viaje nuevo con ID autogenerado (V + max+1) y estado 'activo'.
       Normaliza el destino con normalizar_texto (strip+lower) ANTES de guardarlo,
       para que quede en forma canónica (el reporte de destinos únicos deduplica y
       la búsqueda por destino es consistente). empresa y origen se guardan tal cual
       (strip), no se normalizan a minúsculas. Devuelve (True, id_generado)."""
    nuevo_id = proximo_id_viaje(viajes)
    viajes[nuevo_id] = {
        "empresa": empresa.strip(),
        "origen": origen.strip(),
        "destino": normalizar_texto(destino),
        "fecha": fecha,
        "hora": hora,
        "precio_base": precio_base,
        "estado": "activo",
    }
    return (True, nuevo_id)


def modificar_viaje(viajes: dict, id_viaje: str, empresa: str | None,
                    fecha: str | None, hora: str | None,
                    precio_base: float | None) -> tuple[bool, str]:
    """Modifica SOLO empresa, fecha, hora y/o precio_base de un viaje existente.
       Origen y destino NO se tocan. Los parámetros en None se dejan sin cambiar."""
    if id_viaje not in viajes:
        return (False, "El viaje no existe")
    viaje = viajes[id_viaje]
    if empresa is not None:
        viaje["empresa"] = empresa.strip()
    if fecha is not None:
        viaje["fecha"] = fecha
    if hora is not None:
        viaje["hora"] = hora
    if precio_base is not None:
        viaje["precio_base"] = precio_base
    return (True, f"Viaje {id_viaje} modificado")


def viaje_tiene_ventas(ventas: dict, id_viaje: str) -> bool:
    """True si existe al menos una venta con ese id_viaje."""
    for venta in ventas.values():
        if venta["id_viaje"] == id_viaje:
            return True
    return False


def cancelar_o_borrar_viaje(viajes: dict, ventas: dict, id_viaje: str) -> tuple[bool, str]:
    """Si el viaje NO tiene ventas → lo borra del dict (borrado físico).
       Si tiene ventas → pasa estado a 'cancelado' (soft-delete, preserva integridad).
       Devuelve (True, mensaje indicando qué acción se tomó)."""
    if id_viaje not in viajes:
        return (False, "El viaje no existe")
    if viaje_tiene_ventas(ventas, id_viaje):
        viajes[id_viaje]["estado"] = "cancelado"
        return (True, f"Viaje {id_viaje} cancelado (tiene ventas, no se borra)")
    del viajes[id_viaje]
    return (True, f"Viaje {id_viaje} borrado (no tenía ventas)")


def ventas_de_viaje(ventas: dict, id_viaje: str) -> list[dict]:
    """Devuelve la lista de ventas que pertenecen a un viaje (filtradas por id_viaje).
       Se usa para derivar grilla y conjunto de DNIs."""
    return [venta for venta in ventas.values() if venta["id_viaje"] == id_viaje]


def buscar_viajes(viajes: dict, ventas: dict, origen: str | None, destino: str | None,
                  fecha: str | None, solo_vendibles: bool) -> list[dict]:
    """Motor de consultas único. Filtra con filter + lambda según los criterios dados
       (los None se ignoran). El match de origen y destino es EXACTO sobre texto
       normalizado. fecha matchea como string exacto. Si solo_vendibles=True (boletero):
       solo estado 'activo' y con asientos libres. Si False (admin): todos. Cada viaje
       devuelto es una copia de su dict enriquecida con: `id_viaje` (str), `ocupacion`
       (int 0-100, cada asiento equivale a 5%) y `libres` (int)."""
    resultado = []
    # Se recorre con sus claves para poder estampar id_viaje en la copia.
    ids = filter(
        lambda id_v: _coincide(viajes[id_v], origen, destino, fecha),
        viajes,
    )
    for id_viaje in ids:
        viaje = viajes[id_viaje]
        libres = contar_libres(construir_grilla(ventas_de_viaje(ventas, id_viaje)))
        # Vista vendible: solo activos con al menos un asiento libre.
        if solo_vendibles and (viaje["estado"] != "activo" or libres == 0):
            continue
        ocupados = _TOTAL_ASIENTOS - libres
        copia = dict(viaje)
        copia["id_viaje"] = id_viaje
        copia["libres"] = libres
        copia["ocupacion"] = round(ocupados / _TOTAL_ASIENTOS * 100)
        resultado.append(copia)
    return resultado


def _coincide(viaje: dict, origen: str | None, destino: str | None,
              fecha: str | None) -> bool:
    """Helper privado: True si el viaje matchea los criterios no-None.
       origen/destino se comparan normalizados (exacto); fecha como string exacto."""
    if origen is not None and normalizar_texto(viaje["origen"]) != normalizar_texto(origen):
        return False
    if destino is not None and normalizar_texto(viaje["destino"]) != normalizar_texto(destino):
        return False
    if fecha is not None and viaje["fecha"] != fecha:
        return False
    return True


def destinos_activos_unicos(viajes: dict) -> set[str]:
    """Conjunto de destinos de los viajes con estado 'activo' (para el reporte admin).
       La deduplicación es correcta porque el destino se guarda normalizado en el alta."""
    return {
        viaje["destino"]
        for viaje in viajes.values()
        if viaje["estado"] == "activo"
    }
