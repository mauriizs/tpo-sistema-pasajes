# ==========================================
# MÓDULO DE BÚSQUEDAS Y CATÁLOGO
# ==========================================

# Base de datos temporal (Lista de Listas)

# Índices: [0]ID, [1]Origen, [2]Destino, [3]Fecha, [4]Precio, [5]Matriz de Asientos

catalogo_viajes = [
    [
        "1", 
        "Buenos Aires", 
        "Bariloche", 
        "20/05", 
        50000.0, 
        [
            ["L", "L", "L", "L"],
            ["L", "O", "L", "L"],
            ["O", "O", "L", "L"]
        ]
    ],
    [
        "2", 
        "Buenos Aires", 
        "Mar del Plata", 
        "25/05", 
        35000.0, 
        [
            ["L", "L", "L", "L"],
            ["L", "L", "L", "L"],
            ["L", "L", "L", "L"]
        ]
    ],
    [
        "3", 
        "Cordoba", 
        "Misiones", 
        "30/05", 
        45000.0, 
        [
            ["O", "O", "O", "O"],  # Ejemplo de micro casi lleno
            ["O", "L", "O", "O"],
            ["O", "O", "O", "O"]
        ]
    ]
]

def buscar_viajes(origen_buscado, destino_buscado, fecha_buscada):
    """
    Filtra el catálogo buscando coincidencias exactas de origen, destino y fecha.
    Retorna una lista con los viajes encontrados.
    """
    # Explicación: Usamos filter con una lambda que revisa los índices [1], [2] y [3]
    # convertimos a minúsculas (.lower()) para evitar errores si el usuario escribe "bariloche" o "BARILOCHE"
    
    viajes_filtrados = list(filter(
        lambda viaje: viaje[1].lower() == origen_buscado.lower() and 
                      viaje[2].lower() == destino_buscado.lower() and 
                      viaje[3] == fecha_buscada, 
        catalogo_viajes
    ))
    
    return viajes_filtrados