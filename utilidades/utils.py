import random
import os
from data.JSONs    import leer_archivo
from config.config import PATH_USUARIOS
 
def generate_ID():
    """
    generate_ID genera un ID random a cada usuario registrado
 
    Returns:
        int: un numero random [1000-9999]
    """
    usuarios = leer_archivo(PATH_USUARIOS)
    id = random.randint(1000,10000)
    idUsuarios = [user["id"] for user in usuarios]
    while True:
        if id in idUsuarios:
            id = random.randint(1000,10000)
        else:
            return id

def pedir_entero(mensaje, minimo=None, maximo=None):
    """
    Pide un número entero al usuario y valida:
    - Que no sea vacío
    - Que sea entero
    - Que esté dentro de un rango opcional

    Devuelve el entero válido.
    """
    while True:
        try:
            entrada = input(mensaje).strip()

            if entrada == "":
                print("ERROR: No puede estar vacío.\n")
                continue

            if not entrada.isdigit():
                print("ERROR: Debe ingresar un número entero o mayor a 0.\n")
                continue

            numero = int(entrada)

            if minimo is not None and numero < minimo:
                print(f"ERROR: Debe ser un número mayor o igual a {minimo}.\n")
                continue

            if maximo is not None and numero > maximo:
                print(f"ERROR: Debe ser un número menor o igual a {maximo}.\n")
                continue

            return numero
        except Exception as e:
            print(f"Error: {e}.")

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')