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
    
    pujas = leer_archivo(PATH_PUJAS) or []
    subastas = leer_archivo(PATH_SUBASTAS) or []

    subastas_map = {s.get("id"): s for s in subastas if s.get("id") is not None}

    pujas_por_sub = {}
    for p in pujas:
        sid = p.get("subasta_id")
        if sid is None:
            continue
        pujas_por_sub.setdefault(sid, []).append(p)

    ids = set(subastas_map.keys()) | set(pujas_por_sub.keys())

    informes = {}
    for sid in sorted(ids):
        sub = subastas_map.get(sid, {})
        nombre = sub.get("nombre", f"<subasta {sid} sin nombre>")
        costo_inicial = sub.get("costo_inicial")

        historial = pujas_por_sub.get(sid, [])
        try:
            historial_ordenado = sorted(historial, key=lambda x: x.get("timestamp") or "")
        except Exception:
            historial_ordenado = historial[:]

        montos = []
        for pu in historial_ordenado:
            m = pu.get("monto", 0)
            try:
                montos.append(int(m))
            except Exception:
                try:
                    montos.append(int(float(m)))
                except Exception:
                    continue
        mayor_puja = max(montos) if montos else 0
        cantidad = len(historial_ordenado)

        informe = {
            "subasta_id": sid,
            "nombre": nombre,
            "costo_inicial": costo_inicial,
            "cantidad_pujas": cantidad,
            "mayor_puja": mayor_puja,
            "historial": historial_ordenado
        }
        informes[sid] = informe

        if imprimir:
            print("--------------------------------------------------")
            print(f"Subasta {sid} - {nombre}")
            print(f"Costo inicial: {costo_inicial}")
            print(f"Pujas totales: {cantidad}")
            print(f"Mayor puja: {mayor_puja}")
            print("Historial de pujas:")
            if historial_ordenado:
                for pu in historial_ordenado:
                    ts = pu.get("timestamp", "")
                    usr = pu.get("usuario", pu.get("id_usuario", "<sin usuario>"))
                    monto = pu.get("monto", 0)
                    print(f"  - {ts} | {usr} | {monto}")
            else:
                print("  (No hay pujas registradas para esta subasta)")
            print()

    return informes
 
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
        print("6- Salir")
        opcion = int(input("Elija una opción: "))
        print("")
        while opcion < 1 or opcion > 5:
            opcion = int(input("Elija una opción válida (1-6): "))
 
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
            print("Saliendo...")
            break
        else:
            if not isinstance(opcion, int):
                print("Error, debe ingresar un dato numerico válido")
                opcion = int(input("Elija una opción válida (1-6): "))
 
 
main()
 