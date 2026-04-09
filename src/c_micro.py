# ============================
# MÓDULO DEL MAPA DE ASIENTOS
# ============================

def mostrar_micro(matriz_micro):
    
    '''Recibe la lista de listas del viaje seleccionado y la imprime con el formato visual de consola.'''

    print("\n        ╔══════════════════════════════════════╗")
    print("        ║            MAPA DE ASIENTOS          ║")
    print("        ╚══════════════════════════════════════╝\n")
    print("           [ COL 1 ] [ COL 2 ]     [ COL 3 ] [ COL 4 ]")
    print("          ┌─────────┬─────────┐   ┌─────────┬─────────┐")

    # Usamos enumerate para saber en qué número de fila estamos (1, 2 o 3)
    for indice, fila in enumerate(matriz_micro):
        num_fila = indice + 1
        
        # Desarmamos la fila en 4 variables para que sea fácil imprimir
        c1, c2, c3, c4 = fila[0], fila[1], fila[2], fila[3]
        
        print(f"  FILA {num_fila}: │    {c1}    │    {c2}    │   │    {c3}    │    {c4}    │")
        
        # Si NO es la última fila, imprimimos los separadores del medio
        if num_fila < len(matriz_micro):
            print("          ├─────────┼─────────┤   ├─────────┼─────────┤")
        # Si ES la última fila, imprimimos el borde de abajo
        else:
            print("          └─────────┴─────────┘   └─────────┴─────────┘")
            
    print("        ----------------------------------------")
    print("               (L = LIBRE  |  O = OCUPADO)\n")




def asiento_esta_libre(matriz_micro, fila, columna):

    '''Solo VERIFICA si está libre (Retorna True o False)'''
    
    return matriz_micro[fila - 1][columna - 1] == "L"


def reservar_asiento(matriz_micro, fila, columna):
    
    '''OCUPA definitivamente el asiento (Cambia L por O)'''
    
    matriz_micro[fila - 1][columna - 1] = "O"

