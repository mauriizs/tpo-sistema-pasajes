# Indicaciones para el PowerPoint

Contenido slide por slide para la presentación oral del TP2.

> **IMPORTANTE — para qué sirve este PowerPoint.** No es un apoyo visual minimalista
> para que lo lea el público. Es **nuestro guion de defensa**: lo vemos nosotros en
> nuestras laptops mientras exponemos. La presentación es oral; el profe nos escucha
> y nos para cuando quiera ("¿quedó claro? ¿dudas?"). Por eso el power tiene que ser
> **denso y completo**, para poder desarrollar cada tema lo máximo posible y defender
> el sistema hasta donde nos frenen. **No buscamos que sea breve.**

Cada slide tiene dos partes:

- **En pantalla:** lo estructurado que se ve en la diapositiva. Sirve de ancla
  visual para saber de qué estamos hablando y tener los términos a la vista. Puede
  tener más contenido que una presentación normal — es nuestro apoyo.
- **Notas del orador (guion):** bullets con las ideas clave, **el porqué de cada
  decisión** (que es lo que hay que poder defender) y **posibles preguntas del profe
  con su respuesta**. Es lo que miramos para hablar. No está redactado como libreto
  textual: son disparadores para desarrollar con nuestras palabras.

Los slides están agrupados en bloques temáticos. El reparto entre integrantes queda
para después (sin nombres por slide).

---

## BLOQUE 0 · Apertura

---

## Slide 1 — Carátula

**En pantalla:**
- Sistema de Gestión y Venta de Pasajes de Micro — "Nexus Viajes"
- Algoritmos y Estructura de Datos I — UADE
- Grupo 9
- Integrantes: Farfan, Mauricio · Velasquez, Lorena · Astudillo, Valentina ·
  Chaina, Brian · Ayala, Alan
- Fecha: 19 de junio de 2026

**Notas (guion):**
- Mismo encabezado que la documentación escrita (consistencia).
- Presentarnos y decir en una frase qué es: "una boletería de micros digitalizada,
  por consola, en Python".

---

## Slide 2 — Agenda de la exposición

**En pantalla:**
- 1. Qué es el sistema y para quién (visión general)
- 2. Recorrido funcional (arranque, roles, viajes, usuarios, venta, reportes)
- 3. La funcionalidad estrella: la venta múltiple
- 4. Cómo está construido por dentro (arquitectura en capas + modelo de datos)
- 5. Los 6 conceptos del TP2 y dónde se usan
- 6. Decisiones de diseño defendibles + casos borde
- 7. Pruebas unitarias y demo en vivo

**Notas (guion):**
- Sirve para ordenar la exposición y que el profe sepa que está todo cubierto.
- Aclarar que vamos de lo general (qué hace) a lo técnico (cómo y por qué).

---

## Slide 3 — El problema y el contexto

**En pantalla:**
- Parte 1 (ya aprobada): venta de pasajes por consola, en memoria, sin roles ni
  persistencia. Todo dentro de `main()`.
- Parte 2 (este TP): rediseño completo del sistema.
- La consigna obliga a incorporar: diccionarios, tuplas, conjuntos, excepciones,
  archivos, pruebas unitarias y Git/branches.
- Restricciones de la cátedra: sin bases de datos, sin interfaces gráficas, sin
  librerías externas. Todo CLI y portable.

**Notas (guion):**
- El problema de la Parte 1: toda la lógica vivía en `main()` y la validación se
  mezclaba con el `input()` → era **imposible de testear** sin simular a alguien
  tecleando, y cualquier cambio era riesgoso porque todo estaba acoplado.
- La Parte 2 no es "agregarle cosas" a la Parte 1: es un **rediseño** que parte de
  separar el sistema en capas para que sea testeable y mantenible.
- *Posible pregunta:* "¿por qué rehicieron todo?" → porque la consigna pide tests, y
  el código viejo no se podía testear sin desacoplar la lógica del input/print.

---

## BLOQUE 1 · Qué hace el sistema (recorrido funcional)

---

## Slide 4 — Visión general

**En pantalla:**
- Sistema de venta de pasajes de micro, por consola, en Python.
- Administra tres entidades: **usuarios**, **viajes** y **ventas**.
- La información se conserva entre ejecuciones (archivos JSON).
- Corre en cualquier computadora: solo biblioteca estándar, sin rutas absolutas.
- Micro fijo de 5 × 4 = 20 asientos (constante del sistema).

**Notas (guion):**
- En una frase: una boletería de micros digitalizada.
- Dos tipos de empleado: administrador (gestiona) y boletero (vende).
- "Se conserva entre ejecuciones" = si cierro el programa y lo vuelvo a abrir, los
  datos siguen ahí (eso es la persistencia, lo vemos en detalle después).
- El micro es siempre 5×4 porque todos los micros son iguales: la dimensión es una
  constante del código, no un dato que se guarde por viaje.

---

## Slide 5 — Dos roles, dos menús

**En pantalla:**
- **Administrador:** gestiona viajes (alta / modificación / baja), gestiona usuarios
  (crear / desactivar / resetear clave) y consulta reportes (recaudación, destinos
  únicos). Ve la cartelera **completa** (activos y cancelados).
- **Boletero:** consulta la cartelera **vendible** (solo activos con asientos
  libres), vende pasajes (venta múltiple) y revisa su propio historial.
- Cada uno, al iniciar sesión, ve solo el menú de su rol.

**Notas (guion):**
- El sistema separa responsabilidades por rol: el boletero solo vende, no administra.
- La cartelera es **una sola lógica con un parámetro de visibilidad**, no dos
  funciones distintas. El admin la ve en "vista total"; al boletero se le oculta lo
  que no puede vender (cancelados/llenos) para que no se equivoque.
- *Posible pregunta:* "¿el boletero puede ver los reportes?" → no, solo el admin.

---

## Slide 6 — Recorrido de arranque

**En pantalla:**
```
ARRANQUE
  1. Cargar usuarios / viajes / ventas desde data/   (si falta → {})
  2. ¿usuarios quedó vacío? → inyectar admin/admin    (auto-reparación)
  3. ¿existe admin/admin de fábrica?
        SÍ → MODO FÁBRICA (crear el admin real, una sola vez)
        NO → MODO NORMAL (menú principal → login)
```
- Modo normal: [1] Iniciar sesión · [2] Ayuda · [3] Salir
- Login: 3 intentos, valida usuario + clave + estado activo, y rutea por rol.

**Notas (guion):**
- **Modo fábrica:** la primera vez que se usa, no hay admin real. El sistema lo
  detecta y guía para crear el primer administrador. Pasa directo a crearlo (no pide
  loguearse con admin/admin, sería fricción sin función) y después borra admin/admin.
- **Auto-reparación:** si alguien borra `usuarios.json`, el sistema vuelve solo a
  modo fábrica en vez de quedar muerto.
- **Login:** al 3er intento fallido vuelve al menú principal (no usa `exit()`: es
  robustez/UX, no seguridad real).
- El menú principal es "ciego": no hay auto-registro, el personal nuevo lo da de alta
  el admin.
- *Posible pregunta:* "¿qué pasa si me equivoco de clave?" → 3 intentos y vuelve al
  menú; "¿y la primera vez?" → modo fábrica.

---

## Slide 7 — Gestión de viajes

**En pantalla:**
- **Alta:** empresa, origen, destino, fecha, hora, precio_base (todos obligatorios).
  ID autogenerado (`V001`, `V002`...). Estado `activo`.
- **Modificación:** solo empresa, fecha, hora y precio. Origen y destino **NO** se
  editan. Mecanismo campo por campo (S/N antes de pedir cada uno).
- **Baja (soft-delete):** sin ventas → se borra. Con ventas → pasa a `cancelado`,
  no se borra.

**Notas (guion):**
- **Por qué origen/destino no se editan:** si se equivocaron, se da de baja y se crea
  otro. Cambiarlos rompería la coherencia de las ventas ya hechas sobre ese viaje.
- **Por qué soft-delete (lo más importante de defender acá):** una venta guarda el
  `id_viaje`, no una copia de los datos del viaje. Si borrara un viaje con ventas,
  esas ventas quedarían **huérfanas**, apuntando a algo que ya no existe (ticket sin
  viaje). Por eso "cancelar" = pasar a `cancelado`: deja de venderse pero sigue
  existiendo para mantener la integridad referencial.
- Borrado físico solo para viajes que **nunca** tuvieron una venta.
- *Posible pregunta:* "¿por qué no borran y listo?" → integridad referencial; mostrar
  el caso del ticket huérfano.

---

## Slide 8 — Gestión de usuarios

**En pantalla:**
- **Crear:** nombre (normalizado), clave, rol. No se puede recrear "admin". Anti-clones.
- **Desactivar:** soft-delete (estado `inactivo`), nunca se borra.
- **Resetear clave:** asigna clave nueva **y** reactiva al usuario.
- Regla anti-admin-suicida: no se puede desactivar al **último admin activo**.

**Notas (guion):**
- **Anti-admin-suicida (defender el detalle fino):** la cuenta es de admins
  **activos**, no totales. Si hay dos admins pero uno está inactivo, desactivar al que
  queda dejaría el sistema sin nadie que lo administre. La regla precisa: no se puede
  desactivar a un admin si es el último con estado activo.
- **Por qué los usuarios no se borran:** misma razón que los viajes. Un boletero
  borrado dejaría ventas con un `boletero` fantasma. Soft-delete siempre.
- **Reset = reactivar:** reactivar siempre implica clave nueva. Cierra el callejón de
  "lo desactivé sin querer y no hay vuelta" sin agregar otra opción de menú.
- *Posible pregunta:* "¿qué pasa con el historial de un usuario desactivado?" → se
  conserva, por eso no se borra.

---

## BLOQUE 2 · La funcionalidad estrella: la venta múltiple

---

## Slide 9 — Venta múltiple: la idea

**En pantalla:**
- El boletero carga **varios pasajeros en una sola operación** (tipo "carrito").
- Para cada pasajero: elige asiento → carga DNI, email, teléfono → siguiente.
- Muestra el **mapa de asientos en vivo** entre pasajero y pasajero.
- Es el flujo más complejo del TP2 y el que concentra los conceptos.

**Notas (guion):**
- Es el corazón del sistema y lo más vistoso para la demo.
- **Por qué cada pasajero completo antes del siguiente** (y no todos los asientos y
  después todos los datos): cada pasajero es una unidad cerrada; si algo falla con
  uno, falla ahí sin arrastrar a los demás, y se puede mostrar el mapa actualizado
  entre uno y otro.

---

## Slide 10 — Venta múltiple: todo o nada (atomicidad)

**En pantalla:**
- Durante la carga **no se registra ninguna venta ni se ocupa ningún asiento real**.
- Todo vive en estructuras temporales: un "carrito" y una "matriz de trabajo".
- Recién al confirmar se crean las N ventas **de una sola vez** y se guarda **una
  sola vez**.
- Cancelar en el medio es **gratis**: se descarta el carrito y nada cambió.

**Notas (guion):**
- **Atomicidad = todo o nada.** Como nada es real hasta la confirmación final, no
  hace falta código de "deshacer": la atomicidad es consecuencia de no tocar nada
  real hasta confirmar.
- Una sola escritura a disco al final, no N (eficiente y seguro).
- La confirmación usa **lista blanca**: solo `{"s", "si", "sí"}` confirma; cualquier
  otra cosa (Enter, "ok", "dale") cae en "no confirma" = cancela. Para algo
  irreversible con plata, el default seguro es no cobrar.
- *Posible pregunta:* "¿y si se corta la luz a mitad de carga?" → no pasa nada, no se
  escribió nada todavía; el sistema queda como estaba.

---

## Slide 11 — Venta múltiple: doble conjunto anti-duplicados

**En pantalla:**
```
Cada DNI nuevo se chequea contra DOS conjuntos:
  · Conjunto del viaje    → DNIs que ya compraron este micro antes
  · Conjunto de la sesión → DNIs cargados en esta misma compra
```
- Sin el del viaje → alguien recompra el mismo viaje.
- Sin el de la sesión → la familia mete dos veces el mismo DNI antes de confirmar.
- También se controla que no se repita un **asiento** (ventas reales + carrito).

**Notas (guion):**
- Este es el uso "estrella" de **conjuntos** del TP2; conviene explicarlo despacio.
- El conjunto del viaje se **deriva** de las ventas ya registradas; el de la sesión
  se va armando en la compra actual. Hacen falta los dos porque cubren momentos
  distintos: antes (ya compró) y ahora (lo repetí en este carrito, cuando todavía no
  hay ninguna venta registrada que lo detecte).
- *Posible pregunta:* "¿por qué un `set` y no una lista?" → pertenencia inmediata
  (`in`) y unicidad automática; es exactamente lo que necesitamos.

---

## BLOQUE 3 · Reportes

---

## Slide 12 — Reportes del administrador

**En pantalla:**
- **Recaudación total:** suma de todos los `precio_pagado` de las ventas.
- **Destinos activos únicos:** conjunto de destinos de los viajes activos
  (sin repetidos).
- **Mis Ventas (boletero):** historial filtrado por el boletero logueado, con su
  total.
- Sin datos → mensajes claros y total `$0.00` (no se rompe sobre listas vacías).

**Notas (guion):**
- Muchos de estos flujos son en el fondo **"filtrar una colección + mostrarla"** con
  distinto filtro: recaudación, Mis Ventas, destinos únicos, búsquedas de cartelera.
  No son funciones distintas que se parecen: son la misma operación.
- Acá aparecen `filter` + `lambda` (Mis Ventas) y `reduce` (sumar totales).
- *Posible pregunta:* "¿qué pasa si no hay ventas?" → devuelve `$0.00`, no crashea.

---

## BLOQUE 4 · Cómo está construido por dentro

---

## Slide 13 — Arquitectura en capas

**En pantalla:**
```
CAPA 5 · Orquestación   main + menús. Conecta todo: pide, decide y guarda.
CAPA 4 · Presentación   ui. Lo que el usuario ve y escribe.
CAPA 3 · Dominio        Reglas del negocio. Decide; no imprime ni pide datos.
CAPA 2 · Persistencia   Leer y escribir los archivos JSON.
CAPA 1 · Lógica pura    Validar, calcular, armar la grilla. No depende de nadie.
```
- **Ley única:** las dependencias solo apuntan hacia abajo. Nunca hacia arriba, nunca
  en círculo.

**Notas (guion):**
- Los tres mandamientos que no se violan:
  1. El **dominio** nunca hace `print()` ni `input()`: recibe datos, decide, devuelve.
  2. La **presentación** nunca aplica una regla de negocio: muestra y captura.
  3. El **único** que habla con los dos mundos (I/O y reglas) es la orquestación.
- **Por qué importa:** esta separación es lo que hace al sistema **testeable**. La
  Capa 1 y la Capa 3 se prueban pasándoles datos de juguete, sin consola ni archivos.
  Engancha directo con el slide de pruebas.
- Decisión crítica: **el dominio NO persiste.** Registrar una venta son dos pasos
  separados (modificar el diccionario en memoria, después guardar). Así el dominio se
  testea sin tocar disco.
- *Posible pregunta:* "¿por qué tantas capas para un TP?" → para poder testear y para
  que un cambio en un lado no rompa el otro; es lo que pedía la consigna (tests).

---

## Slide 14 — Modelo de datos: una sola fuente de verdad

**En pantalla:**
```
SE PERSISTE (la verdad)          SE DERIVA en memoria (vistas)
  usuarios.json                    → matriz de asientos 5×4
  viajes.json                      → conjunto de DNIs por viaje
  ventas.json  (FUENTE DE VERDAD)  → asientos libres
                                   → destinos activos únicos
```
- Principio: **todo lo que se puede calcular NO se guarda: se calcula.**

**Notas (guion):**
- El problema que resuelve: un mismo hecho ("el DNI X compró el asiento 2-3 del
  V001") podía quedar escrito en 4 lugares a la vez (matriz, conjunto, ventas,
  contador). Cuatro copias = cuatro cosas que se desincronizan. Esa desincronización
  es el bug clásico que rompe los sistemas de reservas.
- Solución: un único dueño del dato (las **ventas**) y todo lo demás se **deriva** en
  el momento, con funciones puras, y se descarta.
- **Cumple la consigna sin trampa:** "implementar una matriz" = usarla en memoria (se
  construye, se recorre, se muestra); "los datos persisten" = lo que sobrevive son las
  ventas. La matriz no se guarda: se proyecta desde las ventas cada vez.
- Beneficio sobre JSON: como ningún `set` se guarda, los JSON solo tienen tipos
  nativos (no hay que convertir set↔lista).
- *Posible pregunta:* "¿dónde está la matriz guardada?" → en ningún lado; se calcula
  desde las ventas cuando se necesita. Es una decisión, no un olvido.

---

## BLOQUE 5 · Los 6 conceptos del TP2

---

## Slide 15 — Diccionarios y Tuplas

**En pantalla:**
- **Diccionarios** (estructura principal): usuarios, viajes y ventas son
  **diccionarios de diccionarios**; la clave externa es el ID de cada elemento.
- **Tuplas** (inmutables):
  - coordenada de asiento `(fila, columna)`
  - el ticket emitido (no se modifica nunca)
  - el resultado `(exito, mensaje)` de las reglas de negocio

**Notas (guion):**
- Decir **dónde** se usa cada uno, no leer código.
- Diccionarios: se cargan al inicio y se pasan **por parámetro** (sin variables
  globales) → testabilidad, una sola fuente de estado, claridad de dependencias.
- Tuplas: la coordenada circula por todo el flujo de venta; el ticket es inmutable
  porque un pasaje, una vez emitido, no se toca; `(exito, mensaje)` es cómo las reglas
  devuelven su resultado al flujo.
- *Posible pregunta:* "¿por qué tupla y no lista para el ticket?" → porque es
  inmutable: modela que el comprobante no cambia.

---

## Slide 16 — Conjuntos y Excepciones

**En pantalla:**
- **Conjuntos:** doble anti-duplicados de DNI (venta múltiple), destinos activos
  únicos, y la lista blanca de confirmación `{"s", "si", "sí"}`.
- **Excepciones:** manejo de archivos (`FileNotFoundError`, `JSONDecodeError`) y
  conversión de tipos (`ValueError` al leer un número).
- Las **reglas de negocio NO usan excepciones**: devuelven un resultado.

**Notas (guion):**
- Conjuntos: ya explicado el doble anti-duplicados (slide 11); destinos únicos
  deduplica solo; lista blanca acepta el "sí" inequívoco.
- **La línea clave a defender:** un asiento ocupado o un DNI duplicado **no es un
  error del programa**, es un resultado normal del negocio que pasa todos los días →
  se maneja devolviendo `(exito, mensaje)`. Usar excepciones para control de flujo de
  negocio es un anti-patrón.
- Las excepciones se reservan para lo de verdad excepcional: que falte un archivo, que
  esté corrupto, que el usuario tipee letras donde va un número.
- *Posible pregunta:* "¿por qué no envuelven todo en try/except por las dudas?" →
  porque eso esconde bugs; cada except tiene un motivo concreto.

---

## Slide 17 — Archivos (persistencia)

**En pantalla:**
- Persistencia en **JSON**: `usuarios.json`, `viajes.json`, `ventas.json`.
- `cargar` lee y devuelve un diccionario; `guardar` sobrescribe el archivo completo.
- Ruta **relativa** a la ubicación del script (portable, sin rutas absolutas).
- Guardado **inmediato** tras cada cambio (transaccional).

**Notas (guion):**
- `ruta_data` arma la ruta a `data/` relativa al script → corre en cualquier
  computadora.
- Guardado inmediato = el archivo se actualiza apenas se modifica un dato (alta de
  viaje, venta confirmada, desactivar usuario...). Protege contra pérdida de datos si
  el programa se cierra.
- **Decisión sobre archivo corrupto:** si el JSON está dañado, se avisa y se **frena**
  sin tocar nada (no se trata como vacío, porque eso sobrescribiría datos reales que
  quizás se recuperan a mano). Ante la duda, nunca destruir datos.
- *Posible pregunta:* "¿qué pasa la primera vez, sin archivos?" → `cargar` devuelve
  `{}` y arranca en modo fábrica.

---

## Slide 18 — Pruebas unitarias

**En pantalla:**
- **82 pruebas** con `unittest`, todas en verde.
- Prueban las funciones puras (Capa 1) y las reglas de negocio (Capa 3).
- Cada prueba **arma sus propios datos**: no tocan los archivos reales.
- Se verifican casos correctos **y** casos de error.

**Notas (guion):**
- Ejemplos de casos de error probados: DNI inválido rechazado, no se puede desactivar
  al último admin, asiento ocupado, etc.
- **Por qué se pueden testear sin tocar disco:** porque el dominio no persiste y
  recibe los datos por parámetro (engancha con arquitectura). Cada test pasa un
  diccionario de juguete.
- Si se puede, mostrar la corrida verde en vivo:
  `python -m unittest discover -s tests` desde `src`.
- *Posible pregunta:* "¿prueban la interfaz?" → no, se prueban la lógica pura y las
  reglas; la presentación (print/input) no se testea unitariamente.

---

## BLOQUE 6 · Decisiones, casos borde y cierre

---

## Slide 19 — Decisiones de diseño defendibles

**En pantalla:**
- **Reglas vs. excepciones:** las reglas devuelven `(exito, mensaje)`; las
  excepciones, solo para archivos y conversión de tipos.
- **Normalizar ≠ validar:** primero se prepara el dato (strip, lower, coma→punto),
  después se juzga.
- **Lista blanca** en la confirmación de venta (operación con plata).
- **Precio congelado** en cada venta (`precio_pagado`).
- **Claves en texto plano** (hashing fuera de alcance).

**Notas (guion):**
- **Normalización vs. validación:** normalizar es generoso y barato (corregir el
  tipeo es amable); validar es estricto cuando equivocarse es caro. La **clave NO se
  normaliza** (aplicar `lower` achicaría el espacio de claves).
- **Precio congelado (sutil, buen punto):** parece derivable (`precio_base × 1.16`),
  pero el admin puede cambiar el precio del viaje después. La venta guarda lo que el
  pasajero **realmente pagó ese día** → es una foto del momento, no se recalcula.
- **Claves en texto plano:** se dice **honestamente**: "sabemos que en producción se
  hashea, está fuera del alcance de la materia". No se esconde ni se llama "seguro".
- *Posible pregunta:* "¿es seguro guardar las claves así?" → no, y lo sabemos; el
  hashing está fuera de alcance, lo declaramos a propósito.

---

## Slide 20 — Casos borde contemplados

**En pantalla:**
- Archivos: no existen → `{}`; corrupto → avisar y frenar; `usuarios` vacío → modo
  fábrica.
- Viajes: ID inexistente → avisar; cartelera vacía → mensaje, no tabla rota.
- Venta: viaje sin asientos → bloqueado desde el inicio; pedir más asientos que los
  libres → "solo quedan X"; cancelar a mitad → atómico.
- Usuarios: desactivar al último admin → bloqueado; nombre duplicado → bloqueado;
  desactivar a uno ya inactivo → aviso (no-op).
- Reportes: sin datos → `$0.00` / mensaje, no crashea.

**Notas (guion):**
- Mostrar que el sistema no se rompe ante lo inesperado: cada borde tiene una respuesta
  pensada, no un crash.
- Este slide es buen colchón para preguntas sueltas del profe: probablemente lo que
  pregunte ya esté acá.

---

## Slide 21 — Demo en vivo (guion)

**En pantalla:**
- 1. Arranque en **modo fábrica** → crear admin real.
- 2. Login como admin → **alta de un viaje**.
- 3. Login como boletero → **venta múltiple** (mostrar mapa + anti-duplicados).
- 4. Volver a admin → **recaudación** y **destinos únicos**.
- 5. Correr los **82 tests** en verde.

**Notas (guion):**
- El mejor momento para impresionar: la venta múltiple (paso 3) y los tests (paso 5).
- En la venta, provocar a propósito un DNI repetido y un asiento ocupado para mostrar
  los controles.
- **Recordar restaurar los datos al terminar:** `git restore data/` (la demo crea un
  admin y ventas de prueba).
- Tener la terminal lista de antemano (en la carpeta `src`).

---

## Slide 22 — Conclusión

**En pantalla:**
- Integra los 6 conceptos del TP2 de forma coherente con el negocio, no forzada.
- El diseño en capas + los datos en un solo lugar lo hacen ordenado y fácil de probar.
- Resultado: app de consola funcional, portable y con la información guardada de forma
  segura entre ejecuciones.
- ¿Preguntas?

**Notas (guion):**
- Cerrar reforzando: cada concepto está donde tiene sentido (diccionarios = estructura
  base, conjuntos = unicidad, tuplas = inmutabilidad, excepciones = lo excepcional).
- Quedar abiertos a preguntas; usar los slides de decisiones (19) y casos borde (20)
  como respaldo si el profe profundiza.

---

## Consejos de armado

- **Este power es nuestro apoyo, no del público:** está bien que tenga bastante texto.
  Aun así, en pantalla conviene estructura y términos clave; el desarrollo largo va en
  las **notas del orador** de cada slide.
- **Consistencia visual:** mismo tipo de letra, colores sobrios. Los bloques de
  diagrama/código, en fuente **monoespaciada**.
- **Las notas del orador son el guion:** al generar el `.pptx`, cargar las notas en el
  panel de notas de cada diapositiva (no en el cuerpo visible).
- **Demo en vivo:** mejores momentos, slide 21 (venta) y los tests. Restaurar datos
  después con `git restore data/`.
- **Si lo generan con Claude web:** pasarle ESTE archivo como base (no la
  arquitectura). Pedir un `.pptx` con estos 22 slides, estilo sobrio, diagramas en
  monoespaciado, y que el contenido de "Notas (guion)" vaya al panel de **notas** de
  cada slide.
