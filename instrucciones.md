# 🤖 Contexto y Arquitectura del Proyecto (TP1 - Programación 1)

## 🎯 Objetivo del Asistente (Tú)
Tu rol es actuar como programador en par para desarrollar este sistema en Python. **Debes respetar estrictamente el nivel de un alumno de primer año universitario**. No sugieras soluciones, librerías, paradigmas o estructuras de datos que excedan el alcance detallado en este documento. Si se te pide resolver un error, hazlo utilizando únicamente las herramientas permitidas.

## 🚌 Descripción General
El sistema es un **Gestor de Ventas de Pasajes de Micro** que funciona por consola.
Flujo principal:
1. Buscar viajes (filtrando por Origen, Destino y Fecha).
2. Comprar un pasaje (seleccionar ID, elegir asiento en matriz, validar datos del pasajero, calcular recargos y registrar venta).
3. Ver recaudación total del sistema.
4. Salir.

---

## 💾 Estructura de Datos (ESTRICTO)
Para respetar las restricciones académicas, **NO SE DEBEN USAR DICCIONARIOS COMPLEJOS**. Toda la información en memoria debe estructurarse usando **Listas y Listas Anidadas**.

### 1. Catálogo de Viajes (`catalogo_viajes`)
Es una Lista de Listas. Cada sub-lista respeta estrictamente estos índices:
* `[0]` -> ID del viaje (String, ej: "1")
* `[1]` -> Empresa (String)
* `[2]` -> Origen (String)
* `[3]` -> Destino (String)
* `[4]` -> Fecha (String, formato DD/MM)
* `[5]` -> Precio Base (Float o Int)
* `[6]` -> Matriz de Asientos (Lista bidimensional de Strings: "L" para Libre, "O" para Ocupado)

**Ejemplo:**
`viajes = [ ["1", "Via Bariloche", "Buenos Aires", "Bariloche", "20/05", 50000, [["L", "O"], ["L", "L"]]] ]`

### 2. Registro de Ventas (`ventas_diarias`)
Es una lista unidimensional simple que almacena números (floats/ints) correspondientes al precio final de cada pasaje vendido, para luego ser procesada. Ejemplo: `[58000, 45000]`

---

## 🛑 REGLAS ESTRICTAS DE CÓDIGO (Límites del Proyecto)

### ✅ OBLIGATORIO USAR:
1. **Matrices:** La visualización y actualización de asientos debe recorrer una lista bidimensional.
2. **Programación Funcional:** * `filter()`: Exclusivo para buscar viajes en el catálogo.
   * `map()`: Exclusivo para calcular el precio final (precio base + 16% de recargos).
   * `reduce()` (de `functools`): Exclusivo para sumar la lista de `ventas_diarias`.
   * **`lambda`**: Se deben usar funciones anónimas dentro de los maps, filters y reduces.
3. **RegEx (Librería `re`):** Uso obligatorio para validar Inputs del usuario (DNI numérico, Email válido, Teléfono, y formato de Fecha DD/MM).
4. **Validación sin Excepciones:** No usar bloques `try/except`. Para evitar crasheos en ingresos numéricos (como elegir fila/columna), validar antes con RegEx o `.isdigit()`.

### 🚫 PROHIBIDO USAR:
1. **Archivos o Bases de Datos:** No usar `.json`, `.csv`, `.txt`, ni SQL. Todo es efímero en memoria (Variables hardcodeadas).
2. **Programación Orientada a Objetos (POO):** Nada de `class`, `self` u objetos. Todo se resuelve con programación estructurada (funciones `def` y bucles).
3. **Recursividad:** Prohibido. Usar `while True` o `for`.
4. **Múltiples pasajeros / Carritos:** El flujo de compra es de "Sólo Ida" y de "1 solo pasajero por vez". No agregar lógicas de carritos de compras.
5. **Diccionarios para lógica central:** Evitar su uso para estructurar el catálogo.

---

## 🛠️ Casos Borde a Contemplar (QA)
Al sugerir código para la entrada de datos, siempre debes contemplar estas validaciones lógicas:
* **El botón de arrepentimiento:** Al pedir Fila y Columna del asiento, permitir que el ingreso de `'0'` cancele la operación y haga un `break` al menú.
* **El Asiento Inexistente:** Validar que la fila y columna ingresadas no superen los límites de la matriz (IndexError) antes de buscar.
* **ID Inexistente:** Si el usuario busca un ID de viaje que `filter()` no encuentra, mostrar error y volver al menú, no intentar iterar una lista vacía.
* **Caja Vacía en `reduce`:** Si se llama a Ver Recaudación y la lista `ventas_diarias` está vacía, atajarlo con un condicional para que `reduce()` no lance TypeError.

---

## 📂 Modularización del Proyecto
Generar funciones puras y con una única responsabilidad. Los módulos son:
* `a_main.py`: Punto de entrada, contiene el `while True` del Menú y llama a las demás funciones.
* `b_info.py`: Imprime los datos estáticos de la agencia.
* `c_busquedas.py`: Contiene la variable del catálogo hardcodeado y las funciones que usan `filter()`.
* `d_micro.py`: Funciones para imprimir la matriz de asientos formateada y actualizar un asiento de "L" a "O".
* `e_validaciones.py`: Todas las funciones que usan `re.match` o `re.fullmatch` (fechas, DNI, emails, limpieza de inputs).
* `f_finanzas.py`: Funciones económicas (`map` para recargos y `reduce` para totalizar caja).