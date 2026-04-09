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
from f_validaciones import validar_fecha, validar_dni, validar_opcion
from c_micro import mostrar_asientos, reservar_lugar
from d_busquedas import catalogo_viajes, buscar_viajes
from e_finanzas import calcular_recaudacion

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
            print("\nLlamar a validaciones, micro y finanzas...")
            
        elif opcion == "3":
            print("\nLlamar a finanzas...")
            
        elif opcion == "4":
            print("\nCerrando sistema. ¡Hasta luego!")
            break
            
        else:
            print("\nOpción no válida.")



if __name__ == "__main__":
    main()

