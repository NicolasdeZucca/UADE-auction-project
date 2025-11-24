# pylint: disable=C0103
# pylint:disable=C0303

"""
    Este modulo representa la estructura básica de la aplicación.
    Proporciona un menu interactivo para el usuario y se realizan
    llamadas a las funciones necesarias para el desarrollo del programa.
"""
import os
from data.subastas             import actualizar_subasta, mostrar_subastas, elegir_subasta
from data.usuarios             import obtener_usuarios, crear_usuario, guardar_usuario
from data.pujas                import obtener_pujas, registrar_usuario_puja, guardar_puja
from data.JSONs                import leer_archivo
from config.config             import PATH_PUJAS, PATH_SUBASTAS, PATH_USUARIOS
from utilidades.utils          import pedir_entero, limpiar
from data.JSONs                import leer_archivo
from typing                    import Dict, Any
from validaciones.validaciones import validarNombre, validarContrasena, usuario_existe, validar_credenciales, validar_monto_subasta
import json
 
 
# --- Usuario actual logueado ---
USUARIO_ACTUAL = None
 
# Funciones de usuarios
def registrar_usuario():
    """
    Agrega / registra el nombre de usuario en 'usuarios.json' si no existe
 
    Returns:
        boolean:    True si el usuario fue cargado.
                    False si el usuario decidio salir.
    """
    global USUARIO_ACTUAL
    
    usuarios = obtener_usuarios()
    
    while True:
        nombre = input("Ingrese su nombre de usuario (o 'salir' para volver atras): ")
        print()

        if nombre.strip().lower() == "salir":
            print("Volviendo al menu de inicio...\n")
            return False
        
        if validarNombre(nombre):
            if usuario_existe(nombre):
                print(f"El usuario {nombre} ya existe, intente nuevamente...\n")
                continue

            else:
                while True:
                    contrasena = input(f"Ingrese la contrasena de '{nombre}' para registrar el usuario (o 'salir' para volver atras): ")
                    print()

                    if contrasena.strip().lower() == "salir":
                        print("Volviendo al menu de inicio...\n")
                        return False

                    if validarContrasena(contrasena):
                        usuario = crear_usuario(nombre, contrasena)
                        usuarios.append(usuario)
                        guardar_usuario(usuarios)
                        print(f"Usuario creado con exito, su ID es {usuario["id"]}\n")
                        USUARIO_ACTUAL = usuario
                        return True
                    else:
                        continue
        else:
            continue

 
def login():
    """
    Funcion de login de usuarios.
 
    Returns:
        boolean:    True  + el usuario logueado
                    False.
    """
    global USUARIO_ACTUAL
    
    while True:
        nombre = input("Ingrese su nombre de usuario (o 'salir' para volver atras): ")
        print()

        if nombre.strip().lower() == "salir":
            print("Volviendo al menu de inicio...\n")
            return False
        
        if validarNombre(nombre):
            contrasena = input(f"Ingrese la contrasena de {nombre} para iniciar sesion (o 'salir' para volver atras): ")
            print()

            if contrasena.strip().lower() == "salir":
                print("Volviendo al menu de inicio...\n")
                return False

            usuario = validar_credenciales(nombre, contrasena)

            if usuario:
                USUARIO_ACTUAL = usuario
                print(f"Felicidades {nombre}, inicio sesion con exito\n")
                return True
            else:
                print("La contraseña o el usuario son incorretos, intente nuevamente...\n")
                continue
        else:
            continue
 
 
def registrar_puja():
    """
    funcion que registra una puja en una subasta
    return (boolean).
    """
 
    mostrar_subastas()
     
    subasta_elegida = elegir_subasta()
    if not subasta_elegida:
        print("No se pudo elegir una subasta.")
        return False
    
    if subasta_elegida["ganador"] == USUARIO_ACTUAL["nombre"]:
        print(f"\n¡Ya eres el mayor postor de esta subasta! (Tu oferta actual: ${subasta_elegida['monto_actual']})")
        print("No puedes volver a pujar hasta que alguien te supere.\n")
        return False
    
    subasta_id = subasta_elegida["id"]
 
    # El monto debe ser numerico y positivo
    try:
        monto = pedir_entero("Ingrese un monto a ofertar: ")
 
        monto_validado = validar_monto_subasta(monto, subasta_elegida)
        
        if not monto_validado: 
            return False
        
        
    except Exception as e:
        print(f"Nadie sabe que paso: {e}")
        return False
 
    pujas = obtener_pujas()
    user_id = USUARIO_ACTUAL["id"]
    user_nombre = USUARIO_ACTUAL["nombre"]
 
    usuario_puja = registrar_usuario_puja(user_id, user_nombre, monto_validado)
    
    try:
        pujas[str(subasta_id)].append(usuario_puja)
    except KeyError:
        pujas[str(subasta_id)] = []
        pujas[str(subasta_id)].append(usuario_puja)
    
    
    if not actualizar_subasta(subasta_id, monto_validado, user_nombre):
        print("Error al guardar la SUBASTA.")
        return False
    
    
    guardar_puja(pujas)
    print(f"Puja registrada: {USUARIO_ACTUAL['nombre']} ofertó {monto_validado}.")
    return True
 
def generar_informe():
    """
    genera  informe completo de subastas y lo guarda en un archivo de txt, calcula estadisticas y exporta los resultados.
    """
    
    print("Generando informe de subastas")

    # se lee los datos de los archivos JSON 
    pujas = leer_archivo(PATH_PUJAS)
    subastas = leer_archivo(PATH_SUBASTAS) 

    #valida que existan datos antes de procesar
    if not subastas:
        print("No hay subastas para informar.")
        return

    nombre_archivo = "informe_subastas.txt"
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:            
            #encabezado del informe
            archivo.write("INFORME DE SUBASTAS UADE\n")
            archivo.write(f"Total de subastas registradas: {len(subastas)}\n\n") #cantidad total de subastas

            #se recorre la lista de subastas 
            for subasta in subastas:
                id_subasta = subasta.get("id")
                nombre_subasta = subasta.get("nombre", "Sin nombre")
                costo_inicial = subasta.get("costo_inicial", 0)
                pujas_de_subasta = [p for p in pujas if p.get("subasta_id") == id_subasta]

                #calculamos estadisticas de las pujas
                cantidad_pujas = len(pujas_de_subasta) 
                monto_maximo = 0
                promedio_pujas = 0

                if cantidad_pujas > 0:
                    #se crea una lista solo con los montos para los calculos
                    lista_montos = [p.get("monto", 0) for p in pujas_de_subasta]
                    
                    monto_maximo = max(lista_montos) #devuelve el elemento max
                    promedio_pujas = sum(lista_montos) / cantidad_pujas #retorna el promedio

                #escribimos los detalles de la subasta en el archivo
                archivo.write(f"ID: {id_subasta} | Subasta: {nombre_subasta}\n")
                archivo.write(f"Precio Base: ${costo_inicial}\n")
                archivo.write(f"Estado: {subasta.get('estado', 'Desconocido')}\n")
                archivo.write(f"Ganador actual: {subasta.get('ganador') if subasta.get('ganador') else 'Nadie'}\n")
                archivo.write(f" >> Cantidad de pujas: {cantidad_pujas}\n")
                archivo.write(f" >> Puja máxima: ${monto_maximo}\n")
                archivo.write(f" >> Promedio ofertado: ${promedio_pujas}\n")
                archivo.write("\n")
#porcetaje de cantidad de usuarios que participaron en la subasta HACER
        print(f"Informe generado exitosamente en {nombre_archivo}")
    except Exception as e: 
        print(f"error:{e}")
    #lectura del archivo recién creado para mostrarlo
    try: 
        print("\nVista previa del informe")
        with open(nombre_archivo, 'r', encoding='utf-8') as f_lectura: 
            contenido = f_lectura.read() 
            print(contenido)
    except Exception as e: #excepcion  si el archivo no existe
        print(f"no se pudo leer el archivo generado: {e}")

def cerrar_sesion():
    global USUARIO_ACTUAL

    if not USUARIO_ACTUAL:
        return False, print("No hay un usuario logueado actualmente.")

    else:
        USUARIO_ACTUAL = None
        return True, print("...cerrando sesion..."), 
 
# Funcion main principal
def main():
    """
    Funcion principal del programa.
    Muestra un menu interactivo con opciones para el usuario
    """

    while True:
        
        if not USUARIO_ACTUAL: # mientras nadie este logueado
            
            print("\n\n-------------------------")
            print("BIENVENIDO A SUBASTAS.COM")
            print("-------------------------\n")

            print("----------------")
            print("PAGINA DE INICIO")
            print("----------------\n")

            print("1- Registrarse")
            print("2- Iniciar sesion")
            print("3- Salir")
            
            opcion = pedir_entero("Ingrese una opcion valida (1-3): ", 1, 3)          

            if opcion == 1:
                print()
                registrar_usuario()
 
            elif opcion == 2:
                print()
                login()

            elif opcion == 3:
                print()
                print("Gracias por usar SUBASTAS.COM")
                print("Saliendo...\n")
                break

        if USUARIO_ACTUAL:

            if USUARIO_ACTUAL["rol"] == "user":
                print("--------------")
                print("MENU PRINCIPAL")
                print("--------------\n")

                print(f"Usuario: {USUARIO_ACTUAL["nombre"]}")
                print(f"ID: {USUARIO_ACTUAL["id"]}\n")
                print("1- Ver subastastas disponibles")
                print("2- Registrar puja")
                print("3- Generar informe")
                print("4- Cerrar Sesion")
            
                opcion = pedir_entero("Ingrese una opcion valida (1-4): ", 1, 4)
            
                if opcion == 1:
                    print()
                    mostrar_subastas()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()
        
                elif opcion == 2:
                    print()
                    registrar_puja()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()

                elif opcion == 3:
                    print()
                    generar_informe()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()

                elif opcion == 4:
                    print()
                    cerrar_sesion()
            
            else:
                # Si se inicia sesion como admin
                pass
                
 
 
main()
 