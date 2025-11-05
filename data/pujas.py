"""
    Modulo pujas
"""
 
from datetime import datetime
from config.config import PATH_PUJAS
from data.JSONs import leer_archivo, escribir_archivo
 
 
def obtener_pujas():
    pujas = leer_archivo(PATH_PUJAS)
    return pujas
 
def guardar_puja(puja):
    escribir_archivo(PATH_PUJAS, puja)
 
 
def registrar_usuario_puja(user_id, nombre, monto, subasta_id):
 
    nueva_puja = {
        "id_usuario": user_id,
        "usuario": nombre,
        "monto": monto,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "subasta_id": subasta_id
    }
 
    return nueva_puja