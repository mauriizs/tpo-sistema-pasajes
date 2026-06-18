# 🚌 Nexus Viajes — Guía de uso del sistema

Notas prácticas para correr, probar y demostrar el sistema. (El diseño está en
`arquitectura-v3.md`; esto es el "cómo se usa".)

---

## ▶️ Cómo ejecutar

Desde una terminal, parado en la carpeta `src/`:

```
python main.py
```

No requiere instalar nada (solo librería estándar de Python). Funciona en
cualquier computadora porque las rutas a `data/` se arman relativas al script.

---

## 🧪 Cómo correr los tests

Desde la carpeta `src/`:

```
python -m unittest discover -s tests
```

Deberían pasar **82 tests** (Capa 1 + reglas del Dominio).

---

## 🏭 Primer arranque: modo fábrica (IMPORTANTE)

El sistema se entrega en **estado de fábrica**: `data/usuarios.json` contiene
únicamente un usuario `admin` con clave `admin`.

- La **primera vez** que corras `python main.py`, detecta ese estado y te lleva
  directo a **crear tu administrador real** (nombre + clave). Al confirmarlo,
  borra el `admin/admin` y guarda tu admin en `usuarios.json`.
- **Esto modifica el archivo de forma permanente.** Es el comportamiento correcto
  y esperado para la entrega, pero significa que el "estado de fábrica" se
  **consume** la primera vez que lo usás.

### 🔁 Restaurar el estado de fábrica (para volver a demostrarlo)

Si querés volver a mostrar el modo fábrica (p. ej. antes de la defensa), reemplazá
el contenido de `data/usuarios.json` por:

```json
{
    "admin": {
        "clave": "admin",
        "rol": "administrador",
        "estado": "activo"
    }
}
```

> Nota: si llegás a **borrar** `usuarios.json` por completo, el sistema se
> auto-repara: al no encontrar usuarios, vuelve solo a modo fábrica.

Para una demo "desde cero" también podés vaciar las ventas dejando
`data/ventas.json` en `{}` (y, si querés, restaurar la semilla de `viajes.json`).

---

## 🔑 Convenciones de uso

- **`0` = cancelar / volver.** En cualquier dato que se te pida, ingresar `0`
  cancela la operación y sube un nivel. En la venta múltiple, un `0` cancela
  **toda** la venta (no se registra nada).
- **Confirmación de venta:** solo se acepta `s`, `si` o `sí`. Cualquier otra cosa
  (incluido Enter vacío) **no** confirma → cancela la venta.
- **Opciones de menú:** se eligen tipeando el número (`1`, `2`, ...). Una opción
  inexistente vuelve a preguntar.

---

## 🗺️ Mapa de menús

```
MENÚ PRINCIPAL (ciego)
  [1] Iniciar sesión
  [2] Ayuda
  [3] Salir

MENÚ ADMINISTRADOR
  [1] Ver cartelera (vista total: activos, cancelados y llenos)
  [2] Alta de viaje
  [3] Modificar viaje (campo por campo; origen y destino NO se editan)
  [4] Baja de viaje (borra si no tiene ventas; cancela si tiene)
  [5] Gestión de usuarios (crear / desactivar / resetear clave)
  [6] Reporte: recaudación total
  [7] Reporte: destinos activos únicos
  [0] Cerrar sesión

MENÚ BOLETERO
  [1] Ver cartelera (vista vendible: solo activos con asientos libres)
  [2] Venta múltiple
  [3] Mis ventas (historial)
  [0] Cerrar sesión
```

---

## 🎬 Guion de demo sugerido

1. Arrancar → modo fábrica → crear admin real (ej: `gestor`).
2. Loguear como `gestor` → crear un boletero (ej: `vende1`).
3. Cerrar sesión → loguear como `vende1`.
4. Ver cartelera (vista vendible: el viaje cancelado **no** aparece).
5. Vender a una familia de 3-4 pasajeros (mostrar el anti-duplicados al repetir
   un DNI; mostrar la confirmación con lista blanca).
6. Ver "Mis Ventas".
7. Cerrar sesión → loguear como `gestor`.
8. Cartelera vista total (el viaje cancelado **sí** aparece).
9. Intentar dar de baja un viaje que ya tiene ventas → se **cancela** (no se borra).
10. Reportes: recaudación total + destinos únicos.
11. Intentar desactivar al único admin → **bloqueado** (anti-admin-suicida).

---

## 🌱 Datos semilla incluidos

- **usuarios.json** → solo `admin/admin` de fábrica.
- **viajes.json** → 6 viajes (2 a Bariloche, 2 a Mendoza, 1 a Mar del Plata
  activo y 1 cancelado). Sirven para demostrar búsqueda por destino, deduplicación
  de destinos únicos y el contraste cartelera admin vs. boletero.
- **ventas.json** → vacío `{}`. La recaudación arranca en $0 y cada venta que se
  registre tendrá un boletero real (la demo se hace vendiendo en vivo).

---

## 🐞 Si algo falla

- **"El archivo X está dañado o corrupto"** y el programa se detiene: alguno de
  los `.json` quedó mal formado (no es JSON válido). El sistema **no** lo
  sobrescribe a propósito, para no destruir datos. Revisá el archivo a mano o
  restauralo a un estado válido (`{}` como mínimo).
- **Tildes/ñ se ven raras en la consola:** el programa fuerza UTF-8 al arrancar;
  si igual se ven mal, es el codepage de la terminal de Windows.
