# 🚌 Nexus Viajes — Apunte del Sistema

> Una vuelta de lectura para entender **qué hace el sistema y cómo está armado**, sin tecnicismos ni código. Si el Documento de Arquitectura es el plano de ingeniería, esto es el folleto que te explica la casa.

---

## 🧭 Índice

1. [¿Qué es esto, en una frase?](#1)
2. [¿Quién lo usa? Los dos roles](#2)
3. [El primer arranque: el "modo fábrica"](#3)
4. [Entrar al sistema: el login](#4)
5. [Lo que puede hacer cada uno](#5)
6. [La venta, contada como una escena](#6)
7. [Cómo está construido por dentro (en criollo)](#7)
8. [Las cinco ideas que sostienen todo](#8)
9. [¿Dónde vive la información?](#9)
10. [Resumen de la heladera](#10)

---

<a name="1"></a>
## 1. 🎯 ¿Qué es esto, en una frase?

Es un sistema de **venta y gestión de pasajes de micro**, que funciona enteramente por **consola** (texto, sin ventanas ni mouse). Lo usan los empleados de una terminal: alguien que vende pasajes y alguien que administra los viajes y al personal.

No es una página web ni una app con botones. Es un programa que se abre en la terminal, te hace preguntas, y vos respondés tecleando. Simple por fuera, ordenado por dentro.

---

<a name="2"></a>
## 2. 👥 ¿Quién lo usa? Los dos roles

Todo el sistema gira alrededor de **dos tipos de usuario**, y cada uno ve un mundo distinto:

- **🎟️ El boletero.** Es el que está en la ventanilla. Su trabajo es uno solo: **vender pasajes**. Por eso el sistema le muestra únicamente lo que puede vender y le esconde el resto, para que no se confunda.

- **🛠️ El administrador.** Es el que maneja el negocio. **Crea los viajes, los modifica, los da de baja, da de alta a los boleteros** y mira los reportes. Ve todo, incluso lo que ya no se vende.

La idea de fondo: cada uno tiene exactamente las herramientas que necesita y ninguna que pueda usar mal. Un boletero nunca puede borrar un viaje; un administrador no anda vendiendo desde su menú.

---

<a name="3"></a>
## 3. 🏭 El primer arranque: el "modo fábrica"

Cuando el sistema se enciende por **primerísima vez** (o si alguien borra los datos de usuarios), no hay nadie cargado todavía. Sería un huevo y la gallina: para crear un administrador necesitás ser administrador.

La solución es el **modo fábrica**. La primera vez, el sistema trae un usuario provisorio de fábrica y, en vez de pedirte que inicies sesión con él, te lleva derecho a **crear tu administrador real** (tu nombre, tu clave). Una vez creado, el usuario de fábrica se borra y no vuelve nunca más. A partir de ahí el sistema queda en **modo normal** para siempre.

Es el mismo gesto que cuando comprás un router nuevo: viene con una clave genérica, lo primero que hacés es poner la tuya, y la genérica desaparece.

---

<a name="4"></a>
## 4. 🔐 Entrar al sistema: el login

En modo normal, lo primero que ves es un **menú "ciego"**: iniciar sesión, ayuda, o salir. Ciego porque no muestra nada del negocio hasta que sepa quién sos.

Iniciás sesión con tu usuario y clave. El sistema chequea tres cosas: que el usuario exista, que la clave coincida y que tu cuenta esté **activa**. Si fallás tres veces seguidas, te devuelve al menú principal (no te bloquea la computadora ni nada dramático: es solo para cortar el manoseo).

Cuando entrás bien, el sistema mira tu rol y te manda al menú que te corresponde: **boletero** o **administrador**. Cerrar sesión te devuelve al menú ciego, listo para el próximo empleado.

> Una nota honesta: las claves se guardan **tal cual**, sin encriptar. En un sistema real eso se "hashea", pero eso queda fuera del alcance de la materia. Lo decimos de frente, no lo escondemos.

---

<a name="5"></a>
## 5. 🧰 Lo que puede hacer cada uno

### 🎟️ El boletero

- **Ver la cartelera vendible** → solo los viajes activos que todavía tienen asientos. Lo demás no aparece.
- **Vender pasajes** → el corazón del sistema (lo cuento en la próxima sección).
- **Ver "Mis Ventas"** → el historial de lo que vendió esa persona, con su total.

### 🛠️ El administrador

- **Ver la cartelera completa** → todos los viajes, incluso los cancelados y los llenos.
- **Gestión de viajes** → dar de **alta** uno nuevo, **modificarlo** (empresa, fecha, hora, precio) o darlo de **baja**.
- **Gestión de usuarios** → **crear** boleteros o admins, **desactivarlos** o **resetearles la clave**.
- **Reportes** → la **recaudación total** y la lista de **destinos activos** (sin repetir).

Un detalle que se repite en todo el sistema: **primero se muestra, después se pide**. Nunca te pregunta "¿qué viaje querés modificar?" a ciegas; siempre te enseña la lista antes para que elijas sobre algo que estás viendo.

---

<a name="6"></a>
## 6. 🛒 La venta, contada como una escena

La venta es el flujo más interesante, así que va contado como una escena real en la ventanilla.

> Llega una familia de cuatro a comprar pasajes para el viaje a Bariloche.

**Primero**, el boletero elige el viaje y dice cuántos pasajeros son: cuatro. El sistema chequea que haya al menos cuatro asientos libres.

**Después**, va pasajero por pasajero, uno completo antes del siguiente:
- Le muestra el **mapa de asientos** (una grillita de los 20 lugares, marcando cuáles están libres y cuáles ocupados).
- Elige el asiento, carga el DNI, el email y el teléfono.
- Y acá entra la estrella del sistema: el **doble control de DNI repetido**. El sistema no deja que la misma persona compre dos pasajes en el mismo viaje. Lo chequea contra dos listas a la vez: contra los que **ya compraron antes** (en ventas viejas) y contra los que **se están cargando en esta misma compra**. Así no se cuela un repetido ni por recompra ni por error de tipeo en la misma familia.

**Lo importante:** mientras carga, **nada es real todavía**. Los asientos no se reservan de verdad, las ventas no se anotan. Todo vive en un "carrito" temporal, como cuando comprás online y todavía no apretaste "pagar".

**Al final**, el sistema muestra el resumen con los cuatro pasajes y el total, y pregunta: *¿confirmás?* Solo si la respuesta es un **sí** claro y sin vueltas, recién ahí se anotan las cuatro ventas de una sola vez y se imprimen los comprobantes.

¿Y si la familia se arrepiente a mitad de camino? **Cancelar es gratis.** Como nada se había anotado de verdad, no hay nada que deshacer: se tira el carrito y listo. Esto se llama que la venta es **atómica**: o pasa entera, o no pasa nada.

> El precio se calcula sumándole un **16% de recargo** al precio base del viaje. Y ojo con un detalle fino: el precio que pagó cada pasajero **se guarda congelado** en su venta. Si mañana el admin sube el precio del viaje, los pasajes viejos siguen mostrando lo que esa persona realmente pagó ese día.

---

<a name="7"></a>
## 7. 🏗️ Cómo está construido por dentro (en criollo)

Esto es lo que más impresiona del proyecto, contado fácil. En vez de tener todo el programa amontonado en un solo bloque (como era la versión anterior), el sistema está dividido en **capas**, como los pisos de un edificio. La regla de oro: **cada piso solo puede apoyarse en los de abajo, nunca en los de arriba.**

De abajo hacia arriba:

- **🧱 El cimiento: lógica pura.** Funciones que reciben datos y devuelven datos, sin hablar con nadie. ¿El DNI tiene el formato correcto? ¿Cuánto es el precio con recargo? ¿Cómo queda el mapa de asientos? Son las piezas más sólidas y las más fáciles de poner a prueba.

- **💾 La persistencia.** El piso que sabe leer y escribir los archivos del disco. Nada más. No entiende de reglas del negocio, solo de guardar y traer.

- **⚖️ El dominio (las reglas).** Acá viven las decisiones del negocio: ¿este DNI ya compró? ¿se puede dar de baja este viaje? ¿es el último administrador? Este piso **decide**, pero no muestra ni pregunta nada en pantalla.

- **🖥️ La presentación.** Todo lo que el usuario **ve y teclea**: los menús, las tablas, el mapa de asientos, los mensajes. Este piso **muestra y pregunta**, pero no toma ni una sola decisión del negocio.

- **🎬 La orquestación.** El director de orquesta. Le pide un dato a la presentación, se lo pasa al dominio para que aplique la regla, agarra el resultado y, si hace falta, le dice a la persistencia que lo guarde. Es el único que conoce todos los pisos.

¿Por qué tanto orden? Por dos razones muy concretas: **se puede probar pieza por pieza** (sobre todo el cimiento y las reglas), y **cambiar una cosa no rompe las demás**, porque cada piso tiene un trabajo y uno solo.

---

<a name="8"></a>
## 8. 💡 Las cinco ideas que sostienen todo

Si tuvieras que explicar el diseño en cinco frases, son estas:

1. **🎯 Una sola fuente de verdad.** El hecho "fulano compró tal asiento de tal viaje" se guarda en **un solo lugar** (las ventas). Todo lo demás —el mapa de asientos, cuántos lugares quedan, quiénes ya compraron— **no se guarda: se calcula** a partir de las ventas en el momento que se necesita. Así nunca hay dos datos que digan cosas distintas.

2. **🗑️ No se borra, se desactiva.** Un viaje que ya tuvo ventas no se elimina: se marca como "cancelado". Un usuario tampoco se borra: se pone "inactivo". Borrar de verdad dejaría pasajes apuntando a viajes fantasma o ventas con un vendedor que ya no existe. (A esto se le dice *baja lógica* o *soft-delete*.)

3. **🛒 La venta es todo o nada.** Como conté antes: hasta que no confirmás, no pasó nada. Eso hace que cancelar sea instantáneo y que nunca quede una venta a medias.

4. **🚫 Nadie se queda afuera por accidente.** El sistema no te deja desactivar al **último administrador activo** (si no, nadie podría volver a administrar). Y no deja crear dos usuarios con el mismo nombre. Pequeños candados contra los errores que más duelen.

5. **🧮 Calcular es más barato que sincronizar.** Rearmar el mapa de 20 asientos cada vez que se necesita es instantáneo, y elimina de raíz el peor bug de los sistemas de reservas: que el mapa diga una cosa y el contador diga otra. Mejor calcular fresco que mantener copias que se pelean entre sí.

---

<a name="9"></a>
## 9. 📂 ¿Dónde vive la información?

Lo que tiene que **sobrevivir** cuando se apaga el programa se guarda en tres archivos de texto (formato JSON, que es texto legible y ordenado):

- **`usuarios`** → quién puede entrar, su rol y si está activo.
- **`viajes`** → la cartelera: empresa, origen, destino, fecha, hora, precio, estado.
- **`ventas`** → cada pasaje vendido. **Este es el archivo más importante**, porque de él se deriva casi todo lo demás.

El mapa de asientos, los DNIs que ya compraron, los lugares libres: nada de eso se guarda. Se arma en memoria cuando hace falta y se descarta. El disco queda limpio, guardando solo los hechos, no las fotos de los hechos.

El sistema también se cuida de los accidentes: si un archivo no existe, arranca vacío (modo fábrica); si un archivo está **dañado**, avisa y se detiene sin tocar nada, antes que arriesgarse a pisar datos que quizás se puedan recuperar.

---

<a name="10"></a>
## 10. 🧊 Resumen de la heladera

Si pegaras una nota en la heladera con lo esencial, diría:

> Un sistema de venta de pasajes por consola, con dos roles (boletero y admin). Vende en "carrito" atómico con doble control de DNI repetido. Guarda solo los hechos esenciales en tres archivos y calcula todo lo demás al vuelo. Está armado en capas para poder probarlo y mantenerlo sin que se desarme. No borra nada importante: lo desactiva.

Y eso es, en esencia, todo el sistema. 🚌💨
