# Contexto y Reglas del Proyecto (TP1 - Programación 1)

## 🎯 Objetivo del Asistente
Tu rol es ayudar a desarrollar el código de este proyecto asegurando que se cumplan **estrictamente** los requerimientos técnicos detallados a continuación. No debes sugerir soluciones, librerías o estructuras que excedan el alcance de esta primera entrega.

## 🚌 Descripción del Proyecto
El sistema es un **Gestor de Ventas de Pasajes de Micro** para terminales. El flujo principal es:
1.  Mostrar información de la empresa.
2.  Permitir al usuario buscar viajes en un catálogo filtrando por destino.
3.  Mostrar una cuadrícula de asientos disponibles para que el usuario elija.
4.  Solicitar y validar los datos personales del pasajero.
5.  Calcular precios con recargos y registrar la venta.
6.  Permitir consultar la recaudación total del sistema.

---

## 🛑 REGLAS ESTRICTAS DE CÓDIGO (Qué SI y qué NO usar)

### ✅ Lo que DEBE usarse obligatoriamente:
1.  **Matrices (Listas Bidimensionales):** El mapa de asientos del micro debe ser obligatoriamente una lista de listas (ej: matriz de 10 filas x 4 columnas).
2.  **Expresiones Regulares (RegEx):** Se debe usar la librería `re` para validar los inputs del usuario (DNI sin letras, Formato de Email correcto).
3.  **Programación Funcional:** * Uso de `filter()` para la búsqueda de viajes en el catálogo.
    * Uso de `map()` para transformar datos (ej. aplicar recargos a los precios).
    * Uso de `reduce()` (de `functools`) para cálculos totales (ej. sumar la recaudación del día).
    * Uso de funciones anónimas `lambda` junto a las herramientas anteriores.
4.  **Modularización:** El código debe estar separado en funciones claras, con un único punto de entrada en `main.py`.

### 🚫 Lo que ESTÁ PROHIBIDO usar en esta entrega:
1.  **Archivos Externos:** No usar lectura/escritura de archivos `.txt`, `.csv`, `.json`, ni bases de datos. Todos los datos (catálogos, ventas) deben vivir en memoria usando diccionarios y listas durante la ejecución.
2.  **Programación Orientada a Objetos (POO):** No usar Clases (`class`), objetos, ni herencia. Todo debe resolverse con funciones secuenciales.
3.  **Recursividad:** No usar funciones que se llamen a sí mismas. Usar iteraciones clásicas (`for`, `while`).
4.  **Librerías Externas Complejas:** No importar `pandas`, `numpy`, ni interfaces gráficas (`tkinter`). Todo es por consola.

---

## 📂 Estructura de Archivos del Proyecto
El proyecto está modularizado de la siguiente manera. Todas las sugerencias de código deben respetar dónde va cada responsabilidad:

* `main.py`: Punto de entrada principal. Contiene el menú interactivo (`while True`) y orquesta el llamado a los demás módulos.
* `info.py`: Función simple que imprime en consola los datos de bienvenida de la agencia.
* `busquedas.py`: Contiene el catálogo de viajes pre-cargado (Lista de diccionarios) y las funciones de búsqueda usando `filter()`.
* `micro.py`: Responsable de inicializar la matriz de asientos, imprimirla en formato cuadrícula y manejar la lógica de reservar un asiento (cambiar 'L' por 'O').
* `validaciones.py`: Contiene todas las funciones de validación de inputs del usuario utilizando `re.match()`.
* `finanzas.py`: Responsable de la lógica de negocio económica. Usa `map()` para aplicar porcentajes y `reduce()` para sumatorias.

## 🛠️ Directrices para Copilot:
1.  **Simplicidad:** Mantén el código legible para un estudiante de primer año de programación.
2.  **Comentarios:** Comenta el código explicando *qué* hace, especialmente cuando se usen RegEx o funciones funcionales complejas.
3.  **Manejo de Errores:** Evita sugerir bloques `try/except` excesivos a menos que sea estrictamente necesario (ej: casteos a `int`). Prioriza la validación por lógica (RegEx y condicionales).