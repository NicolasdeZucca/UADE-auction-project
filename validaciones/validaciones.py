"""
    Modulo validaciones
    Se agrupan todas las funciones de validaciones
"""
import re
from data.usuarios import obtener_usuarios
from utilidades.utils import pedir_entero

def validarNombre(nombre:str):
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
        print("Nombre inválido. Debe tener 3-20 caracteres, solo letras / numeros (minimo una letra)\n")
        return False

    return True

def validarNombreCategoria(nombreCategoria:str):
    """
    Valida que el nombre de categoria cumpla los requisitos.

    Reglas:
    - Nombre de categoria:
        * Debe contener letras y/o números
        * Largo entre 3 y 20 caracteres
        * Solo mayusculas, minusculas y numeros.
        * Solo una palabra sin espacios.

    Params:
        nombre (str): nombre de categoria 

    Return:
        (bool):  True si el parametro cumple con las reglas.
    """

    # Se eliminan espacios vacíos.
    nombre_valido = nombreCategoria.strip()

    nombre_regex = r"^(?=.*[a-zA-Z])[a-zA-Z0-9]{3,20}$"

    if not re.fullmatch(nombre_regex, nombre_valido):
        print("Categoria inválida. Debe ser una palabra y tener 3-20 caracteres, solo letras / numeros\n")
        return False

    return True

def validarNombreSubasta(nombre:str):
    """
    Valida que el nombre de subasta cumpla los requisitos.

    Reglas:
    - Nombre:
        * Debe contener letras y/o números
        * Largo entre 3 y 50 caracteres
        * Solo mayusculas, minusculas y numeros.

    Params:
        nombre (str): nombre del usuario 

    Return:
        (bool): (es_valido)
                     True si el parametro cumple con las reglas.
    """
    nombre_regex = r"^(?=.*[A-Za-z])[A-Za-z0-9 ]{3,50}$"

    if not re.fullmatch(nombre_regex, nombre):
        print("Nombre inválido. Debe tener 3-50 caracteres, solo letras / numeros\n")
        return False

    return True

def validarDescSubasta(descripcion:str):
    """
    Valida que la descripcion de la subasta cumpla los requisitos.

    Reglas:
    - Descripcion:
        * Debe contener letras y/o números
        * Largo entre 3 y 100 caracteres
        * Solo mayusculas, minusculas y numeros.

    Params:
        Descripcion (str): nombre del usuario 

    Return:
        (bool): (es_valido)
                     True si el parametro cumple con las reglas.
    """
    nombre_regex = r"^(?=.*[A-Za-z])[A-Za-z0-9 ]{3,100}$"

    if not re.fullmatch(nombre_regex, descripcion):
        print("Descripción inválida. Debe tener 3-100 caracteres, solo letras / numeros\n")
        return False

    return True

def validarContrasena(password:str):
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

    pass_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9])\S{6,16}$"

    if not re.fullmatch(pass_regex, password_valida):
        print("Contraseña inválida. Debe tener 6-16 caracteres e incluir: ")
        print("una mayúscula, una minúscula, un número y un caracter especial (sin espacios).\n")
        return False

    return True


def usuario_existe(nombreUsuario, listaUsuarios=None):
    """
    validarUsuarioExistente verifica si un nombre de usuario ya fue previamente registrado.

    Args:
        nombreUsuario (str): el nombre de usuario

    Returns:
        boolean: True si el usuario existe. 
                 False si no existe
    """
    if listaUsuarios is None:
        listaUsuarios = obtener_usuarios()

    # Evitamos duplicados sin importar mayusculas/minúsculas
    usuario_encontrado = next((user for user in listaUsuarios if user.get("nombre") == nombreUsuario), False)

    if usuario_encontrado:
        return True
    
    return False


def validar_credenciales(nombre:str, contrasena:str, listaUsuarios=None):
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
    if listaUsuarios is None:
        listaUsuarios = obtener_usuarios()
    # Next: detiene la búsqueda tan pronto como encuentra el primer usuario coincidente
    # Usamos tuplas para evitar repetidos. Igualmente no deberían existir.
    usuario = next((user for user in listaUsuarios if user.get("nombre") == nombre and user.get("password") == contrasena), False)

    return usuario

def validar_id_subasta(idSubasta, subastas):

    subasta_elegida = next(filter(lambda s: s.get("id") == idSubasta,subastas),None)

    return subasta_elegida


def validar_monto_subasta(monto, subasta):
    
    if monto == 0:
        print("El monto no puede ser vacío")
        return False

    if subasta["monto_actual"] == 0:
        while monto <= subasta["costo_inicial"]:
            print(f"La oferta debe ser mayor al costo inicial: {subasta["costo_inicial"]}.")
            monto = pedir_entero("Ingrese un monto a ofertar nuevamente: ", subasta["costo_inicial"])
        return monto

    while monto <= subasta["monto_actual"]:
        print(f"La oferta debe ser mayor al precio vigente: {subasta["monto_actual"]}.")
        monto = pedir_entero("Ingrese una nueva oferta: ", subasta["monto_actual"])
    
    
    return monto
