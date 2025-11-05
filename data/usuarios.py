"""
    Modulo de usuarios
"""
 
from config.config import PATH_USUARIOS
from data.JSONs import leer_archivo, escribir_archivo
from utilidades.utils import generate_ID
 
 
def obtener_usuarios():
    usuarios = leer_archivo(PATH_USUARIOS)
    return usuarios
 
 
def guardar_usuario(usuario):
    escribir_archivo(PATH_USUARIOS, usuario)
 
 
def crear_usuario(nombre, password):
 
    usuario = {
        "id": generate_ID(),
        "nombre": nombre,
        "password": password
        }
 
    return usuario
 
 