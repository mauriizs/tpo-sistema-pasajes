datosagencia = ["""CENTRAL DE PASAJES DE MICRO""", """LEGAJO - 115758""", """AV. RAMOS MEJIA 1560""", """TEL: 11-6824-8705""",
                """MAIL:centraldemicro10@gmail.com"""]
for i in range(len(datosagencia)):
    print(datosagencia[i])
        
print("""\nDESTINOS Y PUNTO DE PARTIDA DISPONIBLES:""")
datosdestinos=["""BARILOCHE""","""MAR DEL PLATA""","""MISIONES""", """BUENOS AIRES"""]
datosdestinos.sort()
for i in range(len(datosdestinos)):
    print(datosdestinos[i])