"""
    Modulo validaciones
    Se agrupan todas las funciones de validaciones
"""
import re
from data.usuarios import obtener_usuarios

def validarNombre(nombre):
    """
    Valida que el nombre de usuario cumpla los requisitos.

    Reglas:
    - Nombre:
        * Debe contener letras y/o números
        * Largo entre 3 y 20 caracteres
        * Solo mayusculas, minusculas y numeros.

    Params:
        nombre (str): nombre del usuario 

    Return:
        (bool): (es_valido)
                     True si el parametro cumple con las reglas.
    """

    # Se eliminan espacios vacíos.
    nombre_valido = nombre.strip()

    nombre_regex = r"^(?=.*[a-zA-Z])[a-zA-Z0-9]{3,20}$"

    if not re.fullmatch(nombre_regex, nombre_valido):
        print("Nombre inválido. Debe tener 3-20 caracteres, solo letras / numeros\n")
        return False

    return True

def validarContrasena(password):
    """
    Valida que la contraseña cumpla los requisitos.

    Reglas:
    - Contraseña, al menos:
        * 1 minúscula
        * 1 mayúscula
        * 1 número
        * 1 caracter especial
        * Largo entre 6 y 16 caracteres

    Params:
        password (str): contraseña del usuario

    Return:
        (bool): (es_valido)
                     True si la contraseña cumple los requisitos
                     False si hay algún problema
    """

    # Se eliminan espacios vacíos.
    password_valida = password.strip()

    pass_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:<,>.?/|\\~-]).{6,16}$"

    if not re.fullmatch(pass_regex, password_valida):
        print("Contraseña inválida. Debe tener 6-16 caracteres e incluir: ")
        print("una mayúscula, una minúscula, un número y un caracter especial.")
        return False

    return True


def usuario_existe(nombreUsuario):
    """
    validarUsuarioExistente verifica si un nombre de usuario ya fue previamente registrado.

    Args:
        nombreUsuario (str): el nombre de usuario

    Returns:
        boolean: True si el usuario existe. 
                 False si no existe
    """
    listaUsuarios = obtener_usuarios()

    # Evitamos duplicados sin importar mayusculas/minúsculas
    usuario_encontrado = next((user for user in listaUsuarios if user.get("nombre") == nombreUsuario), False)

    if usuario_encontrado:
        return True, usuario_encontrado
    
    return False


def validar_credenciales(nombre:str, contrasena:str):
    """
    validarCredenciales valida la coincidencia de nombre y/o password de usuario
    con las registradas anteriormente.

    Args:
        nombre (str): nombre de usuario
        password (str): constraseña del usuario
        listausuarios (list): lista con todos los nombres de usuarios registrados.

    Returns:
        boolean: True si el usuario existe. 
                 False si el usuario no existe.
    """
    listaUsuarios = obtener_usuarios()
    # Next: detiene la búsqueda tan pronto como encuentra el primer usuario coincidente
    # Usamos tuplas para evitar repetidos. Igualmente no deberían existir.
    usuario = next((user for user in listaUsuarios if user.get("nombre") == nombre and user.get("password") == contrasena), False)

    if usuario:
        return True, usuario
    
    return False, None

def validar_id_subasta(idSubasta, subastas):

    subasta_elegida = next(filter(lambda s: s.get("id") == idSubasta,subastas),None)

    if subasta_elegida is None:
        return False

    return True, subasta_elegida


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
