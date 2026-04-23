# ==========================================
# 1. BASE DE DATOS EN MEMORIA (El Catálogo)
# ==========================================

# Estructura de cada viaje (Lista anidada).
# indices: [0]ID, [1]Empresa, [2]Origen, [3]Destino, [4]Fecha, [5]Precio, [6]Matriz de Asientos

catalogo_viajes = [
    [
        "1", 
        "Via Bariloche", 
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
        "Andesmar", 
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
        "Crucero Norte", 
        "Cordoba", 
        "Misiones", 
        "30/05", 
        45000.0, 
        [
            ["O", "O", "O", "O"], 
            ["O", "L", "O", "O"],
            ["O", "O", "O", "O"]
        ]
    ],
    [
        "4", 
        "Crucero Norte", 
        "Mendoza", 
        "Buenos Aires", 
        "05/06", 
        42000.0, 
        [
            ["O", "O", "O", "O"], 
            ["O", "O", "O", "O"],
            ["O", "O", "O", "L"]
        ]
    ],
    [
        "5", 
        "Via Bariloche", 
        "Salta", 
        "Cordoba", 
        "10/06", 
        55000.0, 
        [
            ["O", "O", "L", "O"], 
            ["O", "O", "O", "O"],
            ["O", "O", "L", "O"]
        ]
    ],
    [
        "6",
        "Chevallier",
        "Rosario",
        "Buenos Aires",
        "12/06",
        25000.0, 
        [
            ["L", "O", "L", "O"], 
            ["L", "L", "O", "O"], 
            ["L", "L", "L", "L"]
        ]
    ],
    [
        "7", 
        "Flechabus", 
        "Tucuman", 
        "Salta", 
        "15/06", 
        28000.0, 
        [
            ["O", "O", "O", "L"], 
            ["L", "O", "O", "L"], 
            ["O", "O", "O", "O"]
        ]

    ],
    [
        "8", 
        "Andesmar", 
        "Mendoza", 
        "Bariloche", 
        "20/06", 
        65000.0, 
        [
            ["L", "L", "O", "O"], 
            ["L", "L", "L", "L"], 
            ["O", "L", "L", "O"]
        ]
    ],
    [
        "9", 
        "Chevallier", 
        "Buenos Aires", 
        "Rosario", 
        "22/06", 
        25000.0, 
        [
            ["L", "L", "L", "L"], 
            ["L", "L", "L", "L"], 
            ["L", "L", "L", "L"]
        ]
    ],
    [
        "10", 
        "Urquiza", 
        "Cordoba", 
        "Tucuman", 
        "25/06", 
        32000.0, 
        [
            ["O", "O", "L", "L"], 
            ["O", "O", "L", "L"], 
            ["O", "O", "L", "L"]
        ]
    ],
    [
        "11", 
        "Plusmar", 
        "Buenos Aires", 
        "Santa Cruz", 
        "22/04", 
        100000.0, 
        [
            ["O", "O", "O", "O"], 
            ["O", "O", "O", "L"], 
            ["O", "O", "O", "O"]
        ]
    ]

]

# ==================================================
# 2. FUNCIONES DE BÚSQUEDA (Programación Funcional)
# ==================================================

def buscar_viajes(origen_buscado, destino_buscado, fecha_buscada):

    '''Filtra el catálogo buscando coincidencias exactas de origen, destino y fecha. Retorna una lista con los viajes encontrados.'''
    
    viajes_filtrados = list(filter(
        lambda viaje: viaje[2].lower() == origen_buscado.lower() and 
                      viaje[3].lower() == destino_buscado.lower() and 
                      viaje[4] == fecha_buscada, 
        catalogo_viajes
    ))
    
    return viajes_filtrados

    # 1. Usamos filter con una funcion lambda que revisa los índices [1], [2] y [3]
    # 2. Convertimos a minúsculas (.lower()) para evitar errores si el usuario escribe "bariloche" o "BARILOCHE"


def buscar_por_id(id_viaje):  
    
    '''Busca un viaje específico por su ID'''

    viaje_encontrado = filter(lambda viaje: viaje[0] == id_viaje, catalogo_viajes) 
    resultados = list(viaje_encontrado)

    if len(resultados) > 0: 
        return resultados[0]
    else:
        return None
    
    # 1. Primero filtramos el catálogo por ID, luego convertimos el resultado a lista para verificar si encontramos algo. 
    # 2. Si la lista tiene elementos, devolvemos el primero (único) resultado. Si no encontramos nada, devolvemos None para indicar que no existe ese ID.

