def mostrar_bienvenida():
    datosagencia = [
        "CENTRAL DE PASAJES DE MICRO", 
        "LEGAJO - 115758", 
        "AV. RAMOS MEJIA 1560", 
        "TEL: 11-6824-8705", 
        "MAIL:centraldemicro10@gmail.com"
    ]
    
    for dato in datosagencia:
        print(dato)
        
    print("\nDESTINOS Y PUNTO DE PARTIDA DISPONIBLES:")
    datosdestinos = ["BARILOCHE", "MAR DEL PLATA", "MISIONES", "BUENOS AIRES"]
    datosdestinos.sort()
    
    for destino in datosdestinos:
        print(destino)
