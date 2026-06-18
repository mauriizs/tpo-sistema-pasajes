# Nexus Viajes — Sistema de Gestión y Venta de Pasajes de Micro

> Trabajo Práctico Obligatorio · **Algoritmos y Estructura de Datos I** · UADE

<br>

Sistema de gestión y venta de pasajes de micro por consola (CLI), desarrollado en
Python puro. Maneja usuarios con roles, catálogo de viajes, venta de pasajes con
selección de asientos y reportes, con persistencia en archivos JSON.

<br>

---

<br>

## ✨ Funcionalidades

<br>

- **Dos roles con menús propios:** administrador y boletero.

- **Gestión de viajes:** alta, modificación, baja (con borrado físico o cancelación
  lógica según tenga ventas o no).

- **Gestión de usuarios:** alta, desactivación y reseteo de clave, con protección
  anti-bloqueo (no se puede desactivar al último administrador activo).

- **Venta múltiple atómica:** se cargan varios pasajeros en una sola operación
  tipo "carrito"; nada se registra hasta confirmar (cancelar no deja rastros).

- **Mapa de asientos** 5x4 derivado en tiempo real de las ventas.

- **Anti-duplicados de DNI** por viaje y dentro de la misma compra.

- **Reportes:** recaudación total y destinos activos únicos.

- **Persistencia** automática en archivos JSON tras cada operación.

<br>

---

<br>

## 🛠️ Requisitos

<br>

- **Python 3.10 o superior** (se usan type hints con la sintaxis `X | None`).

- **Sin librerías externas:** usa únicamente la biblioteca estándar de Python.

- Funciona en cualquier sistema operativo (rutas relativas, sin configuración).

<br>

---

<br>

## ▶️ Cómo ejecutar

<br>

Desde la carpeta del proyecto:

```bash
cd src
python main.py
```

<br>

### Primer arranque (modo fábrica)

<br>

La primera vez, el sistema arranca en **modo fábrica**: detecta que no hay un
administrador real y te guía para crear el primero (usuario y clave). Una vez
creado, el sistema pasa al funcionamiento normal y ya no vuelve a pedirlo.

> El estado de fábrica se reconoce porque existe el usuario `admin` con clave
> `admin`. Para volver a fábrica, basta con restaurar los archivos de `data/`.

<br>

### Menús según el rol

<br>

| Administrador | Boletero |
|---------------|----------|
| Ver cartelera (vista total) | Ver cartelera (solo viajes vendibles) |
| Alta / modificación / baja de viajes | Venta múltiple |
| Gestión de usuarios | Mis ventas (historial) |
| Reportes (recaudación y destinos) | |

<br>

En cualquier dato que se pida, ingresar `0` cancela y vuelve al nivel anterior.

<br>

---

<br>

## 🧪 Tests

<br>

El proyecto incluye una suite de pruebas unitarias con `unittest` (biblioteca
estándar). Se ejecuta desde la carpeta `src`:

```bash
cd src
python -m unittest discover -s tests
```

<br>

---

<br>

## 📁 Estructura del proyecto

<br>

```
tpo-sistema-pasajes/
├── data/                     # Persistencia (archivos JSON)
│   ├── usuarios.json
│   ├── viajes.json
│   └── ventas.json           # Fuente de verdad de las ventas
├── src/
│   ├── main.py               # Punto de entrada y arranque
│   ├── menu_admin.py         # Menú del administrador
│   ├── menu_boletero.py      # Menú del boletero (venta múltiple)
│   ├── ui.py                 # Presentación: menús, tablas, input
│   ├── logica_usuarios.py    # Reglas de negocio de usuarios
│   ├── logica_viajes.py      # Reglas de negocio de viajes
│   ├── logica_ventas.py      # Reglas de negocio de ventas
│   ├── persistencia.py       # Lectura/escritura de los JSON
│   ├── validaciones.py       # Validaciones de formato (regex)
│   ├── finanzas.py           # Cálculos de dinero
│   ├── asientos.py           # Grilla de asientos (matriz)
│   └── tests/
│       └── test_sistema.py   # Pruebas unitarias
└── README.md
```

<br>

El sistema está organizado en **capas**, donde cada una solo depende de las
inferiores: lógica pura → persistencia → dominio → presentación → orquestación.
Esto mantiene la lógica de negocio testeable y aislada de la entrada/salida.

<br>

---

<br>

## 📌 Dónde se usa cada concepto del TP2

<br>

| Concepto | Dónde se implementa |
|----------|---------------------|
| **Diccionarios** | Estructuras principales: `usuarios`, `viajes`, `ventas` (diccionarios de diccionarios con el ID como clave) |
| **Tuplas** | Coordenada de asiento `(fila, columna)`; ticket emitido inmutable |
| **Conjuntos** | Anti-duplicados de DNI en la venta (conjunto del viaje + de la sesión); destinos activos únicos |
| **Excepciones** | Carga de archivos (`FileNotFoundError`, `JSONDecodeError`); conversión de tipos en `pedir_precio` / `pedir_entero` |
| **Archivos** | Persistencia en JSON de las tres estructuras (`data/`) |
| **Pruebas unitarias** | `unittest` sobre lógica pura y reglas de dominio (`src/tests/test_sistema.py`) |
| **Listas / matriz** | Mapa de asientos: grilla 5x4 derivada de las ventas |
| **lambda / map / filter / reduce** | `buscar_viajes` y `ventas_de_boletero` (filter + lambda); `map` en la venta múltiple; `calcular_recaudacion` (reduce) |
| **Expresiones regulares** | Validación de formato (DNI, email, teléfono, fecha, hora) en `validaciones.py` |

<br>

---

<br>

## 👥 Integrantes y Roles

<br>

| Integrante | Legajo | Rol |
|------------|--------|-----|
| Farfan, Mauricio | 1167832 | Líder del Proyecto |
| Velasquez, Lorena | 1146019 | Desarrolladora |
| Astudillo, Valentina | 1211931 | Analista |
| Chaina, Brian | 1213338 | Tester |
| Ayala, Alan | 1196870 | Diseñador de UI/UX |

<br>

_Grupo — Algoritmos y Estructura de Datos I, UADE._
