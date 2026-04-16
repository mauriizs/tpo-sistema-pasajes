import re

def validar_fecha(fecha_ingresada):
    dias_maximos = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    while True:
        # RegEx: Formato DD/MM, donde DD es 01-31 y MM es 01-12
        if re.match(r'^\d{2}/\d{2}$', fecha_ingresada): 
            dia, mes = map(int, fecha_ingresada.split('/'))
            
            if 1 <= mes <= 12:
                if 1 <= dia <= dias_maximos[mes - 1]:
                    return fecha_ingresada
                
        print("\n ------------------------------------------------------")
        print(" [ ERROR ] Fecha no válida. Ingresá en formato DD/MM. ")
        print(" ------------------------------------------------------\n")
        fecha_ingresada = input("> Ingresá la fecha del viaje (DD/MM): ")

def validar_dni(dni_ingresado):
    while True:
        # RegEx: Exactamente entre 7 y 8 dígitos numéricos
        if re.match(r'^\d{7,8}$', dni_ingresado): 
            return dni_ingresado
        print("\n ------------------------------------------------------")
        print(" [ ERROR ] El DNI debe contener solo números. ")
        print(" ------------------------------------------------------\n")
        dni_ingresado = input("> Ingresá tu DNI (sin puntos): ")


def validar_email(email_ingresado):
    while True:
        # RegEx: Formato basico de email texto@texto.texto
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_ingresado): 
            return email_ingresado
        print("\n ------------------------------------------------------")
        print(" [ ERROR ] Formato de email no válido. ")
        print(" ------------------------------------------------------\n")
        email_ingresado = input("> Ingresá tu Email: ")

def validar_telefono(tel_ingresado):
    while True:
        # RegEx: Solo números, entre 8 y 15 dígitos
        if re.match(r'^\d{8,15}$', tel_ingresado): 
            return tel_ingresado
        print("\n ------------------------------------------------------")
        print(" [ ERROR ] Teléfono no válido (solo números). ")
        print(" ------------------------------------------------------\n")
        tel_ingresado = input("> Ingresá tu Teléfono: ")
