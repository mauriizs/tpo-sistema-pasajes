from functools import reduce

# Lista global donde se guardará la plata de cada pasaje vendido
ventas_diarias = []

def aplicar_recargo(precio_base):
    
    precio_con_recargo = list(map(lambda p: p * 1.16, [precio_base]))
    return precio_con_recargo[0]

    #1. Usamos map para aplicar un recargo del 16% a cada precio en la lista (en este caso, solo hay uno). 
    #2. Luego devolvemos el primer elemento de la lista resultante, que es el precio con recargo.
    

def calcular_recaudacion_total(lista_ventas):

    if len(lista_ventas) == 0:
        return 0.0
    
    return reduce(lambda a, b: a + b, lista_ventas)

    #1. Si la lista de ventas está vacía, no hay nada que sumar, así que devolvemos 0.0 para indicar que no se recaudó nada.
    #2. Usamos reduce para sumar todos los elementos de la lista de ventas, lo que nos da el total recaudado. 
    #3. La función lambda toma dos argumentos (a y b) y devuelve su suma, y reduce() aplica esta función acumulativamente a los elementos de la lista.