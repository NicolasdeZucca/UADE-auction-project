# pylint: disable=C0103
# pylint:disable=C0303

"""
    Este modulo representa la estructura básica de la aplicación.
    Proporciona un menu interactivo para el usuario y se realizan
    llamadas a las funciones necesarias para el desarrollo del programa.
"""
import os
from data.subastas             import actualizar_subasta, mostrar_subastas, elegir_subasta, crear_subasta
from data.usuarios             import obtener_usuarios, crear_usuario, guardar_usuario
from data.pujas                import obtener_pujas, registrar_usuario_puja, guardar_puja
from data.JSONs                import leer_archivo
from config.config             import PATH_PUJAS, PATH_SUBASTAS, PATH_USUARIOS
from utilidades.utils          import pedir_entero
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
    
    if subasta_elegida["estado"] != "activa":
        print("La subasta ya finalizó. No se pueden registrar nuevas pujas.\n")
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
    Genera informe completo de subastas y lo guarda en un archivo de txt, 
    calcula estadisticas y exporta los resultados.
    """
    
    print("Generando informe de subastas...")

    # Se leen los datos de los archivos JSON 
    pujas = leer_archivo(PATH_PUJAS)       
    subastas = leer_archivo(PATH_SUBASTAS)

    if not subastas:
        print("No hay subastas para informar.")
        return

    nombre_archivo = "informe_subastas.txt"
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:            
            archivo.write("INFORME DE SUBASTAS\n")
            archivo.write(f"Total de subastas registradas: {len(subastas)}\n\n") 

            for subasta in subastas:
                id_subasta = subasta.get("id")
                nombre_subasta = subasta.get("nombre", "Sin nombre")
                categoria = subasta.get("categoria", "Sin categoría")
                costo_inicial = subasta.get("costo_inicial", 0)
    
                # Accedemos al diccionario de pujas usando el ID de la subasta como clave (string)
                pujas_de_subasta = pujas.get(str(id_subasta), [])

                #estadisticas
                cantidad_pujas = len(pujas_de_subasta) 
                monto_maximo = 0
                monto_minimo = 0
                promedio_pujas = 0
                rentabilidad = 0.0

                if cantidad_pujas > 0:
                    # Creamos una lista solo con los montos para los cálculos
                    lista_montos = [p.get("monto", 0) for p in pujas_de_subasta]
                    
                    monto_maximo = max(lista_montos) 
                    monto_minimo = min(lista_montos)
                    promedio_pujas = sum(lista_montos) / cantidad_pujas 
                    #CALCULO DE RENTABILIDAD
                    #FORMULA = ((monto maximo  - costo inicial) / costo inicial) * 100
                    if costo_inicial > 0:
                        ganancia = monto_maximo - costo_inicial
                        rentabilidad = (ganancia / costo_inicial) * 100

                # Escribimos los detalles en el archivo
                archivo.write(f"ID: {id_subasta} | Subasta: {nombre_subasta}\n")
                archivo.write(f"Categoría: {categoria}\n")
                archivo.write(f"Precio Base: ${costo_inicial}\n")
                archivo.write(f"Estado: {subasta.get('estado', 'Desconocido')}\n")
                archivo.write(f"Ganador actual: {subasta.get('ganador') if subasta.get('ganador') else 'Nadie'}\n")
                archivo.write(f" >> Cantidad de pujas: {cantidad_pujas}\n")
                archivo.write(f" >> Puja máxima: ${monto_maximo}\n")
                archivo.write(f" >> Puja mínima: ${monto_minimo}\n")
                archivo.write(f" >> Promedio ofertado: ${promedio_pujas}\n") 
                signo = "+" if rentabilidad > 0 else ""#se muestra la rentabilidad con un signo '+' si es positiva
                archivo.write(f"   * Rentabilidad:{signo}{rentabilidad:}% (sobre precio base ({costo_inicial}))\n")
                
        print(f"Informe generado exitosamente en {nombre_archivo}")
        
    except Exception as e: 
        print(f"Error al generar el informe: {e}")
        
    # vista previa
    try: 
        print("\n--- VISTA PREVIA DEL INFORME ---")
        with open(nombre_archivo, 'r', encoding='utf-8') as f_lectura: 
            contenido = f_lectura.read() 
            print(contenido)
        print("--------------------------------")
    except Exception as e: 
        print(f"No se pudo leer el archivo generado: {e}")
def solicitar_rol_admin():
    """
    permite a un usuario normal solicitar permisos de administrador
    """
    global USUARIO_ACTUAL
    print("\n--- SOLICITUD DE ADMINISTRADOR ---")
    
    usuarios = obtener_usuarios()
    
    for usuario in usuarios:# se busca al usuario actual en la lista para modificarlo
        if usuario["id"] == USUARIO_ACTUAL["id"]:
            
            if usuario.get("solicitud_admin") is True:
                print("Ya has enviado una solicitud previamente, espera a que un administrador la apruebe")
                return
            
            while True:
                confirmacion = input("estas seguro que deseas solicitar permisos de Administrador? (si/no): ").lower().strip()
            
                if confirmacion == "si" or confirmacion == "no":
                    break
                else:
                    print("Opción no válida. Por favor escribe 'si' o 'no'.\n")

            if confirmacion == 'si':
                usuario["solicitud_admin"] = True
                guardar_usuario(usuarios)
                print("Solicitud enviada con éxito, espera a que un admin revise tu peticion")
                # se actualiza la variable global para reflejar el cambio en memoria
                USUARIO_ACTUAL = usuario 
            else:
                print("Operación cancelada.")
            return

def gestionar_nuevos_admins():
    """
    Funcion para el ADMIN.
    Lista los usuarios que pidieron ser admin y permite aprobarlos.
    """
    print("\n--- GESTIÓN DE SOLICITUDES DE ADMIN ---")
    
    usuarios = obtener_usuarios()
    
    # Filtramos los usuarios que tienen la solicitud activa
    candidatos = [usuario for usuario in usuarios if usuario.get("solicitud_admin") is True]
    
    if not candidatos:
        print("no hay solicitudes pendientes en este momento.")
        return

    print(f"Hay {len(candidatos)} solicitudes pendientes:\n")
    for u in candidatos:
        print(f"ID: {u['id']} | Usuario: {u['nombre']}")
    
    print("\nIngrese el ID del usuario al que desea DARLE PERMISOS de Administrador.")
    print("(O ingrese '0' para volver atrás)")
    
    while True:
        try:
            id_elegido = pedir_entero("ID de usuario a aprobar: ")
            
            if id_elegido == 0:
                return

            usuario_a_modificar = None
            
            #se busca el usuario en la lista principal 
            for usuario in usuarios:
                if usuario["id"] == id_elegido and usuario.get("solicitud_admin") is True:
                    usuario_a_modificar = usuario
                    break
            
            if usuario_a_modificar:
                while True:
                    try:
                        confirmar = input(f"¿Convertir a {usuario_a_modificar['nombre']} en ADMIN? (si/no): ").strip().lower()
                        if confirmar == "si" or confirmar == "no":
                            break
                    except Exception as e:
                        print("Debe ingresar un id o '0', intente nuevamente...")

                if confirmar == "si":
                    #se cambia el rol
                    usuario_a_modificar["rol"] = "admin"
                    #se borra la solicitud
                    del usuario_a_modificar["solicitud_admin"]
                    
                    guardar_usuario(usuarios)
                    print(f"El usuario {usuario_a_modificar['nombre']} ahora es Administrador.")
                    return
                else:
                    print("Operación cancelada.")
                    return
            else:
                print("ID no es correcto o el usuario NO tiene una solicitud pendiente.")
                continue

        except Exception as e:
            print(f"Ocurrió un error: {e}")

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

                print(f"Usuario: {USUARIO_ACTUAL['nombre']}")
                print(f"ID: {USUARIO_ACTUAL['id']}\n")
                print("1- Ver subastastas disponibles")
                print("2- Registrar puja")
                print("3- Generar informe")
                print("4- Cerrar Sesion")
                print("5- Solicitar ser Admin") 
            
                opcion = pedir_entero("Ingrese una opcion valida (1-5): ", 1, 5)
            
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
                
                elif opcion == 5:
                    print()
                    solicitar_rol_admin()
                    input("\nPresione 'enter' para volver al menu principal")
            
            else:
                print("------------------")
                print("MENU ADMINISTRADOR")
                print("------------------\n")

                print(f"Usuario: {USUARIO_ACTUAL['nombre']}")
                print(f"ID: {USUARIO_ACTUAL['id']}\n")
                print("1- Ver subastastas disponibles")
                print("2- Crear subasta")
                print("3- Generar informe")
                print("4- Gestionar nuevos admins") 
                print("5- Cerrar Sesion")

                opcion = pedir_entero("Ingrese una opcion valida (1-5): ", 1, 5)

                if opcion == 1:
                    print()
                    mostrar_subastas()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()
                
                elif opcion == 2:
                    print()
                    crear_subasta()

                elif opcion == 3:
                    print()
                    generar_informe()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()

                elif opcion == 4: 
                    print()
                    gestionar_nuevos_admins()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()

                elif opcion == 5:
                    print()
                    cerrar_sesion()
                
 
 
main()
 