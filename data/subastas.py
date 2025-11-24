"""
    Modulo de subastas
"""
 
from config.config import PATH_SUBASTAS
from data.JSONs import leer_archivo, escribir_archivo
from utilidades.utils import pedir_entero
from validaciones.validaciones import validar_id_subasta
 
 
def obtener_subastas():
    subastas = leer_archivo(PATH_SUBASTAS)
    return subastas
 
 
def mostrar_subastas():
    """
    listar_subastas muestra ID, nombre y costo inicial de cada subasta disponible
    y las muestra por pantalla
 
    Returns:
        list: lista de subastas
    """
    subastas = leer_archivo(PATH_SUBASTAS)
   
    if not subastas:
        print("No hay subastas disponibles. \n")
        return []
 
    print("\nSubastas disponibles:\n")
    for sub in subastas:
        print("-------------------------------------------")
        print(f"Subasta ID: {sub.get('id')}")
        print(f"Nombre: {sub.get('nombre')}")
        print(f"Costo inicial: {sub.get('costo_inicial')}")
        print(f"Puja actual: {sub.get('monto_actual')}")
        print("-------------------------------------------\n")
 
 
def guardar_subastas(subasta):
    escribir_archivo(PATH_SUBASTAS, subasta)
 
 
def elegir_subasta():
    """
    elegir_subasta Pide al usuario un ID de subasta y devuelve la subasta elegida.
    Si elige algo inválido, vuelve a pedir.
 
    Args:
        subastas (list): lista de subastas existentes.
    """
    subastas = leer_archivo(PATH_SUBASTAS)
    
    if not subastas:
        print("No hay subastas disponibles. \n")
        return None
 
    while True:
        try:
            id_seleccionado = pedir_entero("Elija el ID de la subasta : ")
            
 
        except ValueError:
            print("Por favor ingrese un numero válido.\n")
            return
 
        subasta = validar_id_subasta(id_seleccionado, subastas)
        if not subasta:
            print("ERROR: No existe una subasta con ese ID.\n")
            continue
            
        print(f"Subasta seleccionada: {subasta['nombre']} (ID: {subasta['id']})\n")
        return subasta

 
def actualizar_subasta(subastaID, montoActual, ganador=None):
 
    subastas = obtener_subastas()
 
    estado, subasta = validar_id_subasta(subastaID, subastas)
    if not estado:
        return estado, "No se encontro ID de subasta"
 
    subasta["monto_actual"] = montoActual
    if subasta["ganador"] is None:
        subasta["ganador"] = ganador
 
    guardar_subastas(subastas)
   
 