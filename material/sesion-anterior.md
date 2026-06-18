# Sesión anterior

## Fecha
2026-06-17 (primera sesión de implementación; se partió de cero, todos los .py y .json estaban vacíos).

## Qué hicimos
Se implementó **el sistema completo, de la Capa 1 a la Capa 5**, siguiendo el plan
de la arquitectura (Sección 6.1) de abajo hacia arriba. Un módulo por vez, cada
uno verificado antes de seguir.

### Capa 1 · Lógica pura (con tests unitarios)
- `src/validaciones.py` — DNI/email/teléfono/fecha/hora (regex), `normalizar_texto`, `texto_no_vacio`.
- `src/finanzas.py` — `RECARGO_SERVICIO`, `aplicar_recargo`, `calcular_recaudacion` (reduce), `normalizar_precio`.
- `src/asientos.py` — grilla 5x4 (`construir_grilla`), `asiento_en_rango`, `asiento_esta_libre`, `contar_libres`, `dnis_del_viaje`.

### Capa 2 · Persistencia
- `src/persistencia.py` — `cargar` (FileNotFoundError→{}, JSONDecodeError→avisa y frena), `guardar`, `ruta_data`. Verificado a mano (round-trip, archivo inexistente, JSON corrupto).

### Capa 3 · Dominio (con tests unitarios)
- `src/logica_usuarios.py` — login, crear/desactivar/resetear, anti-admin-suicida, normalización simétrica del nombre.
- `src/logica_viajes.py` — alta/modificación/baja (soft-delete), `buscar_viajes` (motor único filter+lambda, enriquece con ocupacion/libres), destinos únicos, IDs.
- `src/logica_ventas.py` — `registrar_venta`, `dni_ya_en_viaje`, precios, `ventas_de_boletero`, `construir_ticket` (tupla inmutable), IDs.

### Capa 4 · Presentación
- `src/ui.py` — banners, menús, cartelera, mapa de asientos, ticket, resumen, reportes y todas las `pedir_X`. Verificado a ojo.
- Se agregó **conscientemente** `mostrar_historial_ventas` (no estaba en el contrato 4.8) porque "Mis Ventas" necesitaba presentar la lista.

### Capa 5 · Orquestación
- `src/main.py` — arranque, modo fábrica, login (3 intentos), ruteo por rol. Fuerza UTF-8 en consola. Import diferido de los menús.
- `src/menu_boletero.py` — flujo estrella **venta múltiple atómica** (carrito, doble anti-duplicados, map+reduce, una sola escritura), cartelera vendible, Mis Ventas.
- `src/menu_admin.py` — cartelera total, alta/modificación/baja de viajes, gestión de usuarios, reportes. Guardado transaccional tras cada mutación.

### Tests
- `src/tests/test_sistema.py` — 82 tests (TestValidaciones, TestFinanzas, TestAsientos, TestUsuarios, TestViajes, TestVentas). Todos en verde. Se corren con `python -m unittest discover -s tests` desde `src/`.

### Datos
- Se inicializaron los `data/*.json` (estaban en 0 bytes, lo que hacía crashear el loader).
- `data/usuarios.json` → estado de fábrica (admin/admin).
- `data/viajes.json` → semilla de 6 viajes curados (2 a bariloche, 2 a mendoza, 1 a mar del plata activo + 1 cancelado).
- `data/ventas.json` → `{}` (cero ventas semilla).

### Verificación
- Suite: 82 tests OK.
- Flujos clave probados con input simulado (venta múltiple con anti-dup/asiento ocupado/atomicidad, admin completo, login, modo fábrica).
- Corrida integral de `main()` punta a punta (guión de demo).
- Todos los módulos compilan e importan limpio.

### Otros
- Se creó `material/uso-del-sistema.md` (cómo ejecutar, modo fábrica, cómo restaurar a fábrica, mapa de menús, guion de demo).

## Notas / detalles conocidos
- El sistema **no** se ejecutó interactivamente en consola real (eso escribiría sobre los `.json`); queda como prueba manual pendiente del Paso 8.
- Detalle cosmético menor sin corregir: el total de "Mis Ventas" muestra "(1 ventas)" sin singular.
- Branch de trabajo: `cimientos`.
