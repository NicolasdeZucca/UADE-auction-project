# pylint: disable=C0103
# pylint:disable=C0303

"""
    Este modulo representa la estructura básica de la aplicación.
    Proporciona un menu interactivo para el usuario y se realizan
    llamadas a las funciones necesarias para el desarrollo del programa.
"""
import os
from data.subastas             import actualizar_subasta, mostrar_subastas, elegir_subasta
from data.usuarios             import obtener_usuarios, crear_usuario, guardar_usuario
from data.pujas                import obtener_pujas, registrar_usuario_puja, guardar_puja
from data.JSONs                import leer_archivo
from config.config             import PATH_PUJAS, PATH_SUBASTAS
from utilidades.utils          import pedir_entero
from data.JSONs                import leer_archivo
from typing                    import Dict, Any
from validaciones.validaciones import validarNombreContrasena, usuario_existe, validar_credenciales, validar_monto_subasta
 
 
# --- Usuario actual logueado ---
USUARIO_ACTUAL = None
 
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
 
    ok, msj, nombre_valido, password_valida = validarNombreContrasena(
        nombre, password)
    if not ok:
        return (False, print(msj))
 
    try:
 
        usuarios = obtener_usuarios()
        if not usuario_existe(nombre_valido, usuarios):
            return False, print(f"El usuario {nombre_valido} ya existe")
 
        nuevo_usuario = crear_usuario(nombre_valido, password_valida)
       
 
        usuarios.append(nuevo_usuario)
        guardar_usuario(usuarios)
        USUARIO_ACTUAL = nuevo_usuario
        return (True, print(f"Usuario '{nombre_valido}' registrado (ID: {nuevo_usuario['id']}).\n"))
   
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
 
    usuarios = obtener_usuarios()
    ok, user = validar_credenciales(nombre, password, usuarios)
    if ok:
        USUARIO_ACTUAL = user
        return (True, f"Usuario {user['nombre']}logueado")
 
 
    return False, print("Usuario o contraseña incorrectos.")
 
 
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
 
    subastas = mostrar_subastas()
    if not subastas:
        return (False, "No hay subastas disponibles en este momento.")
 
    subasta_elegida = elegir_subasta()
    if not subasta_elegida:
        return False, "No se pudo elegir una subasta."

    subasta_id = subasta_elegida["id"]
 
    # El monto debe ser numerico y positivo
    try:
        monto = int(input("Ingrese un monto a ofertar: "))
 
       
        ok, monto_validado= validar_monto_subasta(monto, subasta_elegida)
        if not ok:
            return (False, "Error, algo salio mal")
 
 
    except ValueError:
        return (False, "El monto debe ser numerico.")
 
    pujas = obtener_pujas()
    user_id = USUARIO_ACTUAL["id"]
    user_nombre = USUARIO_ACTUAL["nombre"]
 
    usuario_puja = registrar_usuario_puja(user_id, user_nombre, monto_validado, subasta_id)
    pujas.append(usuario_puja)
    guardar_puja(pujas)
    actualizar_subasta(subasta_id, monto_validado, user_nombre)
    if not ok:
        return (False, "Error al guardar la puja en disco.")
 
    return (True, f"Puja registrada: {USUARIO_ACTUAL['nombre']} ofertó {monto}.")
 
def generar_informe():
    """
    genera  informe completo de subastas y lo guarda en un archivo de txt, calcula estadisticas y exporta los resultados.
    """
    
    print("Generando informe de subastas")

    # se lee los datos de los archivos JSON 
    pujas = leer_archivo(PATH_PUJAS)
    subastas = leer_archivo(PATH_SUBASTAS) 

    #valida que existan datos antes de procesar
    if not subastas:
        print("No hay subastas para informar.")
        return

    nombre_archivo = "informe_subastas.txt"
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:            
            #encabezado del informe
            archivo.write("INFORME DE SUBASTAS UADE\n")
            archivo.write(f"Total de subastas registradas: {len(subastas)}\n\n") #cantidad total de subastas

            #se recorre la lista de subastas 
            for subasta in subastas:
                id_subasta = subasta.get("id")
                nombre_subasta = subasta.get("nombre", "Sin nombre")
                costo_inicial = subasta.get("costo_inicial", 0)
                pujas_de_subasta = [p for p in pujas if p.get("subasta_id") == id_subasta]

                #calculamos estadisticas de las pujas
                cantidad_pujas = len(pujas_de_subasta) 
                monto_maximo = 0
                promedio_pujas = 0

                if cantidad_pujas > 0:
                    #se crea una lista solo con los montos para los calculos
                    lista_montos = [p.get("monto", 0) for p in pujas_de_subasta]
                    
                    monto_maximo = max(lista_montos) #devuelve el elemento max
                    promedio_pujas = sum(lista_montos) / cantidad_pujas #retorna el promedio

                #escribimos los detalles de la subasta en el archivo
                archivo.write(f"ID: {id_subasta} | Subasta: {nombre_subasta}\n")
                archivo.write(f"Precio Base: ${costo_inicial}\n")
                archivo.write(f"Estado: {subasta.get('estado', 'Desconocido')}\n")
                archivo.write(f"Ganador actual: {subasta.get('ganador') if subasta.get('ganador') else 'Nadie'}\n")
                archivo.write(f" >> Cantidad de pujas: {cantidad_pujas}\n")
                archivo.write(f" >> Puja máxima: ${monto_maximo}\n")
                archivo.write(f" >> Promedio ofertado: ${promedio_pujas}\n")
                archivo.write("\n")
#porcetaje de cantidad de usuarios que participaron en la subasta HACER
        print(f"Informe generado exitosamente en {nombre_archivo}")
    except Exception as e: 
        print(f"error:{e}")
    #lectura del archivo recién creado para mostrarlo
    try: 
        print("\nVista previa del informe")
        with open(nombre_archivo, 'r', encoding='utf-8') as f_lectura: 
            contenido = f_lectura.read() 
            print(contenido)
    except Exception as e: #excepcion  si el archivo no existe
        print(f"no se pudo leer el archivo generado: {e}")

def cerrar_sesion():
    global USUARIO_ACTUAL

    if not USUARIO_ACTUAL:
        return False, print("No hay un usuario logueado actualmente.")

    else:
        USUARIO_ACTUAL = None
        return True, print("...cerrando sesion..."), 
 
# Funcion main principal
def main():
    """
    Funcion principal del programa.
    Muestra un menu interactivo con opciones para el usuario
    """
    while True:
        print("Bienvenido a subastas.com")
        print(
           f"Usuario logueado: {USUARIO_ACTUAL['nombre'] if USUARIO_ACTUAL else 'nadie inició sesión aún'} \n")
        print("1- Registrarse")
        print("2- Iniciar sesion")
        print("3- Ver subastastas disponibles")
        print("4- Registrar puja")
        print("5- Generar informe")
        print("6- Cerrar Sesion")
        print("7- Salir")
        opcion = pedir_entero("Elija una opción (1-7): ", minimo=1, maximo=7)
        print("")
        while opcion < 1 or opcion > 7:
            opcion = int(input("Elija una opción válida (1-7): "))
 
        if opcion == 1:
            nombre = input("Ingrese un nombre de usuario: ")
            password = input("Ingrese una contraseña: ")
            registrar_usuario(nombre, password)
 
        elif opcion == 2:
            nombre = input("Ingrese su nombre de usuario: ")
            password = input("Ingrese su contraseña: ")
            login(nombre, password)
 
        elif opcion == 3:
            mostrar_subastas()
 
        elif opcion == 4:
            registrar_puja()

        elif opcion == 5:
            generar_informe()

        elif opcion == 6:
            cerrar_sesion()

        elif opcion == 7:
            print("Saliendo...")
            break
        else:
            if not isinstance(opcion, int):
                print("Error, debe ingresar un dato numerico válido")
                opcion = int(input("Elija una opción válida (1-7): "))
 
 
main()
 