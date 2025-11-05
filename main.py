"""
    Este modulo representa la estructura básica de la aplicación.
    Proporciona un menu interactivo para el usuario y se realizan
    llamadas a las funciones necesarias para el desarrollo del programa.
"""
 
from data.subastas             import actualizar_subasta, mostrar_subastas, elegir_subasta
from data.usuarios             import obtener_usuarios, crear_usuario, guardar_usuario
from data.pujas                import obtener_pujas, registrar_usuario_puja, guardar_puja
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
    subasta_id = subasta_elegida.get("id")
 
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
 
 
 
# Funcion main principal
def main():
    """
    Funcion principal del programa.
    Muestra un menu interactivo con opciones para el usuario
    """
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
            mostrar_subastas()
 
        elif opcion == 4:
            registrar_puja()
 
        elif opcion == 5:
            print("Saliendo...")
            break
        else:
            if not isinstance(opcion, int):
                print("Error, debe ingresar un dato numerico válido")
                opcion = int(input("Elija una opción válida (1-5): "))
 
 
main()
 