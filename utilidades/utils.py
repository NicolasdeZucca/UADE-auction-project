import random
import os
from datetime import datetime
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

# cambiar estado de la subasta segun TIEMPO
def actualizar_estado_por_tiempo(subasta):
    """
    Cambia estado de una subasta a 'finalizada' si ya pasó su fecha_fin.
    Devuelve True si cambió algo, False si no.
    """

    if subasta["estado"] != "activa":
        return False

    ahora = datetime.now()
    fecha_fin = datetime.fromisoformat(subasta["fecha_fin"])

    if ahora >= fecha_fin:
        subasta["estado"] = "finalizada"
        return True

    return False


def calcular_tiempo_restante(subasta):
    """
    Devuelve el tiempo restante en formato MM:SS.
    Si ya venció, devuelve "00:00".
    """

    fecha_fin = datetime.fromisoformat(subasta["fecha_fin"])
    ahora = datetime.now()

    restante_seg = int((fecha_fin - ahora).total_seconds())

    # Si ya venció
    if restante_seg <= 0:
        return "00:00"

    minutos = restante_seg // 60
    segundos = restante_seg % 60

    return f"{minutos:02d}:{segundos:02d} minutos"

