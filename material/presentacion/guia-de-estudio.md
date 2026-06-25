# Guía de estudio — Defensa oral TP2 "Nexus Viajes"

Archivo para estudiar nosotros antes del oral. No se entrega. Junta en un solo lugar
el **qué** (rápido) y sobre todo el **por qué** de cada decisión, que es lo que se
defiende. Al final hay un machete de preguntas probables con su respuesta.

> Regla de oro para el oral: **el profe no pregunta "¿qué hace?", pregunta "¿por qué
> así?".** Si entendés el porqué de cada decisión, estás cubierto.

---

## 1. El sistema en 5 frases

1. Es una **boletería de micros digitalizada**, por consola, en Python, que administra
   **usuarios, viajes y ventas**.
2. Hay **dos roles**: el **administrador** (gestiona viajes y usuarios, ve reportes) y
   el **boletero** (vende pasajes y ve su historial).
3. La información **se conserva entre ejecuciones** en archivos **JSON**.
4. La funcionalidad estrella es la **venta múltiple**: cargar varios pasajeros en un
   "carrito" y confirmar **todo o nada**.
5. Por dentro está organizado en **5 capas** donde las dependencias solo apuntan hacia
   abajo, lo que lo hace **testeable** (82 pruebas unitarias en verde).

---

## 2. Decisiones de diseño y su porqué (LO MÁS IMPORTANTE)

Esta sección es el corazón de la defensa. Cada decisión: qué es y por qué se tomó.

### 2.1 · Arquitectura en capas (la ley de dependencias)
- **Qué:** 5 capas. De arriba a abajo: Orquestación (main + menús) → Presentación
  (ui) → Dominio (reglas) → Persistencia (JSON) → Lógica pura (validar/calcular).
- **La ley:** las dependencias **solo apuntan hacia abajo**, nunca hacia arriba ni en
  círculo.
- **Los 3 mandamientos:**
  1. El dominio nunca hace `print()` ni `input()` (recibe datos, decide, devuelve).
  2. La presentación nunca aplica una regla de negocio (solo muestra y captura).
  3. Solo la orquestación conoce los dos mundos (I/O y reglas).
- **Por qué:** así la lógica se puede **testear** pasándole datos de juguete, sin
  consola ni archivos. En la Parte 1 todo vivía en `main()` y era imposible de probar.

### 2.2 · El dominio NO persiste
- **Qué:** guardar a disco lo hace la orquestación (Capa 5), no el dominio. Registrar
  una venta son **dos pasos**: 1) modificar el diccionario en memoria, 2) después
  guardar.
- **Por qué:** si el dominio guardara solo, cada test escribiría archivos reales y
  dejarían de ser unitarios. Separarlo es lo que hace posible testear.

### 2.3 · Una sola fuente de verdad (persistir vs. derivar)
- **Qué:** se guardan solo **usuarios, viajes y ventas**. La matriz de asientos, el
  conjunto de DNIs, los asientos libres y los destinos únicos **NO se guardan: se
  calculan** desde las ventas cuando se necesitan, y se descartan.
- **Principio:** todo lo que se puede calcular a partir de otra cosa, no se guarda.
- **Por qué:** un mismo hecho ("el DNI X compró el asiento 2-3") podía quedar escrito
  en 4 lugares (matriz, conjunto, ventas, contador). Cuatro copias = cuatro cosas que
  se **desincronizan**. Esa desincronización es el bug clásico que rompe los sistemas
  de reservas (la matriz dice "ocupado", el contador dice "libre"). Con un solo dueño
  del dato (las ventas), no puede pasar.
- **Cómo cumple la consigna:** "implementar una matriz" = usarla en memoria (se arma,
  se recorre, se muestra). "Los datos persisten" = lo que sobrevive son las ventas. La
  matriz se **proyecta** desde las ventas cada vez; nunca se lee de un archivo.

### 2.4 · Estado por parámetro, sin variables globales
- **Qué:** `main.py` carga los 3 diccionarios al arrancar y los pasa **por parámetro**
  a las funciones que los necesitan.
- **Por qué:** (1) testabilidad —una función que recibe sus datos se prueba con datos
  de juguete—, (2) una sola fuente de estado, (3) claridad: mirando la firma se sabe
  qué datos toca.

### 2.5 · Venta múltiple: atomicidad (todo o nada)
- **Qué:** durante la carga **no se registra ninguna venta ni se ocupa ningún asiento
  real**. Todo vive en estructuras temporales (carrito + matriz de trabajo). Recién al
  confirmar se crean las N ventas de una vez y se guarda una sola vez.
- **Por qué:** cancelar a mitad es **gratis** —se descarta el carrito y nada cambió—.
  No hace falta código de "deshacer": la atomicidad es **consecuencia** de no tocar
  nada real hasta confirmar. Si se corta la luz a mitad de carga, no pasa nada.

### 2.6 · Venta múltiple: doble conjunto anti-duplicados
- **Qué:** cada DNI nuevo se chequea contra **dos conjuntos**: el del **viaje** (DNIs
  que ya compraron antes, derivado de las ventas) y el de la **sesión** (DNIs cargados
  en esta misma compra).
- **Por qué hacen falta los dos:** sin el del viaje, alguien recompra el mismo viaje;
  sin el de la sesión, la familia mete dos veces el mismo DNI antes de confirmar
  (cuando todavía no hay ninguna venta registrada que lo detecte).

### 2.7 · Soft-delete en viajes (cancelar ≠ borrar)
- **Qué:** un viaje **sin** ventas se puede borrar; uno **con** ventas pasa a
  `"cancelado"` (no se borra).
- **Por qué:** una venta guarda el `id_viaje`, no una copia de los datos del viaje. Si
  se borrara un viaje con ventas, esas ventas quedarían **huérfanas** apuntando a algo
  inexistente (ticket sin viaje). Eso es **integridad referencial**.

### 2.8 · Soft-delete en usuarios + anti-admin-suicida
- **Qué:** los usuarios nunca se borran (estado `"inactivo"`). No se puede desactivar
  al **último admin activo**.
- **Por qué soft-delete:** un boletero borrado dejaría ventas con un `boletero`
  fantasma (misma integridad referencial que los viajes).
- **Por qué "último admin ACTIVO" y no total:** si hay dos admins pero uno está
  inactivo, desactivar al que queda dejaría el sistema sin nadie que lo administre.
- **Reset = reactivar:** resetear clave asigna clave nueva **y** reactiva. Cierra el
  callejón "lo desactivé sin querer y no hay vuelta" sin agregar otra opción de menú.

### 2.9 · Reglas de negocio vs. excepciones
- **Qué:** las reglas de negocio (DNI duplicado, asiento ocupado, último admin)
  **devuelven** una tupla `(exito, mensaje)`. Las excepciones se reservan para
  archivos (`FileNotFoundError`, `JSONDecodeError`) y conversión de tipos
  (`ValueError`).
- **Por qué:** un asiento ocupado **no es un error del programa**, es un resultado
  normal del negocio que pasa todos los días. Usar excepciones para control de flujo
  de negocio es un anti-patrón. Tampoco se envuelve todo en `try/except` "por las
  dudas": eso esconde bugs.

### 2.10 · Precio congelado en la venta
- **Qué:** cada venta guarda `precio_pagado`, el precio cobrado **en ese momento**.
- **Por qué (parece derivable pero NO lo es):** uno pensaría "es `precio_base × 1.16`,
  lo calculo del viaje". Error: el admin puede **cambiar** el precio del viaje después.
  Las ventas viejas deben seguir mostrando lo que el pasajero **realmente pagó** ese
  día. El precio actual y el precio histórico son dos hechos distintos.

### 2.11 · Normalizar ≠ validar
- **Qué:** primero se **normaliza** (preparar el dato: `strip`, `lower`, coma→punto),
  después se **valida** (juzgar el dato).
- **Por qué:** normalizar es generoso y barato (corregir el tipeo es amable); validar
  es estricto cuando equivocarse es caro. Ejemplo precio: `strip` → `replace(',','.')`
  → recién ahí `try: float()`. El `replace` va **antes** del `try` porque es
  preparación, no la operación que puede fallar.
- **La clave NO se normaliza:** aplicar `lower` a la contraseña haría que `"Abc"` y
  `"abc"` sean iguales, achicando el espacio de claves.

### 2.12 · Lista blanca en la confirmación de venta
- **Qué:** solo confirma si la respuesta está en `{"s", "si", "sí"}`. Cualquier otra
  cosa (Enter, "ok", "dale", "no") = no confirma = cancela.
- **Por qué no "empieza con S":** una heurística así aceptaría "salir" o "sacá esto"
  como confirmación, cobrándole a alguien que escribía otra cosa. Para algo
  irreversible con plata, el esfuerzo de validación es proporcional al costo del error.

### 2.13 · Claves en texto plano (decir la verdad)
- **Qué:** las contraseñas se guardan sin hashear.
- **Cómo defenderlo:** **honestamente**. "Sabemos que en producción se hashea; el
  hashing está fuera del alcance de la materia." No se esconde ni se llama "seguro".

### 2.14 · Guardado transaccional
- **Qué:** se guarda a disco **inmediatamente después de cada cambio** (alta de viaje,
  venta confirmada, desactivar usuario...), no en otro momento.
- **Por qué:** protege contra pérdida de datos si el programa se cierra de golpe.

### 2.15 · JSON corrupto → frenar, no vaciar
- **Qué:** si un `.json` está dañado (`JSONDecodeError`), se avisa y se **frena** sin
  tocar nada. Si **no existe** (`FileNotFoundError`), se devuelve `{}`.
- **Por qué la diferencia:** tratar un archivo corrupto como vacío lo
  **sobrescribiría**, destruyendo datos que quizás se recuperan a mano. Ante la duda,
  nunca destruir datos.

---

## 3. Los 6 conceptos del TP2 (qué, dónde, por qué)

| Concepto | Dónde se usa | Por qué ahí |
|----------|--------------|-------------|
| **Diccionarios** | usuarios, viajes, ventas (diccionarios de diccionarios, clave = ID) | Estructura principal; acceso directo por clave (el ID) |
| **Tuplas** | coordenada `(fila, columna)`, el ticket emitido, el resultado `(exito, mensaje)` | Inmutabilidad: el asiento es un par fijo, el pasaje no se modifica, el resultado no se altera |
| **Conjuntos** | doble anti-duplicados de DNI, destinos activos únicos, lista blanca `{"s","si","sí"}` | Unicidad automática y pertenencia inmediata (`in`) |
| **Excepciones** | archivos (`FileNotFoundError`, `JSONDecodeError`) y tipos (`ValueError`) | Solo para lo realmente excepcional; las reglas de negocio NO usan excepciones |
| **Archivos** | persistencia JSON (`cargar`/`guardar`), ruta relativa, guardado inmediato | Que los datos sobrevivan al cierre; portable sin rutas absolutas |
| **Pruebas unitarias** | `unittest`, 82 tests sobre Capa 1 y Capa 3 | Verifican lógica y reglas sin tocar disco; casos correctos y de error |

**Detalle extra de tuplas:** además de las tres, las reglas de negocio devuelven
`(exito, mensaje)` para que el flujo sepa qué mostrar sin usar excepciones.

**Detalle extra de funciones del TP2 en la venta múltiple:** `map` (proyecta el
carrito a la lista de precios), `reduce` (suma el total), `filter` + `lambda` (Mis
Ventas). El recargo del 16% lo aplica `aplicar_recargo` por pasaje.

---

## 4. Recorrido rápido del sistema (el "qué", para repasar)

- **Arranque:** carga los 3 JSON → si `usuarios` está vacío, inyecta admin/admin
  (**auto-reparación**) → si existe el admin de fábrica, entra en **modo fábrica**
  (crear admin real, una sola vez); si no, **modo normal**.
- **Login:** 3 intentos; valida usuario + clave + estado activo; rutea por rol.
- **Admin:** cartelera total · alta/modificación/baja de viajes · crear/desactivar/
  resetear usuarios · reportes (recaudación, destinos únicos).
- **Boletero:** cartelera vendible · venta múltiple · Mis Ventas.
- **Cerrar sesión (`0`):** vuelve al menú principal "ciego".
- **Convención `0`:** en cualquier input, `0` = cancelar y subir un nivel. Nunca
  avanza, siempre retrocede.

---

## 5. Machete de preguntas probables del profe

- **¿Por qué rehicieron la Parte 1 en vez de agregarle cosas?**
  Porque la consigna pide tests y el código viejo (todo en `main()`, validación
  mezclada con `input()`) era imposible de testear. Hubo que desacoplar en capas.

- **¿Por qué tantas capas para un TP?**
  Para poder testear la lógica aislada y para que un cambio en un lado no rompa el
  otro. Es lo que habilita las 82 pruebas.

- **¿Dónde guardan la matriz de asientos?**
  En ningún lado. Se calcula desde las ventas cuando se necesita. Es una decisión
  (una sola fuente de verdad), no un olvido.

- **¿Por qué no borran un viaje y listo?**
  Integridad referencial: las ventas guardan el `id_viaje`; borrarlo las dejaría
  huérfanas. Por eso soft-delete (pasa a "cancelado").

- **¿Por qué el precio se guarda y no se calcula?**
  Porque el admin puede cambiar el precio del viaje después; la venta debe mostrar lo
  que se pagó ese día. Precio actual ≠ precio histórico.

- **¿Por qué las reglas no usan excepciones?**
  Un asiento ocupado o un DNI repetido es un resultado normal del negocio, no un error
  del programa. Se devuelve `(exito, mensaje)`. Excepciones solo para archivos y tipos.

- **¿Es seguro guardar las claves en texto plano?**
  No, y lo sabemos. El hashing está fuera del alcance de la materia; lo declaramos a
  propósito, no lo escondemos.

- **¿Qué pasa si cancelo la venta a la mitad?**
  Nada: no se escribió nada real, se descarta el carrito y el sistema queda igual
  (atomicidad).

- **¿Por qué dos conjuntos de DNI y no uno?**
  Uno cubre "ya compró antes" (del viaje) y otro "lo repetí en esta misma compra"
  (de la sesión), cuando todavía no hay venta registrada que lo detecte.

- **¿Qué pasa la primera vez que se ejecuta, sin archivos?**
  `cargar` devuelve `{}`, se inyecta admin/admin y arranca en modo fábrica para crear
  el admin real.

- **¿Y si el archivo JSON está corrupto?**
  Se avisa y se frena sin tocar nada, para no sobrescribir datos recuperables. Distinto
  de "no existe", que sí devuelve `{}`.

- **¿Por qué no se puede desactivar a cualquier admin?**
  Porque no se puede dejar el sistema sin ningún admin activo. La cuenta es de admins
  **activos**, no totales.

- **¿Por qué `0` siempre cancela?**
  Convención transversal de UX: `0` nunca avanza, siempre retrocede un nivel.

---

## 6. Mini-glosario

- **Atomicidad:** una operación se hace **entera o nada**; no quedan estados a medias.
- **Integridad referencial:** que las referencias entre datos (una venta → su viaje)
  siempre apunten a algo que existe. Romperla = "registros huérfanos".
- **Soft-delete (baja lógica):** "borrar" marcando un estado (`cancelado`/`inactivo`)
  en vez de eliminar físicamente, para no romper referencias.
- **Derivar vs. persistir:** *persistir* = guardar en disco (la verdad: ventas).
  *Derivar* = calcular en memoria a partir de lo persistido (la matriz, los DNIs).
- **Fuente de verdad:** el único lugar donde vive un dato (acá, las ventas); todo lo
  demás se calcula de ahí.
- **Función pura:** recibe datos y devuelve datos; no imprime, no pide input, no toca
  archivos. Por eso es fácil de testear (Capa 1).
- **Normalizar:** preparar el dato (strip, lower, coma→punto). Distinto de **validar**
  (juzgar si el dato es correcto).
- **Lista blanca:** aceptar solo un conjunto explícito de valores válidos (acá,
  `{"s","si","sí"}` para confirmar).
- **Modo fábrica:** estado inicial del sistema (solo admin/admin) que guía a crear el
  primer admin real, una sola vez.
```
