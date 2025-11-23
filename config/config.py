import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


PROJECT_ROOT = os.path.dirname(BASE_DIR)
print("PROJECT_ROOT", PROJECT_ROOT)


PATH_USUARIOS = os.path.join(PROJECT_ROOT, "usuarios.json")
PATH_SUBASTAS = os.path.join(PROJECT_ROOT, "subastas.json")
PATH_PUJAS    = os.path.join(PROJECT_ROOT, "pujas.json")
