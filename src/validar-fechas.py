
def validar_fecha():
    """Hace toda las invalidaciones posibles de una fecha hasta la actual
    si el cliente elige solo ida y retorna la fecha"""
    print("""FECHA DE PARTIDA""")
    dia=int(input("""dia?"""))
    mes=int(input("""mes?"""))
    anio=int(input("""año?"""))
    cdia=0
    if mes in [1,3,5,7,8,10,12]:
        cdia=31
    elif mes in [4,6,9,11]:
        cdia=30
    elif mes==2:
        if anio%4==0 and anio%100!=0 or anio%400==0:
            cdia=29
        else:
            cdia=28
            
    while dia<=0 or dia>cdia or (anio<=2026 and mes<4) or (anio==2026 and mes==4 and dia<24) or mes<=0 or mes>10 or anio<2026:
        print("""FECHA INVALIDA""")
        dia=int(input("""dia? """))
        mes=int(input("""mes? """))
        anio=int(input("""año? """))
        cdia=0
        if mes in [1,3,5,7,8,10,12]:
            cdia=31
        elif mes in [4,6,9,11]:
            cdia=30
        elif mes==2:
            if anio%4==0 and anio%100!=0 or anio%400==0:
                cdia=29
            else:
                cdia=28
    return dia, mes, anio

dia,mes,anio=validar_fecha()

print(dia, mes, anio)
    