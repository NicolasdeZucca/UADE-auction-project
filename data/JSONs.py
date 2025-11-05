"""
    Modulo de lectura de archivos
"""
import json
import os


def leer_archivo(ruta):
    """
    leer_archivo 

    Args:
        ruta (str): La ruta del archivo

    Returns:
        List: lista mostrando los datos del archivo
    """
    if not os.path.exists(ruta):
        return []

    try:

        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
    
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    
    except Exception as e:
        print(f"Error en leer archivo, utilizando {ruta}: {e}")
        return []
        
        
    return data

def escribir_archivo(ruta, datos):
    """
    Escribe la lista completa en el archivo JSON.
    Maneja excepciones sin romper el main loop

    Args:
        ruta (str): ruta del archivo
        datos (_type_): _description_
    """
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
            return True

    except Exception as e:
        print(f"Error en escribir archivo, utilizando {ruta}: {e}")
        return False




def get_subastas():
    pass
def save_subastas():
    pass
def get_usuarios():
    pass
def save_usuarios():
    pass
def get_pujas():
    pass
def save_pujas():
    pass