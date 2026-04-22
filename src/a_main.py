# estructura del trabajo.
# tpo-sistema-pasajes/
# ├── docs/                   <-- Acá irá el PDF con la documentación final
# ├── src/                    <-- Carpeta de código fuente
# │   ├── a_main.py             (El Menú principal que une todo el programa)
# │   ├── b_info.py             (Muestra los datos y bienvenida de la agencia)
# │   ├── c_micro.py            (Crea, muestra y modifica la matriz de asientos)
# │   ├── d_busquedas.py        (Tiene el catálogo de viajes y usa 'filter')
# │   ├── e_validaciones.py     (Funciones con RegEx para validar DNI, fecha, email)
# │   └── f_finanzas.py         (Cálculos de precios usando 'map' y 'reduce')
# ├── anotaciones.md          <-- Notas temporales de desarrollo
# └── instrucciones.md        <-- Guía de uso del sistema


from b_info import mostrar_bienvenida
from c_micro import mostrar_micro, asiento_esta_libre, reservar_asiento
from d_busquedas import catalogo_viajes, buscar_viajes, buscar_por_id
from e_finanzas import aplicar_recargo, calcular_recaudacion_total, ventas_diarias
from f_validaciones import validar_fecha, validar_dni, validar_email, validar_telefono


def main():
    mostrar_bienvenida()
    
    while True:
        print("\n-------- SISTEMA DE GESTION DE VENTAS --------")
        print(" [1] Buscar viaje         [2] Comprar pasaje ")
        print(" [3] Ver recaudacion      [4] Salir")
        print("----------------------------------------------")
        
        opcion = input("\n> Selecciona una opcion: ")
        
        if opcion == "1":
            print("\n╔════════════════════════════════════════════╗")
            print("║             BUSCADOR DE VIAJES             ║")
            print("╚════════════════════════════════════════════╝")
            
            origen = input("\n> Ingresá el origen: ")
            destino = input("> Ingresá el destino: ")
            
            fecha_input = input("> Ingresá la fecha (dd/mm): ")
            fecha_validada = validar_fecha(fecha_input)
            
            # Llamamos al filter() que está en d_busquedas.py
            resultados = buscar_viajes(origen, destino, fecha_validada)
            
            print("\n ----------------------------------------------")
            print("           RESULTADOS ENCONTRADOS:           ")
            print(" ----------------------------------------------\n")

            if len(resultados) > 0:
                print("  ID | EMPRESA        | FECHA | PRECIO BASE")
                print("  ---|----------------|-------|------------")
                for viaje in resultados:
                    # viaje[0]: ID, viaje[1]: Empresa, viaje[4]: Fecha, viaje[5]: Precio
                    id_v = str(viaje[0]).zfill(2)
                    empresa = f"{viaje[1]:<14}" 
                    fecha = viaje[4]
                    precio = f"$ {viaje[5]:>6}"
                    
                    print(f"  {id_v} | {empresa} | {fecha} | {precio}")
    
                print("\n ----------------------------------------------")
            else:
                print(" [ERROR] No se encontraron viajes para los datos ingresados.")
            
            input("\n Presione [ENTER] para volver al menú...")

        elif opcion == "2":
            print("\n╔════════════════════════════════════════════╗")
            print("║               COMPRAR PASAJE               ║")
            print("╚════════════════════════════════════════════╝")
            
            # PASO A: Ingresar ID
            id_buscado = input("\n> Ingresá el ID del viaje deseado: ")
            viaje = buscar_por_id(id_buscado) # Función de d_busquedas
            
            # Caso Borde: ID Inexistente
            if not viaje:
                print("\n ----------------------------------------------")
                print(" [ ERROR ] El ID ingresado no existe en el catálogo.")
                print(" ----------------------------------------------\n")
                input(" Presione [ENTER] para volver al menú...")
                continue # Vuelve al Menú Principal
                
            empresa, destino, fecha, precio_base, matriz = viaje[1], viaje[3], viaje[4], viaje[5], viaje[6]
            print(f"\nHas seleccionado: {destino} - {fecha} ({empresa})")
            
            # PASO B: Mapa de Asientos        
            while True:
                mostrar_micro(matriz)
                
                fila_input = input("> Ingresá la fila (1-3) o '0' para cancelar: ")
                if fila_input == "0":
                    print("\n ----------------------------------------------")
                    print(" [ INFO ] Operación cancelada por el usuario.")
                    print(" ----------------------------------------------\n")
                    break # Sale del bucle de compra y vuelve al menú
                    
                col_input = input("> Ingresá la columna (1-4) o '0' para cancelar: ")
                if col_input == "0":
                    print("\n ----------------------------------------------")
                    print(" [ INFO ] Operación cancelada por el usuario.")
                    print(" ----------------------------------------------\n")
                    break
                    
                # Caso Borde: Validar que tipeó números y no letras
                if not (fila_input.isdigit() and col_input.isdigit()):
                    print("\n ------------------------------------------------------")
                    print(" [ ERROR ] Debes ingresar números válidos.")
                    print(" ------------------------------------------------------\n")
                    continue    
                    
                fila = int(fila_input)
                columna = int(col_input)
                
                # Caso Borde: Asiento fuera de rango (1 a 3 filas, 1 a 4 columnas)
                if not (1 <= fila <= 3 and 1 <= columna <= 4):
                    print("\n ------------------------------------------------------")
                    print(" [ ERROR ] Coordenadas fuera de rango. El micro tiene 3 filas y 4 columnas.")
                    print(" ------------------------------------------------------\n")
                    continue
                
                # DIAGRAMA: ¿Asiento Libre?
                if not asiento_esta_libre(matriz, fila, columna):
                    print("\n ------------------------------------------------------")
                    print(" [ ERROR ] El asiento seleccionado ya está ocupado.")
                    print(" ------------------------------------------------------\n")
                    continue # Vuelve a mostrar el mapa
                    
                print("\n------------------------------------------------------")
                print("> [ OK ] Asiento disponible. Iniciando Check-in...")
                print("------------------------------------------------------\n")
                
                # PASO C: Registro de Pasajeros (Validar con RegEx)
                print("        ╔══════════════════════════════════════╗")
                print("        ║          DATOS DEL PASAJERO          ║")
                print("        ╚══════════════════════════════════════╝\n")

                dni_input = input("> Ingresá tu DNI (sin puntos): ")
                dni = validar_dni(dni_input)
                
                email_input = input("> Ingresá tu Email: ")
                email = validar_email(email_input)
                
                tel_input = input("> Ingresá tu Teléfono: ")
                tel = validar_telefono(tel_input)
                
                print("\n ------------------------------------------------------")
                print("        [ PROCESANDO DATOS... POR FAVOR ESPERE ]")
                print(" ------------------------------------------------------\n")
                
                # PASO D: Liquidación y Emisión (Calcular recargo con map)
                precio_final = aplicar_recargo(precio_base)
                recargo = precio_final - precio_base
                
                # Armamos las líneas del ticket con espacios fijos (42 caracteres de ancho interno)
                l1 = f"Pasajero: DNI {dni}"
                l2 = f"Destino:  {destino} | Fecha: {fecha}"
                l3 = f"Asiento:  Fila {fila}, Columna {columna}"
                l4 = f"Precio Base:              $ {precio_base:>8.2f}"
                l5 = f"Cargo por servicio (16%): $ {recargo:>8.2f}"
                l6 = f"TOTAL A PAGAR:            $ {precio_final:>8.2f}"
                
                print("╔════════════════════════════════════════════╗")
                print("║             RESUMEN DE COMPRA              ║")
                print("╠════════════════════════════════════════════╣")
                print(f"║ {l1:<42} ║")
                print(f"║ {l2:<42} ║")
                print(f"║ {l3:<42} ║")
                print("╠════════════════════════════════════════════╣")
                print(f"║ {l4:<42} ║")
                print(f"║ {l5:<42} ║")
                print("║ ------------------------------------------ ║")
                print(f"║ {l6:<42} ║")
                print("╚════════════════════════════════════════════╝\n")

                # DIAGRAMA: ¿Confirmar Compra?
                confirmacion = input("\n> ¿Confirmar pago y emitir pasaje? (S/N): ").upper()
                
                if confirmacion == "S":
                    # Actualizar Matriz (L -> O)
                    reservar_asiento(matriz, fila, columna)
                    
                    # Guardar Venta en Memoria
                    ventas_diarias.append(precio_final)
                    
                    # Emitir Ticket
                    t1 = f"TITULAR DNI: {dni}"
                    t2 = f"DESTINO:     {destino} | FECHA: {fecha}"
                    t3 = f"ASIENTO:     Fila {fila} - Columna {columna}"
                    t4 = f"TOTAL:       $ {precio_final:.2f}"
                    
                    print("\n PAGO EXITOSO - Generando pasaje...\n")
                    print(" ╔══════════════════════════════════════════╗")
                    print(" ║      TICKET DE VIAJE - CENTRAL MICRO     ║")
                    print(" ╠══════════════════════════════════════════╣")
                    print(f" ║ {t1:<40} ║")
                    print(f" ║ {t2:<40} ║")
                    print(f" ║ {t3:<40} ║")
                    print(f" ║ {t4:<40} ║")
                    print(" ╠══════════════════════════════════════════╣")
                    print(" ║              ¡BUEN VIAJE!                ║")
                    print(" ╚══════════════════════════════════════════╝")
                else:
                    print("\n ----------------------------------------------")
                    print(" [ INFO ] Operación cancelada. No se cobró nada.")
                    print(" ----------------------------------------------")
                
                input("\nPresione [ENTER] para volver al menú...")
                break # Termina el proceso de compra exitoso o cancelado
            
        elif opcion == "3":
                
            # Usamos la función con reduce() que armamos en finanzas
            total_caja = calcular_recaudacion_total(ventas_diarias)
            cantidad_pasajes = len(ventas_diarias)
            
            print("\n ╔════════════════════════════════════════════╗")
            print(" ║          REPORTE DE CAJA DIARIA            ║")
            print(" ╚════════════════════════════════════════════╝\n")
            
            print(" [ CALCULANDO VENTAS REGISTRADAS... ]\n")
            
            print(" ----------------------------------------------")
            print("   RESUMEN DEL DÍA:")
            print(" ----------------------------------------------")
            print(f" > Pasajes vendidos: {cantidad_pasajes:02d}")
            print(f" > Recaudación total: $ {total_caja:.2f}")
            print(" ----------------------------------------------\n")
            
            # Armamos el texto del total y lo rellenamos para que la caja no se deforme
            texto_caja = f"TOTAL CAJA:      $ {total_caja:.2f}"
            
            print("        ╔══════════════════════════════╗")
            print(f"        ║ {texto_caja:<28} ║")
            print("        ╚══════════════════════════════╝\n")
            
            input(" Presione [ENTER] para volver al menú...")
            
            
        elif opcion == "4":
            print("\n ----------------------------------------------")
            print("    Cerrando sistema... ¡Hasta luego!")
            print(" ----------------------------------------------\n")
            print(" ╔════════════════════════════════════════════╗")
            print(" ║        GRACIAS POR USAR NEXUS VIAJES       ║")
            print(" ║          SISTEMA FINALIZADO - 2026         ║")
            print(" ╚════════════════════════════════════════════╝\n")
            print(" Proceso finalizado.")
            break
            
        else:
            print("\nOpción no válida.")



if __name__ == "__main__":
    main()

