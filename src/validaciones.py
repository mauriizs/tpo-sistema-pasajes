"""
CAPA 1 - Lógica pura: validaciones de formato y normalización de texto.

Funciones puras: reciben datos y devuelven datos. No imprimen, no piden input,
no tocan archivos. No dependen de ningún otro módulo del proyecto.

Acá viven las validaciones de FORMATO del dato (resueltas con regex), no las
reglas de negocio. Cada función responde una sola pregunta: ¿el dato tiene la
forma correcta? Es donde pegan los tests unitarios de la Capa 1.
"""

import re

# Patrones de formato (regex), compilados una vez al importar el módulo.
_PATRON_DNI = re.compile(r"^\d{7,8}$")
_PATRON_EMAIL = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
_PATRON_TELEFONO = re.compile(r"^\d{8,15}$")
_PATRON_FECHA = re.compile(r"^\d{2}/\d{2}/\d{4}$")
_PATRON_HORA = re.compile(r"^\d{2}:\d{2}$")

# Tope de días por mes (índice 1..12). Febrero acepta 29 sin chequear bisiesto
# (decisión consciente, ver arquitectura 4.1): la lógica de años bisiestos es
# complejidad de calendario que ningún requisito pide.
_DIAS_POR_MES = {
    1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31,
}


def es_dni_valido(dni: str) -> bool:
    """True si dni tiene exactamente 7 u 8 dígitos numéricos."""
    return _PATRON_DNI.match(dni) is not None


def es_email_valido(email: str) -> bool:
    """True si email tiene formato básico usuario@dominio.extension."""
    return _PATRON_EMAIL.match(email) is not None


def es_telefono_valido(telefono: str) -> bool:
    """True si telefono tiene entre 8 y 15 dígitos numéricos."""
    return _PATRON_TELEFONO.match(telefono) is not None


def es_fecha_valida(fecha: str) -> bool:
    """True si fecha tiene formato DD/MM/AAAA y el día es válido para el mes.
       El tope de día es POR MES: 31 para ene/mar/may/jul/ago/oct/dic, 30 para
       abr/jun/sep/nov, y 29 para febrero SIN chequear año bisiesto (se acepta
       29/02 aunque el año no sea bisiesto, y se declara en la defensa).
       NO valida que la fecha sea futura, solo la integridad del dato."""
    if _PATRON_FECHA.match(fecha) is None:
        return False
    dia = int(fecha[0:2])
    mes = int(fecha[3:5])
    if mes < 1 or mes > 12:
        return False
    return 1 <= dia <= _DIAS_POR_MES[mes]


def es_hora_valida(hora: str) -> bool:
    """True si hora tiene formato HH:MM con hora 00-23 y minutos 00-59."""
    if _PATRON_HORA.match(hora) is None:
        return False
    h = int(hora[0:2])
    m = int(hora[3:5])
    return 0 <= h <= 23 and 0 <= m <= 59


def normalizar_texto(texto: str) -> str:
    """Devuelve texto sin espacios al borde y en minúsculas (strip + lower).
       Para nombres de usuario, destinos, etc. NO usar en claves."""
    return texto.strip().lower()


def texto_no_vacio(texto: str) -> bool:
    """True si texto tiene contenido tras strip (para empresa, origen, destino)."""
    return len(texto.strip()) > 0
