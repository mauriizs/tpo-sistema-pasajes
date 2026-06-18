"""
CAPA 2 - Persistencia: leer y escribir los archivos JSON de data/.
  · archivo inexistente  → {}  (primera ejecución)
  · archivo corrupto     → avisar y frenar el programa (nunca destruir datos)
La ruta a data/ se arma relativa al script (sin rutas absolutas), para que
funcione en cualquier computadora.
"""

import json
import os
import sys


def ruta_data(nombre_archivo: str) -> str:
    """Devuelve la ruta a data/<nombre_archivo> de forma portable
       (relativa al script, funciona en cualquier computadora).
       OJO: data/ es hermano de src/ (no hijo), así que la ruta sube un nivel
       desde el script."""
    carpeta_script = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(carpeta_script, "..", "data", nombre_archivo)


def cargar(nombre_archivo: str) -> dict:
    """Lee un JSON de data/ y lo devuelve como dict.
       Si el archivo no existe (FileNotFoundError) → devuelve {} (primera ejecución).
       Si el archivo está corrupto (JSONDecodeError) → avisa y FRENA el programa
       (nunca devuelve {} ante corrupción: eso destruiría datos al sobrescribir)."""
    ruta = ruta_data(nombre_archivo)
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        # Primera ejecución: el archivo todavía no existe. Es normal.
        return {}
    except json.JSONDecodeError:
        # Archivo dañado o a medio escribir: NO se trata como vacío, porque
        # sobrescribirlo destruiría datos reales recuperables a mano. Se frena.
        print(f"\nERROR: el archivo '{nombre_archivo}' está dañado o corrupto.")
        print("El programa se detiene para no sobrescribir datos. "
              "Revisá el archivo a mano.")
        sys.exit(1)


def guardar(nombre_archivo: str, estructura: dict) -> None:
    """Sobrescribe el JSON de data/ con la estructura completa.
       La ruta se arma relativa a la ubicación del script (sin rutas absolutas)."""
    ruta = ruta_data(nombre_archivo)
    with open(ruta, "w", encoding="utf-8") as archivo:
        # ensure_ascii=False para que tildes y ñ se guarden legibles;
        # indent=4 para que el JSON quede prolijo y editable a mano.
        json.dump(estructura, archivo, ensure_ascii=False, indent=4)
