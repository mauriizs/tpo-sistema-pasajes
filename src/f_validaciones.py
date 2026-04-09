import re

def validar_fecha(fecha_ingresada): # Valida que la fecha tenga el formato dd/mm y que los valores sean válidos.
    while True:
        if re.match(r'^\d{2}/\d{2}$', fecha_ingresada):
            dia, mes = map(int, fecha_ingresada.split('/'))
            if 1 <= dia <= 31 and 1 <= mes <= 12:
                return fecha_ingresada
        print("Fecha no válida. Ingresá en formato DD/MM.")
        fecha_ingresada = input("> Ingresá la fecha del viaje (DD/MM): ")

def validar_dni(dni_ingresado):
    while True:
        # RegEx: Exactamente entre 7 y 8 dígitos numéricos
        if re.match(r'^\d{7,8}$', dni_ingresado):
            return dni_ingresado
        print("[ERROR] El DNI debe contener solo números (7 u 8 dígitos).")
        dni_ingresado = input("> Ingresá tu DNI (sin puntos): ")

def validar_email(email_ingresado):
    while True:
        # RegEx: Formato basico de email texto@texto.texto
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_ingresado):
            return email_ingresado
        print("[ERROR] Formato de email no válido.")
        email_ingresado = input("> Ingresá tu Email: ")

def validar_telefono(tel_ingresado):
    while True:
        # RegEx: Solo números, entre 8 y 15 dígitos
        if re.match(r'^\d{8,15}$', tel_ingresado):
            return tel_ingresado
        print("[ERROR] Teléfono no válido (solo números).")
        tel_ingresado = input("> Ingresá tu Teléfono: ")
