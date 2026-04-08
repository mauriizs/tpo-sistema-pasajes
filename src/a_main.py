# estructura del trabajo.
# tpo-sistema-pasajes/
# │-- .gitignore
# │-- README.md
# └── src/                    <-- La carpeta principal de código
#     │-- main.py             (Menú principal - Integrante 1)
#     │-- validaciones.py     (RegEx - Integrante 2)
#     │-- micro.py            (Matriz y asientos - Integrante 3)
#     │-- busquedas.py        (Filter y catálogo - Integrante 4)
#     └── finanzas.py         (Map, reduce y cálculos - Integrante 5)


from b_info import catalogo_viajes
from f_validaciones import validar_dni, validar_opcion
from c_micro import mostrar_asientos, reservar_lugar
from d_busquedas import buscar_viaje
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