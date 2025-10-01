from functools import reduce
import os
import json

USUARIO_ACTUAL = None

USUARIOS = []

SUBASTAS = [
    {"id": 1, "nombre": "Subasta de arte", "costo_inicial": 1000},
    {"id": 2, "nombre": "Subasta de autos", "costo_inicial": 5000},
    {"id": 3, "nombre": "Subasta de tecnología", "costo_inicial": 300}
]


PUJAS = []

def registrar_usuario(nombre, password):

    nombre_valido = nombre.strip()

    password_valida = password.strip()

    if not nombre_valido or not password_valida:

        print("ewl usuario o contraseña no pueden estar vacíos.\n")

        return False

    for usuario in USUARIOS:

        if usuario["nombre"].lower() == nombre_valido.lower():

            print(f"El usiario '{nombre_valido}' ya existe.")

            return False

    nuevo = {

        "id": len(USUARIOS) + 1,

        "nombre": nombre_valido,
        "password": password_valida

    }

    USUARIOS.append(nuevo)

    print(f"Usuario {nombre_valido} regitsrado.\n")

    return True


def login():

    global USUARIO_ACTUAL
    if USUARIO_ACTUAL:

        print(f"Ya hay una sesión activa: {USUARIO_ACTUAL['nombre']}")
        return True
    nombre = input("Ingrese su nombre de usuario: ")

    password = input("Ingrese su contraseña: ")

    for user in USUARIOS:

        if user["nombre"].lower() == nombre.lower() and user["password"] == password:

            USUARIO_ACTUAL = user

            print(f"Bienvenido  {user['nombre']}")
            return True

    print("Usuario o contraseña incorrectos")
    return False


def logout():

    global USUARIO_ACTUAL

    if USUARIO_ACTUAL:

        print(f"Sesión cerrada para {USUARIO_ACTUAL['nombre']}.")
        USUARIO_ACTUAL = None

    else:

        print("No hay sesión activa.")


def listar_subastas():

    if not SUBASTAS:
        print("\nNo hay subastas disponibles.")

        return []

    print("\nSubastas disponibles:")

    for sub in SUBASTAS:

        print(f"subasta: {sub.get('id')}")
        print(f"nombre: {sub.get('nombre')}")

        print(f"Costo inicial: {sub.get('costo_inicial')}")

        print()

    return SUBASTAS


def elegir_subasta(subastas):

    if not subastas:

        print("No hay subatsas para elgeir.")

        return None

    id_seleccionado = input("Elija el ID de la subasta: ")

    if not id_seleccionado.isdigit():

        print("Ingrese un número válido.")

        return None

    id_seleccionado = int(id_seleccionado)

    for sub in subastas:

        if sub["id"] == id_seleccionado:

            return sub

    print("ID de subasta inválido.")

    return None


def mejor_puja_para_subasta(subasta_id):
    pujas_subasta = [p for p in PUJAS if p["subasta_id"] == subasta_id]

    if not pujas_subasta:
        return None

    return max(pujas_subasta, key=lambda x: x["monto"])


def mostrar_historial_pujas():

    if not SUBASTAS:

        print("No hay subastas para mostrar.")
        return

    subastas = listar_subastas()

    subasta = elegir_subasta(subastas)

    if not subasta:

        return

    pujas_subasta = [p for p in PUJAS if p["subasta_id"] == subasta["id"]]

    if not pujas_subasta:
        print("No hay pujas para esta subasta.")

        return

    print(f"Historial de pujas para '{subasta['nombre']}':")

    for p in pujas_subasta:

        print(f"{p['usuario']} ofertó {p['monto']}")


def registrar_puja():

    global USUARIO_ACTUAL

    if not USUARIO_ACTUAL:

        print("Regístrese o inicie sesión para participar de una subasta.\n")

        return False

    subastas = listar_subastas()
    if not subastas:

        return False

    subasta = elegir_subasta(subastas)

    if not subasta:
        return False

    mejor_puja = mejor_puja_para_subasta(subasta["id"])

    if mejor_puja:

        minimo = mejor_puja["monto"] + 1
        print(
            f"La mejor puja actual es de {mejor_puja['monto']} por {mejor_puja['usuario']}. Debe ofertar al menos {minimo}.")

    else:

        minimo = subasta["costo_inicial"]

        print(f"No hay pujas aún. El costo inicial es {minimo}.")
    monto_str = input("Ingrese un monto a ofertar: ")

    if not monto_str.replace('.', '', 1).isdigit():
        print("Ingrese un motno válido.")

        return False

    monto = float(monto_str)

    if monto < minimo:
        print(f"Debe ingresar un monto mayor o igual a {minimo}")

        return False
    PUJAS.append({

        "usuario": USUARIO_ACTUAL["nombre"],

        "subasta_id": subasta["id"],


        "monto": monto

    })

    print(
        f"Puja registrada: {USUARIO_ACTUAL['nombre']} oferot {monto} en '{subasta['nombre']}'.")


def crear_subasta():

    global USUARIO_ACTUAL

    if not USUARIO_ACTUAL:

        print("Debe iniciar sesión para crear una subasta.\n")

        return False

    nombre = input("Ingrese el nombre de la nueva subasta: ").strip()

    if not nombre:

        print("El nombre de la subasta no puede estar vacío.")
        return False
    costo_inicial_str = input("Ingrese el costo inicial: ")

    if not costo_inicial_str.replace('.', '', 1).isdigit():

        print("Debe ingresar un número válido para el costo inicial.")
        return False

    costo_inicial = float(costo_inicial_str)

    if costo_inicial <= 0:
        print("El costo inicial debe  ser mayor a 0.")

        return False

    nueva_subasta = {

        "id": len(SUBASTAS) + 1,

        "nombre": nombre,

        "costo_inicial": costo_inicial

    }

    SUBASTAS.append(nueva_subasta)

    print(
        f"Subasta '{nombre}' creada exitosamente noc costo inicial {costo_inicial}.")

    return True


def mostrar_nombres_subastas():

    if not SUBASTAS:

        print("No hay subastas.")

        return

    nombres = list(map(lambda s: s["nombre"], SUBASTAS))
    print("Nombres de subastas:")

    for nombre in nombres:

        print("-", nombre)


def total_pujado():

    if not PUJAS:

        print("No hay pujas registradas.")

        return
    total = reduce(lambda acc, p: acc + p["monto"], PUJAS, 0)
    print(f"Total de dinero pujado en todas las subastas:: {total}")


def main():

    salir = False

    while not salir:

        print("\nBienvenidfo a AUCTION OL")

        print(
            f"Usuario logueado: {USUARIO_ACTUAL['nombre'] if USUARIO_ACTUAL else 'nadie inició sesión aún'}")

        print("1- Registrarse")

        print("2- Iniciar sesión")
        print("3- Ver subastas disponibles")

        print("4- Registrar puja")

        print("5- Ver historial de pujas")

        print("6- Crear subasta")
        print("7- Mostrar nombres de subastas")

        print("8- Mostrar total pujado")

        print("9- Cerrar sesión")

        print("10- Salir")

        opcion = input("Elija una opción: ")

        print("")

        if opcion == "1":

            nombre = input("Ingrese un nombre de usuario: ")
            password = input("Ingrese una contraseña: ")

            registrar_usuario(nombre, password)

        elif opcion == "2":

            login()

        elif opcion == "3":

            listar_subastas()

        elif opcion == "4":
            registrar_puja()

        elif opcion == "5":

            mostrar_historial_pujas()

        elif opcion == "6.":

            crear_subasta()

        elif opcion == "7":

            mostrar_nombres_subastas()

        elif opcion == "8":

            total_pujado()

        elif opcion == "9":

            logout()
        elif opcion == "10":

            print("¡Hasta luegoo!")
            salir = True
        else:
            print("Elija una opción válisa (1-10): ")


main()
