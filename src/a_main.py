# estructura del trabajo.
# tpo-sistema-pasajes/
# ├── docs/                   <-- Acá irá el PDF con la documentación final
# ├── src/                    <-- Carpeta de código fuente
# │   ├── a_main.py             (El Menú principal que une todo el programa)
# │   ├── b_info.py             (Muestra los datos y bienvenida de la agencia)
# │   ├── c_busquedas.py        (Tiene el catálogo de viajes y usa 'filter')
# │   ├── d_micro.py            (Crea, muestra y modifica la matriz de asientos)
# │   ├── e_validaciones.py     (Funciones con RegEx para validar DNI, fecha, email)
# │   └── f_finanzas.py         (Cálculos de precios usando 'map' y 'reduce')
# ├── anotaciones.md          <-- Notas temporales de desarrollo
# └── instrucciones.md        <-- Guía de uso del sistema


from b_info import mostrar_bienvenida
from c_micro import mostrar_micro, asiento_esta_libre, reservar_asiento
from d_busquedas import catalogo_viajes, buscar_viajes, buscar_por_id
from e_finanzas import aplicar_recargo, calcular_recaudacion_total
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
            
            origen = input("> Ingresá el origen: ")
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
            id_buscado = input("> Ingresá el ID del viaje deseado: ")
            viaje = buscar_por_id(id_buscado) # Función de d_busquedas
            
            # Caso Borde: ID Inexistente
            if not viaje:
                print("\n[ERROR] El ID ingresado no existe en el catálogo. Operación cancelada.")
                input("Presione [ENTER] para volver al menú...")
                continue # Vuelve al Menú Principal
                
            empresa, destino, fecha, precio_base, matriz = viaje[1], viaje[3], viaje[4], viaje[5], viaje[6]
            print(f"\nHas seleccionado: {destino} - {fecha} ({empresa})")
            
            # PASO B: Mapa de Asientos
            while True:
                mostrar_micro(matriz)
                
                fila_input = input("> Ingresá la fila (1-3) o '0' para cancelar: ")
                if fila_input == "0":
                    print("\n[INFO] Operación cancelada por el usuario.")
                    break # Sale del bucle de compra y vuelve al menú
                    
                col_input = input("> Ingresá la columna (1-4) o '0' para cancelar: ")
                if col_input == "0":
                    print("\n[INFO] Operación cancelada por el usuario.")
                    break
                    
                # Caso Borde: Validar que tipeó números y no letras
                if not (fila_input.isdigit() and col_input.isdigit()):
                    print("\n[ERROR] Debes ingresar números válidos.")
                    continue
                    
                fila = int(fila_input)
                columna = int(col_input)
                
                # Caso Borde: Asiento fuera de rango (1 a 3 filas, 1 a 4 columnas)
                if not (1 <= fila <= 3 and 1 <= columna <= 4):
                    print("\n[ERROR] Coordenadas fuera de rango. El micro tiene 3 filas y 4 columnas.")
                    continue
                
                # DIAGRAMA: ¿Asiento Libre?
                if not asiento_esta_libre(matriz, fila, columna):
                    print("\n[ERROR] El asiento seleccionado ya está ocupado. Elegí otro.")
                    continue # Vuelve a mostrar el mapa
                    
                print("\n------------------------------------------------------")
                print("> [ OK ] Asiento disponible. Iniciando Check-in...")
                print("------------------------------------------------------")
                
                # PASO C: Registro de Pasajeros (Validar con RegEx)
                print("\nDATOS DEL PASAJERO")
                dni_input = input("> Ingresá tu DNI (sin puntos): ")
                dni = validar_dni(dni_input)
                
                email_input = input("> Ingresá tu Email: ")
                email = validar_email(email_input)
                
                tel_input = input("> Ingresá tu Teléfono: ")
                tel = validar_telefono(tel_input)
                
                print("\n[ PROCESANDO DATOS... POR FAVOR ESPERE ]")
                
                # PASO D: Liquidación y Emisión (Calcular recargo con map)
                precio_final = aplicar_recargo(precio_base)
                
                print("\nRESUMEN DE COMPRA")
                print(f"Pasajero: DNI {dni}")
                print(f"Destino: {destino} | Fecha: {fecha}")
                print(f"Asiento: Fila {fila}, Columna {columna}")
                print(f"Precio Base: $ {precio_base:.2f}")
                print(f"Cargo por servicio (16%): $ {precio_final - precio_base:.2f}")
                print(f"TOTAL A PAGAR: $ {precio_final:.2f}")
                
                # DIAGRAMA: ¿Confirmar Compra?
                confirmacion = input("\n> ¿Confirmar pago y emitir pasaje? (S/N): ").upper()
                
                if confirmacion == "S":
                    # Actualizar Matriz (L -> O)
                    reservar_asiento(matriz, fila, columna)
                    
                    # Guardar Venta en Memoria
                    from e_finanzas import ventas_diarias
                    ventas_diarias.append(precio_final)
                    
                    # Emitir Ticket
                    print("\nPAGO EXITOSO. Generando pasaje...")
                    print("========================================")
                    print("     TICKET DE VIAJE CENTRAL MICRO      ")
                    print("========================================")
                    print(f" TITULAR DNI: {dni}")
                    print(f" DESTINO: {destino} | FECHA: {fecha}")
                    print(f" ASIENTO: Fila {fila} Columna {columna}")
                    print(f" TOTAL: $ {precio_final:.2f}")
                    print("========================================")
                    print("              ¡BUEN VIAJE!              ")
                else:
                    print("\n[INFO] Operación cancelada. No se realizó ningún cargo.")
                
                input("\nPresione [ENTER] para volver al menú...")
                break # Termina el proceso de compra exitoso o cancelado
            
        elif opcion == "3":
            print("\nLlamar a finanzas...")
            
        elif opcion == "4":
            print("\nCerrando sistema. ¡Hasta luego!")
            break
            
        else:
            print("\nOpción no válida.")



if __name__ == "__main__":
    main()

