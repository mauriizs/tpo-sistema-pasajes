# Indicaciones para el PowerPoint

Contenido slide por slide para la presentación del TP2. Está basado en
`documentacion-tp2.md`. Cada slide tiene: **título**, **bullets** (lo que se ve en pantalla) y
**notas** (lo que se cuenta / qué mostrar). Mantener pocos bullets por slide y
texto corto: la diapositiva acompaña, no se lee de corrido.

---

## Slide 1 — Carátula

**Título:** Nexus Viajes — Sistema de Gestión y Venta de Pasajes de Micro

**Bullets:**
- Algoritmos y Estructura de Datos I — UADE
- Grupo 9
- Integrantes: Farfan, Mauricio · Velasquez, Lorena · Astudillo, Valentina ·
  Chaina, Brian · Ayala, Alan
- Fecha: 19 de junio de 2026

**Notas:** Portada. Mismo encabezado que la documentación escrita.

---

## Slide 2 — ¿Qué es?

**Título:** ¿Qué es el sistema?

**Bullets:**
- Sistema de venta de pasajes de micro, por consola, en Python.
- Administra usuarios, viajes y ventas.
- La información se conserva entre ejecuciones (archivos JSON).
- No requiere instalar nada: solo la biblioteca estándar de Python.

**Notas:** Presentar el problema en una frase: una boletería de micros
digitalizada. Aclarar que corre en cualquier computadora.

---

## Slide 3 — Roles de usuario

**Título:** Dos roles, dos menús

**Bullets:**
- **Administrador:** gestiona viajes (alta/baja/modificación), gestiona usuarios y
  consulta reportes (recaudación y destinos únicos).
- **Boletero:** consulta la cartelera vendible, vende pasajes y revisa su historial.
- Cada usuario, al iniciar sesión, ve solo el menú de su rol.

**Notas:** Dejar claro que el sistema separa responsabilidades. El boletero NO ve
los viajes cancelados ni los reportes; el admin ve todo.

---

## Slide 4 — Funcionalidad estrella: la venta múltiple

**Título:** Venta múltiple (todo o nada)

**Bullets:**
- El boletero carga varios pasajeros en un "carrito" en una sola operación.
- Nada se registra hasta confirmar: si se cancela en el medio, no queda nada a
  medias.
- Muestra el mapa de asientos en vivo.
- Evita repetir un asiento o un DNI dentro de la misma compra (y contra ventas
  anteriores del mismo viaje).

**Notas:** Es el flujo más complejo y el más vistoso para mostrar en la demo.
Si se hace demo en vivo, este es el momento. Resaltar el control anti-duplicados.

---

## Slide 5 — Arquitectura en capas

**Título:** Diseño en capas

**Bullets (mostrar como diagrama / bloque monoespaciado):**
```
CAPA 5 · Menús           main + menús. Conecta todo: pide, decide y guarda.
CAPA 4 · Presentación    Lo que el usuario ve y escribe.
CAPA 3 · Reglas          Reglas del negocio. Decide, no imprime ni pide datos.
CAPA 2 · Persistencia    Leer y escribir los archivos.
CAPA 1 · Funciones puras Validar, calcular, armar la grilla.
```

**Notas:** Cada capa solo depende de las de abajo, nunca al revés. Esa separación
es lo que permite probar la lógica de forma aislada (enganchar con el slide de
pruebas). No entrar en detalle de cada módulo: con el diagrama alcanza.

---

## Slide 6 — Conceptos del TP2 (1 de 2)

**Título:** Conceptos aplicados (1/2)

**Bullets:**
- **Diccionarios:** estructura principal. Usuarios, viajes y ventas son
  diccionarios de diccionarios (la clave es el ID de cada elemento).
- **Tuplas:** coordenada de asiento `(fila, columna)`, el ticket emitido (inmutable)
  y el resultado `(exito, mensaje)` de las reglas.
- **Conjuntos:** anti-duplicados de DNI, destinos activos únicos y la lista blanca
  de confirmación `{"s", "si", "sí"}`.

**Notas:** Una línea por concepto, diciendo DÓNDE se usa. No leer código en la
diapositiva; si acaso, un ejemplo cortito de la doc.

---

## Slide 7 — Conceptos del TP2 (2 de 2)

**Título:** Conceptos aplicados (2/2)

**Bullets:**
- **Excepciones:** manejo de archivos (archivo inexistente o corrupto) y conversión
  de tipos (`ValueError` al leer un número). Las reglas de negocio NO usan
  excepciones: devuelven un resultado.
- **Archivos:** persistencia en JSON (`cargar` / `guardar`). Ruta relativa, guardado
  inmediato tras cada cambio.
- **Pruebas unitarias:** `unittest`, 82 pruebas, casos correctos y de error.

**Notas:** Destacar la decisión de diseño: excepciones solo para lo excepcional
(archivos/tipos), no para las reglas del negocio (eso es lo normal del sistema).

---

## Slide 8 — Pruebas

**Título:** Pruebas unitarias

**Bullets:**
- 82 pruebas con `unittest`, todas en verde.
- Prueban las funciones puras (Capa 1) y las reglas de negocio (Capa 3).
- Cada prueba arma sus propios datos: no tocan los archivos reales.
- Se verifican casos correctos Y casos de error (DNI inválido, no desactivar al
  último admin, etc.).

**Notas:** Si se puede, mostrar la corrida verde en consola
(`python -m unittest discover -s tests`). Es el respaldo de que el sistema funciona.

---

## Slide 9 — Conclusión

**Título:** Conclusión

**Bullets:**
- Integra los 6 conceptos del TP2 de forma coherente con el negocio.
- El diseño en capas y los datos en un solo lugar lo hacen ordenado y fácil de
  probar.
- Resultado: una aplicación de consola funcional, portable y con la información
  guardada de forma segura.

**Notas:** Cerrar reforzando que cada concepto está donde tiene sentido, no forzado.

---

## Consejos de armado

- **Pocos bullets, frases cortas.** La diapositiva es apoyo visual.
- **Consistencia visual:** mismo tipo de letra, colores sobrios (es un TP, no una
  campaña). Los bloques de código/diagrama, en fuente monoespaciada.
- **Demo en vivo (opcional):** si la hacen, el mejor momento es el slide 4 (venta
  múltiple) y el slide 8 (tests en verde). Recordar restaurar los datos después con
  `git restore data/`.
- **Si lo generan con Claude web:** pasarle ESTE archivo como base (no la
  arquitectura). Pedir un `.pptx` con estos 9 slides, estilo sobrio y diagrama en
  monoespaciado.
