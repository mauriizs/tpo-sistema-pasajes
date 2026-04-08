import re

def validar_fecha(fecha_ingresada): # Valida que la fecha tenga el formato dd/mm y que los valores sean válidos.  
    
    if re.match(r'^\d{2}/\d{2}$', fecha_ingresada):
        dia, mes = map(int, fecha_ingresada.split('/'))
        if 1 <= dia <= 31 and 1 <= mes <= 12:
            return True




def validar_dni(dni):
    # TODO: Usar re.match() para validar que sean números
    pass

def validar_email(email):
    # TODO: Usar re.match() para validar el formato correo@dominio.com
    pass

def validar_fecha(fecha):
    # TODO: Usar re.match() para validar el formato dd/mm/yyyy
    pass

