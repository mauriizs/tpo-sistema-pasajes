# Trabajo Práctico Obligatorio — 2da Parte

## Sistema de Gestión y Venta de Pasajes de Micro — "Nexus Viajes"

**Materia:** Algoritmos y Estructura de Datos I — UADE

**Grupo:** 9

**Integrantes:**

| Integrante | Legajo | Rol |
|------------|--------|-----|
| Farfan, Mauricio | 1167832 | Líder del Proyecto |
| Velasquez, Lorena | 1146019 | Desarrolladora |
| Astudillo, Valentina | 1211931 | Analista |
| Chaina, Brian | 1213338 | Tester |
| Ayala, Alan | 1196870 | Diseñador de UI/UX |

**Fecha:** 19 de junio de 2026.

---

## Índice

1. Introducción
2. Requisitos y ejecución
3. Descripción general del sistema
4. Estructura del proyecto
5. Uso de los conceptos del TP2
   - 5.1 Diccionarios
   - 5.2 Tuplas
   - 5.3 Conjuntos
   - 5.4 Excepciones
   - 5.5 Archivos
   - 5.6 Pruebas unitarias
6. Conclusión

---

## 1. Introducción

El presente trabajo implementa un sistema de gestión y venta de pasajes de micro
por consola, desarrollado en Python. El sistema permite administrar usuarios con
distintos roles, gestionar un catálogo de viajes, vender pasajes con selección de
asientos y generar reportes, manteniendo la información de forma persistente en
archivos.

El sistema está pensado para ser usado por dos tipos de empleados: el
**administrador**, que gestiona los viajes, los usuarios y consulta reportes; y el
**boletero**, encargado de vender los pasajes. Toda la información (usuarios,
viajes y ventas) se conserva entre ejecuciones gracias a la persistencia en
archivos JSON.

---

## 2. Requisitos y ejecución

- **Python 3.10 o superior.**
- No requiere librerías externas: utiliza únicamente la biblioteca estándar.
- Funciona en cualquier sistema operativo (las rutas a los datos se construyen de
  forma relativa, sin rutas absolutas).

Para ejecutarlo, desde la carpeta `src`:

```
python main.py
```

La primera vez, el sistema arranca en **modo fábrica**: detecta que todavía no hay
un administrador real y guía al usuario para crear el primero. A partir de ahí,
funciona normalmente solicitando inicio de sesión.

Para ejecutar las pruebas unitarias, desde la carpeta `src`:

```
python -m unittest discover -s tests
```

---

## 3. Descripción general del sistema

El sistema se maneja a través de menús por consola. Tras iniciar sesión, cada
usuario accede al menú correspondiente a su rol:

**Administrador:**

- Consultar la cartelera de viajes (vista total: incluye activos y cancelados).
- Alta, modificación y baja de viajes.
- Gestión de usuarios (crear, desactivar, resetear clave).
- Reportes: recaudación total y destinos activos únicos.

**Boletero:**

- Consultar la cartelera (vista vendible: solo viajes activos con asientos libres).
- Venta múltiple de pasajes (varios pasajeros en una sola operación).
- Consultar su historial de ventas.

Una característica central es la **venta múltiple atómica**: el boletero carga
varios pasajeros en una especie de "carrito" y nada se registra hasta confirmar la
operación completa. Si se cancela en el medio, no queda ningún dato a medio
escribir. Durante la carga, el sistema muestra el mapa de asientos y evita que se
repita un asiento o un DNI dentro de la misma compra.

---

## 4. Estructura del proyecto

El proyecto está organizado de la siguiente manera:

```
tpo-sistema-pasajes/
├── data/                  Archivos de datos persistentes (JSON)
│   ├── usuarios.json
│   ├── viajes.json
│   └── ventas.json
└── src/                   Código fuente
    ├── main.py            Punto de entrada del sistema
    ├── menu_admin.py      Menú del administrador
    ├── menu_boletero.py   Menú del boletero
    ├── ui.py              Presentación (menús, tablas, captura de datos)
    ├── logica_usuarios.py Reglas de negocio de usuarios
    ├── logica_viajes.py   Reglas de negocio de viajes
    ├── logica_ventas.py   Reglas de negocio de ventas
    ├── persistencia.py    Lectura y escritura de los archivos JSON
    ├── validaciones.py    Validaciones de formato
    ├── finanzas.py        Cálculos de dinero
    ├── asientos.py        Grilla de asientos
    └── tests/
        └── test_sistema.py  Pruebas unitarias
```

El código está separado en **capas**: las funciones de cálculo y validación no
dependen de nada, la lógica de negocio opera sobre los datos sin imprimir ni pedir
información, la presentación se encarga de la interacción con el usuario, y un nivel
de orquestación conecta todo. Esta separación facilita probar la lógica de forma
aislada.

---

## 5. Uso de los conceptos del TP2

### 5.1 Diccionarios

Los diccionarios son la estructura principal de todo el sistema. Las tres entidades
se modelan como **diccionarios de diccionarios**, donde la clave externa es el
identificador del elemento:

- **`usuarios`** — la clave es el nombre de usuario, y el valor es un diccionario
  con `clave`, `rol` y `estado`.
- **`viajes`** — la clave es el ID del viaje (por ejemplo `"V001"`), y el valor
  contiene `empresa`, `origen`, `destino`, `fecha`, `hora`, `precio_base` y `estado`.
- **`ventas`** — la clave es el ID de la venta (por ejemplo `"T0001"`), y el valor
  guarda `id_viaje`, `dni`, `email`, `telefono`, `fila`, `columna`,
  `precio_pagado` y `boletero`.

Estos diccionarios se cargan al inicio y se pasan como parámetro a las funciones
que los necesitan. Se utilizan en todos los módulos de lógica
(`logica_usuarios.py`, `logica_viajes.py`, `logica_ventas.py`) para buscar, crear,
modificar y eliminar elementos.

### 5.2 Tuplas

Se utilizan tuplas en dos lugares principales:

- **Coordenada de asiento `(fila, columna)`:** representa la posición de un asiento
  como un par inmutable que circula por todo el flujo de venta
  (`menu_boletero.py`).
- **Ticket emitido:** al confirmar una venta, el comprobante se arma como una tupla
  inmutable en la función `construir_ticket` (`logica_ventas.py`), con el formato
  `(id_venta, id_viaje, empresa, origen, destino, fecha, hora, dni, fila, columna,
  precio_pagado)`. Su inmutabilidad representa que un pasaje, una vez emitido, no se
  modifica.

Además, las funciones de lógica que pueden fallar por una regla de negocio
devuelven una tupla `(exito, mensaje)`, que el resto del programa interpreta para
mostrar el resultado.

### 5.3 Conjuntos

Los conjuntos (`set`) se usan donde se necesita unicidad o pertenencia rápida:

- **Anti-duplicados de DNI en la venta múltiple** (`menu_boletero.py`): se manejan
  dos conjuntos. Uno con los DNIs que ya compraron ese viaje en ventas anteriores
  (derivado con `dnis_del_viaje` en `asientos.py`) y otro con los DNIs cargados en
  la compra actual. Cada DNI nuevo se verifica contra ambos para que nadie compre
  dos veces ni se repita dentro de la misma operación.
- **Destinos activos únicos** (`destinos_activos_unicos` en `logica_viajes.py`): se
  arma un conjunto con los destinos de los viajes activos, lo que elimina
  automáticamente los repetidos para el reporte.
- **Validación de confirmación** (`pedir_confirmacion` en `ui.py`): la respuesta se
  compara contra el conjunto `{"s", "si", "sí"}` para aceptar la venta solo ante un
  "sí" inequívoco.

### 5.4 Excepciones

Las excepciones se usan exactamente donde corresponde: situaciones que escapan al
control normal del programa.

- **Manejo de archivos** (`persistencia.py`): al cargar un archivo se usa
  `try/except` para capturar `FileNotFoundError` (si el archivo no existe todavía,
  se devuelve un diccionario vacío) y `JSONDecodeError` (si el archivo está
  corrupto, se avisa y se detiene el programa para no destruir datos).
- **Conversión de tipos** (`ui.py`): al pedir un precio o un número entero, se usa
  `try/except ValueError` para detectar cuando el usuario escribe algo que no es un
  número y volver a preguntar.

Las reglas de negocio (DNI duplicado, asiento ocupado, etc.) **no** se manejan con
excepciones, sino devolviendo un resultado, ya que son situaciones normales del
funcionamiento del sistema y no errores.

### 5.5 Archivos

La persistencia se resuelve con archivos **JSON**, manejados en el módulo
`persistencia.py`:

- La función `cargar` lee un archivo JSON y devuelve su contenido como diccionario.
- La función `guardar` escribe el diccionario completo en el archivo
  correspondiente.

Las tres estructuras se guardan en `data/usuarios.json`, `data/viajes.json` y
`data/ventas.json`. La ruta a la carpeta `data/` se construye de forma relativa a
la ubicación del script, para que el sistema funcione en cualquier computadora sin
depender de rutas absolutas.

El guardado es **transaccional**: el archivo se actualiza inmediatamente después de
cada operación que modifica los datos (crear un viaje, registrar una venta,
desactivar un usuario, etc.), de modo que la información no se pierde si el programa
se cierra.

### 5.6 Pruebas unitarias

Las pruebas unitarias se implementaron con **`unittest`**, el módulo de pruebas de
la biblioteca estándar de Python, en el archivo `src/tests/test_sistema.py`.

Se probaron las funciones de cálculo y validación, y las reglas de negocio del
dominio (usuarios, viajes y ventas). Cada prueba arma sus propios datos de ejemplo
y no lee los archivos reales, por lo que las pruebas son independientes entre sí y
no modifican el estado del sistema. Se verifican tanto los casos correctos como los
casos de error (por ejemplo, que un DNI inválido sea rechazado o que no se pueda
desactivar al último administrador).

La suite cuenta con **82 pruebas**, todas exitosas. Se ejecutan con el comando
`python -m unittest discover -s tests` desde la carpeta `src`.

---

## 6. Conclusión

El sistema cumple con los requisitos planteados, integrando diccionarios, tuplas,
conjuntos, excepciones, archivos y pruebas unitarias de forma coherente con el
funcionamiento del negocio. La organización en capas y el manejo de los datos en
una única fuente de verdad permitieron construir un sistema ordenado, fácil de
probar y de mantener. El resultado es una aplicación de consola funcional, portable
y con la información persistida de forma segura entre ejecuciones.
