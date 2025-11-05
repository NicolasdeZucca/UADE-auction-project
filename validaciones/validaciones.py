"""
    Modulo validaciones
    Se agrupan todas las funciones de validaciones
"""
import re



def validarNombreContrasena(nombre, password):
    """
    Valida que el nombre de usuario y su contraseña cumplan los requisitos.

    Reglas:
    - Nombre:
        * Debe contener letras y/o números
        * Largo entre 3 y 20 caracteres
        * Solo mayusculas, minusculas y numeros.
    - Contraseña, al menos:
        * 1 minúscula
        * 1 mayúscula
        * 1 número
        * 1 caracter especial
        * Largo entre 6 y 16 caracteres

    Params:
        nombre (str): nombre del usuario 
        password (str): contraseña del usuario

    Return:
        (bool, str): (es_valido, mensaje_de_validacion)
                     True si ambas cosas son válidas
                     False si hay algún problema
    """

    # Se eliminan espacios vacíos.
    nombre_valido = nombre.strip()
    password_valida = password.strip()

    nombre_regex = r"^(?=.*[a-zA-Z])[a-zA-Z0-9]{3,20}$"
    pass_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:<,>.?/|\\~-]).{6,16}$"

    if not re.fullmatch(nombre_regex, nombre_valido):
        return (False,
                "Nombre inválido. Debe tener 3-20 caracteres, solo letras / numeros", None, None)


    if not re.fullmatch(pass_regex, password_valida):
        return (False,
                "Contraseña inválida. Debe tener 6-16 caracteres e incluir: "
                "una mayúscula, una minúscula, un número y un caracter especial.", None, None)


    return (True, "Usuario y contraseña validos", nombre_valido, password_valida)


def usuario_existe(nombreUsuario, listaUsuarios):
    """
    validarUsuarioExistente verifica si un nombre de usuario ya fue previamente registrado.

    Args:
        nombreUsuario (str): el nombre de usuario
        lista (list): una lista con todos los nombres de usuarios registrados 

    Returns:
        boolean: True si el usuario existe. 
                 False si no existe
    """

    # Evitamos duplicados sin importar mayusculas/minúsculas
    nombres_existentes = [user['nombre'] for user in listaUsuarios]

    if nombreUsuario in nombres_existentes:
        return (True, (f"El usuario '{nombreUsuario}' ya existe."))
    
    return (False, f"El usuario {nombreUsuario} no está registrado.")


def validar_credenciales(nombre, password, listausuarios):
    """
    validarCredenciales valida la coincidencia de nombre y password de usuario
    con las registradas anteriormente.

    Args:
        nombre (str): nombre de usuario
        password (str): constraseña del usuario
        listausuarios (list): lista con todos los nombres de usuarios registrados.

    Returns:
        boolean: True si el usuario existe. 
                 False si el usuario no existe.
    """

    # Next: detiene la búsqueda tan pronto como encuentra el primer usuario coincidente
    # Usamos tuplas para evitar repetidos. Igualmente no deberían existir.
    usuario_encontrado = next(
        (user for user in listausuarios if user.get("nombre") == nombre and user.get("password") == password),None)

    if usuario_encontrado:
        return True, usuario_encontrado

    return False, None


def validar_id_subasta(idSubasta, subastas):

    subasta_elegida = next(filter(lambda s: s.get("id") == idSubasta,subastas),None)

    if subasta_elegida is None:
        return (False, f"No existe una subasta con ID: {idSubasta}.")

    return (True, subasta_elegida)


def validar_monto_subasta(monto, objSubasta):
    
    if monto == 0:
        print("El monto no puede ser vacío")
        return False, -1

    if objSubasta["monto_actual"] == 0:
        while monto < objSubasta["costo_inicial"]:
            print(f"La oferta debe ser mayor al costo inicial: {objSubasta["costo_inicial"]}.")
            monto = int(input("Ingrese un monto a ofertar nuevamente: "))
        return True, monto

    while monto < objSubasta["monto_actual"]:
        print("MONTO ACTUAL NO ENTRA")
        print(f"La oferta debe ser mayor al precio vigente: {objSubasta["monto_actual"]}.")
        monto = int(input("Ingrese una nueva oferta: "))
    return True, monto
