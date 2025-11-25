"""
    Modulo de subastas
"""
 
from config.config             import PATH_SUBASTAS
from data.JSONs                import leer_archivo, escribir_archivo
from utilidades.utils          import pedir_entero, calcular_tiempo_restante, actualizar_estado_por_tiempo
from validaciones.validaciones import validar_id_subasta, validarNombreSubasta, validarNombreCategoria, validarDescSubasta
from datetime                  import datetime, timedelta
import random
 
 
def obtener_subastas():
    subastas = leer_archivo(PATH_SUBASTAS)
    cambio = False

    for s in subastas:
        if actualizar_estado_por_tiempo(s):
            cambio = True

    if cambio:
        escribir_archivo(PATH_SUBASTAS, subastas)
        
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
        if sub["estado"] == "activa":
            print(f"Tiempo restante: {calcular_tiempo_restante(sub)}")
        else:
            print("Estado: FINALIZADA")
        if sub['monto_actual'] == 0:
            print("Todavia no hay pujas en esta subasta.")
        else:
            print(f"Puja actual: {sub.get('monto_actual')}")
            print(f"Ganador de puja actual: {sub.get('ganador')}")
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
 
    subasta = validar_id_subasta(subastaID, subastas)
    if not subasta:
        print("No se encontro el ID de la subasta")
        return False
 
    subasta["monto_actual"] = montoActual
    subasta["ganador"] = ganador
 
    guardar_subastas(subastas)
    return True

def generar_id_subasta():

    subastas = obtener_subastas()
    id = random.randint(1000,10000)
    idSubastas = [user["id"] for user in subastas]
    while True:
        if id in idSubastas:
            id = random.randint(1,10000)
        else:
            return id
   
def crear_subasta():

    subastas = obtener_subastas()

    while True:
        nombre = input("Ingrese el nombre de la subasta (o 'salir' para volver al menu de administrador): ")
        print()

        if nombre.strip().lower() == "salir":
            print("Volviendo al menu de administrador...\n")
            break

        if validarNombreSubasta(nombre):
            while True:
                categoria = input("Ingrese la categoria de la subasta (y 'atras' para volver a ingresar el nombre o 'salir' para volver al menu de administrador): ")
                print()

                if categoria.strip().lower() == "salir":
                    print("Volviendo al menu de administrador...\n")
                    return False

                if categoria.strip().lower() == "atras":
                    print("Volviendo a ingresar el nombre de la subasta...\n")
                    break

                if validarNombreCategoria(categoria):
                    while True:
                        descripcion = input("Ingrese la descripcion de la subasta (y 'atras' para volver a ingresar la categoria o 'salir' para volver al menu de administrador): ")
                        print()

                        if descripcion.strip().lower() == "salir":
                            print("Volviendo al menu de administrador...\n")
                            return False

                        if descripcion.strip().lower() == "atras":
                            print("Volviendo a ingresar la categoria de la subasta...\n")
                            break

                        if validarDescSubasta(descripcion):
                            while True:
                                precioInicial = pedir_entero("Ingrese el precio inicial de la subasta: ", 1)
                                print()

                                while True:
                                    duracionMin = pedir_entero("Ingrese la duracion de la subasta en minutos: ", 10)
                                    print()

                                    duracionSegundos = duracionMin * 60

                                    ahora = datetime.now()

                                    fechaFin = (ahora+timedelta(seconds=duracionSegundos)).isoformat(timespec="seconds")

                                    idSubasta = generar_id_subasta()

                                    subasta = {
                                        "id": idSubasta,
                                        "nombre": nombre,
                                        "categoria": categoria,
                                        "costo_inicial" : precioInicial,
                                        "descripcion" : descripcion,
                                        "estado" : "activa",
                                        "fecha_inicio" : str(ahora),
                                        "fecha_fin" : str(fechaFin),
                                        "monto_actual" : 0,
                                        "ganador" : None
                                    }

                                    subastas.append(subasta)
                                    guardar_subastas(subastas)
                                    print(f"Subasta con ID:{idSubasta}\n")
                                    return
                            
                        else:
                            continue

                else:
                    continue   
                    



        else:
            continue
