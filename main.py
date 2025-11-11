"""
    Este modulo representa la estructura básica de la aplicación.
    Proporciona un menu interactivo para el usuario y se realizan
    llamadas a las funciones necesarias para el desarrollo del programa.
"""
 
from data.subastas             import actualizar_subasta, mostrar_subastas, elegir_subasta
from data.usuarios             import obtener_usuarios, crear_usuario, guardar_usuario
from data.pujas                import obtener_pujas, registrar_usuario_puja, guardar_puja
from data.JSONs                import leer_archivo
from config.config             import PATH_PUJAS, PATH_SUBASTAS
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
 
def generar_informe():

    imprimir=True
    
    pujas = leer_archivo(PATH_PUJAS)
    subastas = leer_archivo(PATH_SUBASTAS)

    subastasPorId = {subasta.get("id"): subasta for subasta in subastas if subasta.get("id") is not None}

    pujasPorSubasta = {}
    for puja in pujas:
        idDeSubasta = puja.get("subasta_id")
        if idDeSubasta is None:
            continue
        pujasPorSubasta.setdefault(idDeSubasta, []).append(puja)

    ids = set(subastasPorId.keys()) | set(pujasPorSubasta.keys())

    informe = {}
    for idDeSubasta in sorted(ids):
        sub = subastasPorId.get(idDeSubasta, {})
        nombre = sub.get("nombre", f"<subasta {idDeSubasta} sin nombre>")
        costoinicial = sub.get("costo_inicial")

        historial = pujasPorSubasta.get(idDeSubasta, [])
        try:
            historialOrdenado = sorted(historial, key=lambda x: x.get("timestamp") or "")
        except Exception:
            historialOrdenado = historial[:]

        montos = []
        for pujaOrdenada in historialOrdenado:
            monto = pujaOrdenada.get("monto", 0)
            try:
                montos.append(int(monto))
            except Exception:
                try:
                    montos.append(int(float(monto)))
                except Exception:
                    continue
        mayorPuja = max(montos) if montos else 0
        cantidad = len(historialOrdenado)

        informe = {
            "subasta_id": idDeSubasta,
            "nombre": nombre,
            "costo_inicial": costoinicial,
            "cantidad_pujas": cantidad,
            "mayor_puja": mayorPuja,
            "historial": historialOrdenado
        }
        informe[idDeSubasta] = informe

        if imprimir:
            print("--------------------------------------------------")
            print(f"Subasta {idDeSubasta} - {nombre}")
            print(f"Costo inicial: {costoinicial}")
            print(f"Pujas totales: {cantidad}")
            print(f"Mayor puja: {mayorPuja}")
            print("Historial de pujas:")
            if historialOrdenado:
                for pujaOrdenada in historialOrdenado:
                    usr = pujaOrdenada.get("usuario", pujaOrdenada.get("id_usuario", "<sin usuario>"))
                    monto = pujaOrdenada.get("monto", 0)
                    print(f"  - {usr} | {monto}")
            else:
                print("  (No hay pujas registradas para esta subasta)")
            print()

    return informe

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
           f"Usuario logueado: {USUARIO_ACTUAL['nombre'] if USUARIO_ACTUAL else 'nadie inició sesión aún'}")
        print("1- Registrarse")
        print("2- Iniciar sesion")
        print("3- Ver subastastas disponibles")
        print("4- Registrar puja")
        print("5- Generar informe")
        print("6- Cerrar Sesion")
        print("7- Salir")
        opcion = int(input("Elija una opción: "))
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
 