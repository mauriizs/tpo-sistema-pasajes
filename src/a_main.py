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
from f_validaciones import validar_dni, validar_opcion
from c_micro import mostrar_asientos, reservar_lugar
from d_busquedas import catalogo_viajes, buscar_viajes
from e_finanzas import calcular_recaudacion

def main():
    print("--- SISTEMA DE VENTA DE PASAJES ---")
    while True:
        print("\n1. Buscar Viaje")
        print("2. Comprar Pasaje")
        print("3. Ver Recaudación Total")
        print("4. Salir")
        
        opcion = input("Elegí una opción: ")
        
        if opcion == "1":
            print("Llamar a busquedas...")
        elif opcion == "2":
            print("Llamar a validaciones, micro y finanzas...")
        elif opcion == "3":
            print("Llamar a finanzas...")
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()