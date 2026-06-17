"""
Suite de pruebas unitarias (unittest, librería estándar — NO pytest).

Se testea la CAPA 1 (funciones puras) y las reglas del DOMINIO (Capa 3).
NO se testea ui.py, los menús ni persistencia.py (ver arquitectura 5.2).

Cada test arma sus propios datos de juguete: no lee data/. Se corre con:
    python -m unittest        (desde la carpeta src/)
"""

import os
import sys
import unittest

# Permite importar los módulos de src/ sin importar desde dónde se ejecute
# el test (portabilidad: "corre en cualquier computadora"). El test vive en
# src/tests/, así que su carpeta padre es src/.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import validaciones
import finanzas
import asientos
import logica_usuarios


class TestValidaciones(unittest.TestCase):
    """Casos de la Capa 1: validaciones de formato y normalización."""

    # ---- es_dni_valido ----
    def test_dni_valido(self):
        self.assertTrue(validaciones.es_dni_valido("38123456"))
        self.assertTrue(validaciones.es_dni_valido("1234567"))  # 7 dígitos

    def test_dni_invalido(self):
        self.assertFalse(validaciones.es_dni_valido("abc"))
        self.assertFalse(validaciones.es_dni_valido("123"))          # corto
        self.assertFalse(validaciones.es_dni_valido("38.123.456"))   # con puntos
        self.assertFalse(validaciones.es_dni_valido("123456789"))    # 9 dígitos
        self.assertFalse(validaciones.es_dni_valido(""))

    # ---- es_email_valido ----
    def test_email_valido(self):
        self.assertTrue(validaciones.es_email_valido("a@b.com"))
        self.assertTrue(validaciones.es_email_valido("pepe@mail.com.ar"))

    def test_email_invalido(self):
        self.assertFalse(validaciones.es_email_valido("a.com"))   # sin @
        self.assertFalse(validaciones.es_email_valido("a@b"))     # sin dominio.ext
        self.assertFalse(validaciones.es_email_valido(""))

    # ---- es_telefono_valido ----
    def test_telefono_valido(self):
        self.assertTrue(validaciones.es_telefono_valido("1145678901"))
        self.assertTrue(validaciones.es_telefono_valido("12345678"))  # 8 dígitos

    def test_telefono_invalido(self):
        self.assertFalse(validaciones.es_telefono_valido("abc"))
        self.assertFalse(validaciones.es_telefono_valido("123"))            # corto
        self.assertFalse(validaciones.es_telefono_valido("11-4567-8901"))   # símbolos

    # ---- es_fecha_valida ----
    def test_fecha_valida(self):
        self.assertTrue(validaciones.es_fecha_valida("20/05/2026"))
        self.assertTrue(validaciones.es_fecha_valida("29/02/2025"))  # 29/02 se acepta

    def test_fecha_invalida(self):
        self.assertFalse(validaciones.es_fecha_valida("32/01/2026"))  # día > 31
        self.assertFalse(validaciones.es_fecha_valida("00/05/2026"))  # día 0
        self.assertFalse(validaciones.es_fecha_valida("31/04/2026"))  # abril tiene 30
        self.assertFalse(validaciones.es_fecha_valida("10/13/2026"))  # mes > 12
        self.assertFalse(validaciones.es_fecha_valida("hola"))
        self.assertFalse(validaciones.es_fecha_valida("1/5/2026"))    # sin padding

    # ---- es_hora_valida ----
    def test_hora_valida(self):
        self.assertTrue(validaciones.es_hora_valida("14:30"))
        self.assertTrue(validaciones.es_hora_valida("00:00"))
        self.assertTrue(validaciones.es_hora_valida("23:59"))

    def test_hora_invalida(self):
        self.assertFalse(validaciones.es_hora_valida("25:99"))
        self.assertFalse(validaciones.es_hora_valida("1430"))   # sin :
        self.assertFalse(validaciones.es_hora_valida("12:60"))  # minutos fuera

    # ---- normalizar_texto ----
    def test_normalizar_texto(self):
        self.assertEqual(validaciones.normalizar_texto("  Bariloche  "), "bariloche")
        self.assertEqual(validaciones.normalizar_texto("MAURI_Admin"), "mauri_admin")

    # ---- texto_no_vacio ----
    def test_texto_no_vacio(self):
        self.assertTrue(validaciones.texto_no_vacio("Via Bariloche"))
        self.assertFalse(validaciones.texto_no_vacio(""))
        self.assertFalse(validaciones.texto_no_vacio("    "))  # solo espacios


class TestFinanzas(unittest.TestCase):
    """Casos de la Capa 1: cálculos de dinero."""

    # ---- aplicar_recargo ----
    def test_aplicar_recargo(self):
        # 50000 * 1.16 = 58000. Se compara con assertAlmostEqual porque la
        # multiplicación en float arrastra error de representación
        # (57999.99999999999); el redondeo a 2 decimales es de presentación.
        self.assertAlmostEqual(finanzas.aplicar_recargo(50000), 58000.0, places=2)

    def test_aplicar_recargo_cero(self):
        self.assertEqual(finanzas.aplicar_recargo(0), 0.0)

    # ---- calcular_recaudacion ----
    def test_calcular_recaudacion(self):
        self.assertEqual(finanzas.calcular_recaudacion([100.0, 200.0]), 300.0)

    def test_calcular_recaudacion_vacia(self):
        # Caso borde: lista vacía → 0.0 (no crashea)
        self.assertEqual(finanzas.calcular_recaudacion([]), 0.0)

    def test_calcular_recaudacion_un_elemento(self):
        self.assertEqual(finanzas.calcular_recaudacion([58000.0]), 58000.0)

    # ---- normalizar_precio ----
    def test_normalizar_precio_coma(self):
        # El usuario argentino tipea coma por reflejo
        self.assertEqual(finanzas.normalizar_precio("50000,50"), "50000.50")

    def test_normalizar_precio_espacios(self):
        self.assertEqual(finanzas.normalizar_precio("  50000  "), "50000")

    def test_normalizar_precio_no_convierte(self):
        # Solo prepara el texto; NO convierte a float (devuelve str)
        self.assertEqual(finanzas.normalizar_precio("hola"), "hola")


class TestAsientos(unittest.TestCase):
    """Casos de la Capa 1: grilla de asientos derivada de las ventas."""

    # ---- construir_grilla ----
    def test_grilla_sin_ventas_toda_libre(self):
        grilla = asientos.construir_grilla([])
        self.assertEqual(len(grilla), asientos.FILAS)
        self.assertEqual(len(grilla[0]), asientos.COLUMNAS)
        # Todas las celdas libres
        self.assertEqual(asientos.contar_libres(grilla), 20)

    def test_grilla_marca_celda_ocupada(self):
        ventas = [{"dni": "38123456", "fila": 2, "columna": 3}]
        grilla = asientos.construir_grilla(ventas)
        # La celda (2,3) en base 1 → índice [1][2]
        self.assertEqual(grilla[1][2], asientos.OCUPADO)
        # El resto sigue libre: 19 de 20
        self.assertEqual(asientos.contar_libres(grilla), 19)

    def test_grilla_filas_independientes(self):
        # Marcar una celda NO debe afectar a otra fila (sin referencia compartida)
        ventas = [{"dni": "1", "fila": 1, "columna": 1}]
        grilla = asientos.construir_grilla(ventas)
        self.assertEqual(grilla[0][0], asientos.OCUPADO)
        self.assertEqual(grilla[1][0], asientos.LIBRE)

    # ---- asiento_en_rango ----
    def test_asiento_en_rango(self):
        self.assertTrue(asientos.asiento_en_rango(1, 1))
        self.assertTrue(asientos.asiento_en_rango(5, 4))

    def test_asiento_fuera_de_rango(self):
        self.assertFalse(asientos.asiento_en_rango(6, 2))   # fila > 5
        self.assertFalse(asientos.asiento_en_rango(1, 0))   # columna 0
        self.assertFalse(asientos.asiento_en_rango(0, 1))   # fila 0
        self.assertFalse(asientos.asiento_en_rango(1, 5))   # columna > 4

    # ---- asiento_esta_libre ----
    def test_asiento_libre(self):
        grilla = asientos.construir_grilla([])
        self.assertTrue(asientos.asiento_esta_libre(grilla, 2, 3))

    def test_asiento_ocupado(self):
        grilla = asientos.construir_grilla([{"dni": "1", "fila": 2, "columna": 3}])
        self.assertFalse(asientos.asiento_esta_libre(grilla, 2, 3))

    def test_asiento_libre_fuera_de_rango(self):
        # Coordenada fuera de rango → False (no indexa, no wraparound negativo)
        grilla = asientos.construir_grilla([])
        self.assertFalse(asientos.asiento_esta_libre(grilla, 6, 2))
        self.assertFalse(asientos.asiento_esta_libre(grilla, 1, 0))

    # ---- contar_libres ----
    def test_contar_libres(self):
        ventas = [
            {"dni": "1", "fila": 1, "columna": 1},
            {"dni": "2", "fila": 1, "columna": 2},
        ]
        grilla = asientos.construir_grilla(ventas)
        self.assertEqual(asientos.contar_libres(grilla), 18)

    # ---- dnis_del_viaje ----
    def test_dnis_del_viaje(self):
        ventas = [
            {"dni": "38123456", "fila": 1, "columna": 1},
            {"dni": "30111222", "fila": 1, "columna": 2},
        ]
        self.assertEqual(asientos.dnis_del_viaje(ventas), {"38123456", "30111222"})

    def test_dnis_del_viaje_vacio(self):
        self.assertEqual(asientos.dnis_del_viaje([]), set())


class TestUsuarios(unittest.TestCase):
    """Casos del Dominio (Capa 3): reglas de usuarios. Cada test arma su dict."""

    def _usuarios_de_juguete(self):
        # Dos admins activos + un boletero, para probar el anti-admin-suicida.
        return {
            "gestor": {"clave": "1234", "rol": "administrador", "estado": "activo"},
            "gestor2": {"clave": "abcd", "rol": "administrador", "estado": "activo"},
            "vende1": {"clave": "pass", "rol": "boletero", "estado": "activo"},
        }

    # ---- credencial_valida ----
    def test_login_ok_devuelve_rol(self):
        usuarios = self._usuarios_de_juguete()
        exito, rol = logica_usuarios.credencial_valida(usuarios, "gestor", "1234")
        self.assertTrue(exito)
        self.assertEqual(rol, "administrador")

    def test_login_normaliza_usuario(self):
        # Tipear "GESTOR" con mayúsculas y espacios igual loguea
        usuarios = self._usuarios_de_juguete()
        exito, rol = logica_usuarios.credencial_valida(usuarios, "  GESTOR  ", "1234")
        self.assertTrue(exito)

    def test_login_clave_incorrecta(self):
        usuarios = self._usuarios_de_juguete()
        exito, _ = logica_usuarios.credencial_valida(usuarios, "gestor", "mala")
        self.assertFalse(exito)

    def test_login_clave_no_se_normaliza(self):
        # La clave es case-sensitive: "PASS" no es "pass"
        usuarios = self._usuarios_de_juguete()
        exito, _ = logica_usuarios.credencial_valida(usuarios, "vende1", "PASS")
        self.assertFalse(exito)

    def test_login_usuario_inactivo(self):
        usuarios = self._usuarios_de_juguete()
        usuarios["vende1"]["estado"] = "inactivo"
        exito, _ = logica_usuarios.credencial_valida(usuarios, "vende1", "pass")
        self.assertFalse(exito)

    # ---- crear_usuario ----
    def test_crear_usuario_nuevo(self):
        usuarios = self._usuarios_de_juguete()
        exito, _ = logica_usuarios.crear_usuario(usuarios, "vende2", "clave", "boletero")
        self.assertTrue(exito)
        self.assertIn("vende2", usuarios)
        self.assertEqual(usuarios["vende2"]["estado"], "activo")

    def test_crear_usuario_existente_distinta_capitalizacion(self):
        # "Gestor" ya existe como "gestor" → anti-clones lo rechaza
        usuarios = self._usuarios_de_juguete()
        exito, _ = logica_usuarios.crear_usuario(usuarios, "Gestor", "x", "administrador")
        self.assertFalse(exito)

    def test_crear_usuario_nombre_admin_reservado(self):
        usuarios = self._usuarios_de_juguete()
        exito, _ = logica_usuarios.crear_usuario(usuarios, "admin", "x", "administrador")
        self.assertFalse(exito)
        self.assertNotIn("admin", usuarios)

    def test_crear_usuario_clave_no_se_normaliza(self):
        usuarios = self._usuarios_de_juguete()
        logica_usuarios.crear_usuario(usuarios, "nuevo", "ClAvE123", "boletero")
        self.assertEqual(usuarios["nuevo"]["clave"], "ClAvE123")

    # ---- desactivar_usuario ----
    def test_desactivar_con_otro_admin_activo(self):
        usuarios = self._usuarios_de_juguete()
        exito, _ = logica_usuarios.desactivar_usuario(usuarios, "gestor")
        self.assertTrue(exito)
        self.assertEqual(usuarios["gestor"]["estado"], "inactivo")

    def test_desactivar_ultimo_admin_activo_bloquea(self):
        usuarios = self._usuarios_de_juguete()
        # Dejar a "gestor" como único admin activo
        usuarios["gestor2"]["estado"] = "inactivo"
        exito, _ = logica_usuarios.desactivar_usuario(usuarios, "gestor")
        self.assertFalse(exito)
        self.assertEqual(usuarios["gestor"]["estado"], "activo")  # no se tocó

    def test_desactivar_ya_inactivo(self):
        usuarios = self._usuarios_de_juguete()
        usuarios["vende1"]["estado"] = "inactivo"
        exito, mensaje = logica_usuarios.desactivar_usuario(usuarios, "vende1")
        self.assertFalse(exito)
        self.assertIn("inactivo", mensaje.lower())

    def test_desactivar_inexistente(self):
        usuarios = self._usuarios_de_juguete()
        exito, _ = logica_usuarios.desactivar_usuario(usuarios, "fantasma")
        self.assertFalse(exito)

    # ---- resetear_clave ----
    def test_resetear_clave_reactiva(self):
        usuarios = self._usuarios_de_juguete()
        usuarios["vende1"]["estado"] = "inactivo"
        exito, _ = logica_usuarios.resetear_clave(usuarios, "vende1", "nueva")
        self.assertTrue(exito)
        self.assertEqual(usuarios["vende1"]["estado"], "activo")
        self.assertEqual(usuarios["vende1"]["clave"], "nueva")

    def test_resetear_clave_normaliza_nombre(self):
        # Encuentra al usuario aunque se tipee con otra capitalización
        usuarios = self._usuarios_de_juguete()
        exito, _ = logica_usuarios.resetear_clave(usuarios, "VENDE1", "nueva")
        self.assertTrue(exito)

    def test_resetear_clave_inexistente(self):
        usuarios = self._usuarios_de_juguete()
        exito, _ = logica_usuarios.resetear_clave(usuarios, "fantasma", "nueva")
        self.assertFalse(exito)

    # ---- contar_admins_activos ----
    def test_contar_admins_activos(self):
        usuarios = self._usuarios_de_juguete()
        self.assertEqual(logica_usuarios.contar_admins_activos(usuarios), 2)

    def test_contar_admins_uno_inactivo(self):
        usuarios = self._usuarios_de_juguete()
        usuarios["gestor2"]["estado"] = "inactivo"
        self.assertEqual(logica_usuarios.contar_admins_activos(usuarios), 1)

    # ---- existe_usuario ----
    def test_existe_usuario_normaliza(self):
        usuarios = self._usuarios_de_juguete()
        self.assertTrue(logica_usuarios.existe_usuario(usuarios, "  Gestor "))
        self.assertFalse(logica_usuarios.existe_usuario(usuarios, "fantasma"))

    # ---- listar_usuarios ----
    def test_listar_usuarios(self):
        usuarios = self._usuarios_de_juguete()
        lista = logica_usuarios.listar_usuarios(usuarios)
        self.assertEqual(len(lista), 3)
        self.assertIn(("vende1", "boletero", "activo"), lista)


if __name__ == "__main__":
    unittest.main()
