import json
import os
from datetime import datetime

# --- Rutas de archivos (en la misma carpeta que este .py) ---
USUARIO_ACTUAL = None
PATH_USUARIOS = "usuarios.json"
PATH_SUBASTAS = "subastas.json"
PATH_PUJAS = "pujas.json"

__MEMORY__ = {
    PATH_USUARIOS: [{'id': 1, 'nombre': 'admin', 'password': '123'},
                    {'id': 2, 'nombre': 'Nico', 'password': '123'},
                    {'id': 3, 'nombre': 'Pepe', 'password': '456'},
                    {'id': 4, 'nombre': 'Sofia', 'password': '789'},
                    {'id': 5, 'nombre': 'Andrea', 'password': '9999'}],
    PATH_SUBASTAS: [{'categoria': 'Automotores',
                     'costo_inicial': 12000000,
                     'descripcion': 'Polemico pero confiable',
                     'estado': 'activa',
                     'ganador': None,
                     'id': 1,
                     'monto_actual': 0,
                     'nombre': 'Bora 1.8T',
                     'tiempo_restante': 300},
                    {'categoria': 'Arte',
                     'costo_inicial': 100000000,
                     'descripcion': 'Obra de arte',
                     'estado': 'activa',
                     'ganador': None,
                     'id': 2,
                     'monto_actual': 0,
                     'nombre': 'Monalisa',
                     'tiempo_restante': 500},
                    {'categoria': 'Farmacos',
                     'costo_inicial': 5000,
                     'descripcion': 'Capsula de cafeina - 200mg',
                     'estado': 'activa',
                     'ganador': None,
                     'id': 23,
                     'monto_actual': 0,
                     'nombre': 'Pastillas de cafeina',
                     'tiempo_restante': 500}],
    PATH_PUJAS: [],
}

# Funciones de utilidades


def leer_archivo(ruta):
    if ruta in __MEMORY__:
        data = __MEMORY__[ruta]
        return list(data) if isinstance(data, list) else data
    return []


def escribir_archivo(ruta, datos):
    __MEMORY__[ruta] = datos


# Funciones de usuarios


def registrar_usuario(nombre, password):
    """
    Agrega el nombre a usuarios.json si no existe
    parametros: el nombre a registrar
    return (boolean, mensaje)
    """
    # Se validan que el usuario y contraseña no sean vacios
    nombre_valido = nombre.strip()
    password_valida = password.strip()

    if not nombre_valido or not password_valida:
        return False, print("El usuario o contraseña no pueden estar vacios.\n")

    usuarios = leer_archivo(PATH_USUARIOS)

    # Evitamos duplicados sin importar mayúsculas/minúsculas
    nombres_existentes = []
    for usuario in usuarios:
        if isinstance(usuario, str):
            nombres_existentes.append(usuario.lower())

    if nombre_valido.lower() in nombres_existentes:
        return False, print(f"El usuario '{nombre_valido}' ya existe.")

    nuevo = {
        "id": len(usuarios) + 1,
        "nombre": nombre,
        "password": password
    }
    usuarios.append(nuevo)
    escribir_archivo(PATH_USUARIOS, usuarios)
    return True, print(f"Usuario {nombre_valido} registrado.\n")


def login():
    """
    Funcion que simula un login de usuarios
    parametros: usuario y contraseña
    return boolean y el usuario logueado
    """
    global USUARIO_ACTUAL

    if USUARIO_ACTUAL:
        return True, print(f"Se encuentra registrado el usuario {USUARIO_ACTUAL['nombre']}")

    nombre = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")

    usuarios = leer_archivo(PATH_USUARIOS)
    for user in usuarios:
        if user["nombre"].lower() == nombre.lower() and user["password"] == password:
            USUARIO_ACTUAL = user['nombre']
            return True, print(f"bienvenido {user['nombre']}")

    return False, "Usuario o contraseña incorrectos."


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
#
#     for sub in subastas:
#         subastas_activas.append(
#             {sub.get('nombre'), sub.get('id'), sub.get('costo_inicial')})
#
#     print(subastas_activas)
#     print("Si desea participar de alguna subasta elija la opcion numero 4 en el menu principal\n")
#     return subastas_activas


def listar_subastas():
    """
    Muestra ID, nombre y costo inicial de cada subasta disponible
    retorna la lista de subastas
    """
    subastas = leer_archivo(PATH_SUBASTAS)

    print("\nSubastas disponibles:")
    for sub in subastas:
        print(f"subasta: {sub.get('id')}")
        print(f"nombre: {sub.get('nombre')}")
        print(f"Costo_inicial: {sub.get('costo_inicial')}")
        print()

    return subastas


def elegir_subasta(subastas):
    while True:
        id_seleccionado = int(input("Elija el ID de la subasta : "))
        # TODO: validar que la subasta tenga ID correcto
        # TODO: retornar el ID de la subasta para el otro archivo JSON


def registrar_puja():
    """
    funcion que registra una puja en una subasta
    Parametros: el usuario que realiza la puja, el monto que quiere realizar
    return (boolean, mensaje).
    """
    # El usuario debe existir
    global USUARIO_ACTUAL

    if not USUARIO_ACTUAL:
        return False, print("Registrarse o logueese para participar de una subasta \n")

    # El monto debe ser numérico y positivo
    monto = float(input("Ingrese un monto a ofertar: "))
    if monto < 0:
        return "Debe ingresar un monto mayor a 0"

    # ingresar el id de la subasta
    subastas = listar_subastas()
    elegir_subasta(subastas)

    # TODO: Debe superar a la mejor puja actual

    # guarda la nueva puja
    pujas = leer_archivo(PATH_PUJAS)

    pujas.append({
        "usuario": USUARIO_ACTUAL,
        "monto": monto,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    })
    escribir_archivo(PATH_PUJAS, pujas)
    return True, f"Puja registrada: {USUARIO_ACTUAL} ofertó {monto}."


# Funcion main principal


def main():
    while True:
        print("Bienvenido a subastas.com")
        print(
            f"Usuario logueado: {USUARIO_ACTUAL if USUARIO_ACTUAL else 'nadie inicio sesion aún'}")
        print("1- Registrarse")
        print("2- Iniciar sesion")
        print("3- Ver subastastas disponibles")
        print("4- Registrar puja")
        print("5- salir")
        opcion = int(input("Elija una opción: "))
        print("")
        while opcion < 1 or opcion > 5:
            opcion = int(input("Elija una opción válida (1-5): "))

        if opcion == 1:
            nombre = input("Ingrese un nombre de usuario: ")
            password = input("Ingrese una contraseña: ")
            registrar_usuario(nombre, password)
        elif opcion == 2:
            login()
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
