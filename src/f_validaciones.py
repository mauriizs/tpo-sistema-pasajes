import re

def validar_fecha(fecha_ingresada):

    """
    Valida la fecha ingresada por el usuario.
    Asegura que el formato sea DD/MM y que el día y mes sean válidos.
    """

    dias_maximos = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    while True:
        # RegEx: Formato DD/MM, donde DD es 01-31 y MM es 01-12
        if re.match(r'^\d{2}/\d{2}$', fecha_ingresada): 
            dia, mes = map(int, fecha_ingresada.split('/'))
            
            if 1 <= mes <= 12:
                if 1 <= dia <= dias_maximos[mes - 1]:
                    return fecha_ingresada
                
        print("\n ------------------------------------------------------")
        print(" [ ERROR ] Fecha inválida. Ingresela en formato DD/MM. ")
        print(" ------------------------------------------------------\n")
        fecha_ingresada = input("> Ingrese la fecha del viaje (DD/MM): ")


def validar_dni(dni_ingresado):

    """
    Valida el DNI ingresado por el usuario.
    Asegura que el DNI contenga solo números y tenga entre 7 y 8 dígitos.
    """

    while True:
        # RegEx: Exactamente entre 7 y 8 dígitos numéricos
        if re.match(r'^\d{7,8}$', dni_ingresado): 
            return dni_ingresado
        print("\n ------------------------------------------------------")
        print(" [ ERROR ] El DNI debe contener 7 u 8 dígitos. ")
        print(" ------------------------------------------------------\n")
        dni_ingresado = input("> Ingrese su DNI (sin puntos): ")


def validar_email(email_ingresado):

    """
    Valida el email ingresado por el usuario.
    Asegura que el email tenga un formato básico de email@dominio.com
    """
    
    while True:
        # RegEx: Formato basico de email texto@texto.texto
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_ingresado): 
            return email_ingresado
        print("\n ------------------------------------------------------")
        print(" [ ERROR ] Formato de email inválido. ")
        print(" ------------------------------------------------------\n")
        email_ingresado = input("> Ingrese su Email: ")

 
def validar_telefono(tel_ingresado):

    """
    Valida el teléfono ingresado por el usuario.
    Asegura que el teléfono contenga solo números y tenga entre 8 y 15 dígitos.
    """

    while True:
        # RegEx: Solo números, entre 8 y 15 dígitos
        if re.match(r'^\d{8,15}$', tel_ingresado): 
            return tel_ingresado
        print("\n ------------------------------------------------------")
        print(" [ ERROR ] Teléfono inválido (solo números). ")
        print(" ------------------------------------------------------\n")
        tel_ingresado = input("> Ingrese su Teléfono: ")