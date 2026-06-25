# 🚌 Nexus Viajes — Contenido y Estructura del Sistema (TP2)

> Qué **contiene** el sistema y **cómo está armado**: alcance, estructuras de datos, y dónde vive cada exigencia del TP2. Versión alineada al diseño definitivo y a la pauta de la cátedra.

---

# 🎯 Alcance

Sistema de **venta y gestión de pasajes de micro**, por **consola**, con dos roles. Todo en español, sin base de datos, sin interfaz gráfica, sin librerías externas no vistas en clase.

**Entra en el alcance:** login con ruteo por rol, alta/modificación/baja de viajes, gestión de usuarios, venta múltiple de pasajes, reportes (recaudación y destinos activos), persistencia en archivos y pruebas unitarias.

**Queda afuera (a propósito):** devoluciones de pasajes, hashing de claves, fechas futuras/años bisiestos, y cualquier cosa que requiera calendario o seguridad real. Se declara honestamente en la defensa.

---

# 🚌 El micro (constante del sistema)

Todos los micros son iguales: **5 filas × 4 columnas = 20 asientos**. No es un dato por viaje, es una **constante definida una sola vez en el código** (`FILAS = 5`, `COLUMNAS = 4`).

El asiento se modela como una coordenada en **base 1** (la fila 1 es la primera, no la 0), porque así piensa el usuario. La matriz interna se indexa restando 1.

---

# 🏗️ Cómo está construido (capas)

El sistema está dividido en capas; **cada capa solo puede depender de las de abajo**, nunca al revés. Eso es lo que lo hace testeable y mantenible.

```
CAPA 5 · Orquestación   → main + menús. Cablea todo. Pide, decide, guarda.
CAPA 4 · Presentación   → ui. Lo que el usuario ve y teclea. No decide reglas.
CAPA 3 · Dominio        → reglas del negocio. Decide, no imprime ni pide input.
CAPA 2 · Persistencia   → leer/escribir archivos. No sabe de reglas.
CAPA 1 · Lógica pura    → funciones puras (validar, calcular, armar grilla). No depende de nadie.
```

> Regla de oro: el **Dominio nunca persiste** ni imprime; la **Presentación nunca decide** una regla; el único que conoce ambos mundos es la **Orquestación**. Así el dominio se testea pasándole diccionarios de juguete, sin tocar disco.

---

# 🗄️ Diccionarios (la información principal)

Las tres estructuras centrales son **diccionarios de diccionarios**, con el ID como clave externa.

**Usuarios** — clave: el nombre de usuario (normalizado a minúsculas).

```python
usuarios = {
    "mauri_admin": { "clave": "1234", "rol": "administrador", "estado": "activo" },
    "boletero1":   { "clave": "abcd", "rol": "boletero",      "estado": "activo" }
}
```

**Viajes** — clave: el ID del viaje (`"V001"`).

```python
viajes = {
    "V001": {
        "empresa": "Via Bariloche",
        "origen": "Buenos Aires",
        "destino": "bariloche",      # se guarda normalizado (strip+lower)
        "fecha": "20/05/2026",
        "hora": "14:30",
        "precio_base": 50000.0,
        "estado": "activo"           # "activo" | "cancelado"
    }
}
```

**Ventas** — clave: el ID de venta (`"T0001"`). Es **la fuente de verdad** del sistema.

```python
ventas = {
    "T0001": {
        "id_viaje": "V001",
        "dni": "38123456",
        "email": "pepe@mail.com",
        "telefono": "1145678901",
        "fila": 2,
        "columna": 3,
        "precio_pagado": 58000.0,    # congelado: lo que se pagó ese día
        "boletero": "boletero1"
    }
}
```

> **Lo que NO se guarda porque se calcula:** el mapa de asientos, los asientos libres, los DNIs que ya compraron y los destinos únicos. Todo eso se **deriva de las ventas** en el momento que se necesita y se descarta. Una sola fuente de verdad, sin copias que se desincronicen.

---

# 🧩 Tuplas (información inmutable)

Dos usos genuinos, ambos donde la inmutabilidad tiene sentido real:

1. **Coordenada de asiento `(fila, columna)`** — el par que circula por todo el flujo de selección y verificación de asientos.

2. **El ticket emitido** — una tupla que se arma al confirmar la venta, se usa para imprimir el comprobante y **no se guarda** (el registro real ya vive en `ventas`). Un pasaje, una vez emitido, no se toca más:

```python
ticket = ("T0001", "V001", "Via Bariloche", "Buenos Aires", "bariloche",
          "20/05/2026", "14:30", "38123456", 2, 3, 58000.0)
#         id_venta  id_viaje  empresa        origen          destino
#         fecha        hora     dni        fila col  precio_pagado
```

---

# 🗂️ Conjuntos (sets)

Los sets son la **estrella del TP2** y aparecen en tres lugares, siempre para garantizar unicidad o evitar repetidos:

1. **Anti-duplicados en la venta (doble conjunto).** Ningún DNI puede comprar dos veces el mismo viaje. Se chequea contra dos sets a la vez:
   - **Conjunto del viaje** → DNIs que ya compraron antes (derivado de las ventas).
   - **Conjunto de sesión** → DNIs cargados en la venta en curso, todavía sin confirmar.

2. **Destinos activos únicos** → reporte del admin: `set` de los destinos de viajes activos, que deduplica solo (`{"bariloche", "cordoba", ...}`).

3. **Lista blanca de confirmación** → `{"s", "si", "sí"}`: la única forma de aceptar una venta (operación irreversible con plata).

> Ojo en la defensa: las **opciones de menú NO usan set**. Se comparan como string directo (`if opcion == "1"`), así una opción inexistente simplemente cae en "opción inválida → re-preguntar", sin conversión que pueda fallar.

---

# ⚡ Excepciones

La regla de oro: las excepciones son para lo **excepcional**, no para el control de flujo del negocio. Por eso hay una línea clara entre tres cosas:

| Situación | Cómo se trata | Dónde |
|-----------|---------------|-------|
| Letras donde va un número (precio, fila, cantidad) | `try/except ValueError` | `pedir_X` en la presentación |
| Archivo inexistente | `try/except FileNotFoundError` → arranca vacío `{}` | persistencia |
| Archivo corrupto | `try/except JSONDecodeError` → avisa y frena (no destruye datos) | persistencia |
| DNI repetido, asiento ocupado, valor negativo, dato vacío | **regla de negocio**: se valida y se devuelve un resultado, NO se lanza excepción | dominio / validaciones |

> Las validaciones obligatorias de la pauta se cubren así: *letras en numéricos* → excepción de conversión; *negativos y vacíos* → reglas (`precio > 0`, texto no vacío); *códigos repetidos* → sets; *archivos inexistentes* → excepción de archivo.

---

# 📂 Archivos (persistencia)

Lo que tiene que sobrevivir al cierre se guarda en **tres archivos `.json`** dentro de `data/`, con contenido en formato JSON (texto plano legible):

```
data/usuarios.json   → {"mauri_admin": {...}, "boletero1": {...}}
data/viajes.json     → {"V001": {...}, "V002": {...}}
data/ventas.json     → {"T0001": {...}}     ← la fuente de verdad
```

**Cómo funciona el flujo disco ↔ memoria:**

```
ARRANQUE     → se cargan los tres archivos a memoria (si falta uno → {} vacío).
DURANTE      → las estructuras viven en memoria y se modifican normalmente.
GUARDADO     → transaccional: después de CADA mutación (alta/baja/venta/usuario)
               se sobrescribe el archivo entero al instante.
```

El guardado transaccional protege contra pérdida de datos: si el programa se cierra de golpe, lo último confirmado ya está en disco. La ruta se arma **relativa a la ubicación del script** (nunca absoluta), para que corra en cualquier computadora.

> Como ningún `set` se guarda (se derivan en memoria), los archivos solo contienen tipos que el texto entiende de fábrica: nada de convertir sets a listas para serializar.

---

# 🧪 Pruebas unitarias

Se usa **`unittest`** (estándar de Python, cero dependencias). Se corre desde la terminal con `python -m unittest`, no desde el menú.

Se testea lo que **se puede testear sin simular un usuario**: la **Capa 1** (validadores, cálculos, armado de grilla) y las **reglas del Dominio** (alta de usuario, anti-admin-suicida, IDs, búsquedas). Cada test arma sus propios datos de juguete; no leen los archivos reales. Para cada validador se prueba lo que **acepta** y lo que **rechaza**.

---

# 🔁 Cómo se usa (menú)

Hay una sola puerta de entrada: un **menú principal "ciego"** que no muestra nada del negocio hasta saber quién sos. El login rutea automático según el rol.

```bash
╔════════════════════════════════════════════╗
║          SISTEMA CENTRAL DE VIAJES          ║
║                 NEXUS · 2026                ║
╠════════════════════════════════════════════╣
║   [1] Iniciar sesión                        ║
║   [2] Ayuda                                 ║
║   [3] Salir                                 ║
╚════════════════════════════════════════════╝

> Seleccione una opción:
```

- **Login** → pide usuario y clave; valida que exista, coincida y esté activo. Al 3.er fallo vuelve al menú principal (no cierra el programa).
- **Ruteo** → administrador va a su menú; boletero al suyo.
- **Convención del `'0'`** → en cualquier input, `0` cancela y sube un nivel. Nunca avanza, siempre retrocede.

**Menú administrador:** cartelera (vista total) · alta/modificación/baja de viajes · gestión de usuarios (crear / desactivar / resetear clave) · reportes (recaudación total, destinos únicos).

**Menú boletero:** cartelera (vista vendible: solo activos con lugar) · venta múltiple · mis ventas (historial propio).

---

# 🗺️ Dónde vive cada exigencia del TP2

| Exigencia | Dónde se usa en el sistema |
|-----------|----------------------------|
| **Diccionarios** | Las tres estructuras centrales: `usuarios`, `viajes`, `ventas` (diccionarios de diccionarios). |
| **Tuplas** | Coordenada de asiento `(fila, columna)` y el ticket emitido inmutable. |
| **Conjuntos** | Doble anti-duplicados de DNI en la venta; destinos activos únicos; lista blanca de confirmación. |
| **Excepciones** | Conversión de tipos en los `pedir_X`; carga de archivos (`FileNotFoundError`, `JSONDecodeError`). |
| **Archivos** | Persistencia de las tres estructuras en `data/*.json`, con guardado transaccional. |
| **Pruebas unitarias** | `unittest` sobre la Capa 1 y las reglas del Dominio. |
| **Git / branches** | Una branch por módulo, merges chicos a `develop`, repo en GitHub. |

---

*Este documento describe el contenido y la estructura del sistema. El detalle de cada decisión y las firmas de funciones viven en el Documento de Arquitectura.*
