import json
import os
from functools import reduce
from datetime import datetime
import re
from datetime import datetime

# archivos
from validaciones.validaciones import validarNombreContrasena, usuarioExiste, validarCredenciales, validarIDSubasta
from utilidades.utils import generateID, leer_archivo, escribir_archivo

# --- Rutas de archivos (en la misma carpeta que este .py) ---
USUARIO_ACTUAL = None
PATH_USUARIOS = "usuarios.json"
PATH_SUBASTAS = "subastas.json"
PATH_PUJAS = "pujas.json"

# Funciones de usuarios
def registrar_usuario(nombre, password):
    """
    Agrega / registra el nombre de usuario en 'usuarios.json' si no existe

    Args:
        nombre (str): nombre de usuario
        password (str): contraseña del usuario

    Returns:
        boolean, str: True si el usuario fue cargado + msj. 
                      False si hubo errores + msj de error.
    """
    global USUARIO_ACTUAL

    ok, msj, nombre_valido, password_valida = validarNombreContrasena(nombre, password)
    
    if not ok:
        return (False, msj)

    try:
        
        usuarios = leer_archivo(PATH_USUARIOS)
        if usuarioExiste(nombre_valido, usuarios):
            return

        
        nuevo = {
            "id": generateID(),
            "nombre": nombre_valido,
            "password": password_valida
        }

        usuarios.append(nuevo)
        escribir_archivo(PATH_USUARIOS, usuarios)
        USUARIO_ACTUAL = nuevo
        return (True, print(f"Usuario '{nombre_valido}' registrado (ID: {nuevo['id']}).\n"))
    
    except Exception as e:
        return (False, print("Error en registrar usuario: ", e))


def login(nombre, password):
    """
    Funcion de login de usuarios.

    Returns:
        boolean, str: True  + el usuario logueado
                      False + mensaje de error
    """
    global USUARIO_ACTUAL

    if USUARIO_ACTUAL:
        return True, print(f"Se encuentra logueado el usuario {USUARIO_ACTUAL['nombre']}")

    usuarios = leer_archivo(PATH_USUARIOS)
    ok, user = validarCredenciales(nombre, password, usuarios)
    if ok:
        USUARIO_ACTUAL = user
        return (True, f"Usuario {user['nombre']}logueado")
    
    
    return False, print("Usuario o contraseña incorrectos.")


def obtener_archivo(path):
    """
    retorna los datos de un archivo.
    Si la ruta no existe, retorna '[]'
    """
    archivo = leer_archivo(path)
    if not isinstance(archivo, list):
        return []

    return archivo


# def obtener_subastas(path):
#     """
#     Muestra los nombres de las subastas disponibles
#     """
#     subastas_activas = []
#     subastas = leer_archivo(path)
#     if not isinstance(subastas, list):
#         return []

#     for sub in subastas:
#         subastas_activas.append(
#             {sub.get('nombre'), sub.get('id'), sub.get('costo_inicial')})

#     print(subastas_activas)
#     print("Si desea participar de alguna subasta elija la opcion numero 4 en el menu principal\n")
#     return subastas_activas


def listar_subastas():
    """
    listar_subastas muestra ID, nombre y costo inicial de cada subasta disponible
    y las muestra por pantalla

    Returns:
        list: lista de subastas
    """
    subastas = leer_archivo(PATH_SUBASTAS)
    
    if not subastas:
        print("No hay subastas disponibles. \n")
        return []

    print("\nSubastas disponibles:")
    for sub in subastas:
        print("-------------------------------------------")
        print(f"Subasta ID: {sub.get('id')}")
        print(f"Nombre: {sub.get('nombre')}")
        print(f"Costo inicial: {sub.get('costo_inicial')}")
        print("-------------------------------------------")
        print()

    return subastas


def elegir_subasta():
    """
    elegir_subasta Pide al usuario un ID de subasta y devuelve la subasta elegida.
    Si elige algo inválido, vuelve a pedir.

    Args:
        subastas (list): lista de subastas existentes.
    """
    subastas = leer_archivo(PATH_SUBASTAS)

    while True:
        try:
            id_seleccionado = int(input("Elija el ID de la subasta : "))

        except ValueError:
            print("Por favor ingrese un numero.\n")
            return

        ok, resultado = validarIDSubasta(id_seleccionado, subastas)
        if not ok:
            print(resultado)
            continue

        return resultado


def registrar_puja():
    """
    funcion que registra una puja en una subasta
    Parametros: el usuario que realiza la puja, el monto que quiere realizar
    return (boolean, mensaje).
    """
    #TODO: revisar si funciona - incompleta
    # El usuario debe existir
    global USUARIO_ACTUAL

    if not USUARIO_ACTUAL:
        return False, print("Registrarse o logueese para participar de una subasta \n")

    subastas = listar_subastas()
    if not subastas:
        return (False, "No hay subastas disponibles en este momento.")

    subastaElegida = elegir_subasta()
    subastaID = subastaElegida.get("id")

    # El monto debe ser numerico y positivo
    try:
        monto = float(input("Ingrese un monto a ofertar: "))
        while monto < subastaElegida["costo_inicial"]:
            print("El monto debe ser mayor al precio inicial.")
            monto = float(input("Ingrese un monto a ofertar nuevamente: "))

    except ValueError:
        return (False, "El monto debe ser numerico.")

    pujas = leer_archivo(PATH_PUJAS)
    pujas_de_esa_subasta = list(filter(
        lambda p: isinstance(p, dict) and p.get("subasta_id") == subastaID,
        pujas
    ))

    # Determinar la puja maxima actual
    if pujas_de_esa_subasta:
        puja_maxima_existente = reduce(
            lambda acc, p: acc if acc["monto"] >= p["monto"] else p,
            pujas_de_esa_subasta
        )
        monto_actual_maximo = puja_maxima_existente["monto"]
    else:
        # si no hubo pujas, el mínimo aceptable es el costo_inicial de la subasta
        monto_actual_maximo = subastaElegida.get("costo_inicial", 0)

    if monto <= monto_actual_maximo:
        return (
            False,
            f"Tu oferta debe superar la puja actual ({monto_actual_maximo})."
        )

    # 6. Registrar nueva puja
    nueva_puja = {
        "usuario": USUARIO_ACTUAL["nombre"],
        "monto": monto,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "subasta_id": subastaID
    }

    pujas.append(nueva_puja)
    ok_write = escribir_archivo(PATH_PUJAS, pujas)
    if not ok_write:
        return (False, "Error al guardar la puja en disco.")

    return (True, f"Puja registrada: {USUARIO_ACTUAL['nombre']} ofertó {monto}.")

# Funcion main principal

def main():
    while True:
        print("Bienvenido a subastas.com")
        print(
           f"Usuario logueado: {USUARIO_ACTUAL['nombre'] if USUARIO_ACTUAL else 'nadie inició sesión aún'}")
        print("1- Registrarse")
        print("2- Iniciar sesion")
        print("3- Ver subastastas disponibles")
        print("4- Registrar puja")
        print("5- Salir")
        opcion = int(input("Elija una opción: "))
        print("")
        while opcion < 1 or opcion > 5:
            opcion = int(input("Elija una opción válida (1-5): "))

        if opcion == 1:
            nombre = input("Ingrese un nombre de usuario: ")
            password = input("Ingrese una contraseña: ")
            registrar_usuario(nombre, password)

        elif opcion == 2:
            nombre = input("Ingrese su nombre de usuario: ")
            password = input("Ingrese su contraseña: ")
            login(nombre, password)

        elif opcion == 3:
            listar_subastas()
        elif opcion == 4:
            registrar_puja()
        elif opcion == 5:
            break
        else:
            if not isinstance(opcion, int):
                print("Error, debe ingresar un dato numerico válido")
                opcion = int(input("Elija una opción válida (1-5): "))


main()
