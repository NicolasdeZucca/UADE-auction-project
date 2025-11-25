# pylint: disable=C0103
# pylint:disable=C0303

"""
    Este modulo representa la estructura básica de la aplicación.
    Proporciona un menu interactivo para el usuario y se realizan
    llamadas a las funciones necesarias para el desarrollo del programa.
"""
from config.config             import PATH_PUJAS, PATH_SUBASTAS
from data.subastas             import actualizar_subasta, mostrar_subastas, elegir_subasta, crear_subasta, guardar_subastas, generar_id_subasta
from data.usuarios             import obtener_usuarios, crear_usuario, guardar_usuario
from data.pujas                import obtener_pujas, registrar_usuario_puja, guardar_puja
from data.JSONs                import leer_archivo
from utilidades.utils          import pedir_entero
from validaciones.validaciones import validarNombre, validarContrasena, usuario_existe, validar_credenciales, validar_monto_subasta
from datetime                  import datetime, timedelta
 
 
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
        nombre = nombre.strip()

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
                    contrasena = contrasena.strip()

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
        boolean:    True  
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

    if subasta_elegida['monto_actual'] == 0:
        if USUARIO_ACTUAL['saldo'] < subasta_elegida['costo_inicial']:
            print("Su saldo no cubre el costo inicial de esta subasta\n")
            return False
    elif USUARIO_ACTUAL['saldo'] <= subasta_elegida['monto_actual']:
        print("Su saldo no supera el monto actual de la ultima puja en esta subasta.\n")
        return False
 
    # El monto debe ser numerico y positivo
    try:
        monto = pedir_entero("Ingrese un monto a ofertar: ")
 
        monto_validado = validar_monto_subasta(monto, subasta_elegida, USUARIO_ACTUAL)
        
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

    
    usuarios = obtener_usuarios()
    usuarios.remove(USUARIO_ACTUAL)
    USUARIO_ACTUAL['saldo'] -= monto_validado
    usuarios.append(USUARIO_ACTUAL)
    guardar_usuario(usuarios)
    return True
 
def generar_informe():
    """
    Genera informe completo de subastas.
    Solo administradores pueden generar el informe.
    """

    # VALIDACION DE ROL
    if USUARIO_ACTUAL is None or USUARIO_ACTUAL.get("rol") != "admin":
        print("Solo un administrador puede generar el informe completo.\n")
        return False

    print("Generando informe de subastas...\n")

    pujas = leer_archivo(PATH_PUJAS)
    subastas = leer_archivo(PATH_SUBASTAS)

    if not subastas:
        print("No hay subastas para informar.")
        return False

    nombre_archivo = "informe_subastas.txt"

    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:

            archivo.write("========== INFORME COMPLETO DE SUBASTAS ==========\n\n")
            archivo.write(f"Total de subastas registradas: {len(subastas)}\n\n")

            for sub in subastas:

                id_sub = sub["id"]
                nombre = sub["nombre"]
                categoria = sub.get("categoria", "Desconocida")
                estado = sub.get("estado", "N/A")
                costo_inicial = sub.get("costo_inicial", 0)
                ganador = sub.get("ganador") or "Nadie"

                # Fechas
                inicio = sub.get("fecha_inicio")
                fin = sub.get("fecha_fin")

               
                fechaInicio = datetime.fromisoformat(inicio)
                FechaFin = datetime.fromisoformat(fin)
                duracion_minutos = int((FechaFin - fechaInicio).total_seconds() // 60)
                

                # Pujas de esta subasta
                lista = pujas.get(str(id_sub), [])

                archivo.write(f"--- SUBASTA # {id_sub} — {nombre} ---\n")
                archivo.write(f"Categoría: {categoria}\n")
                archivo.write(f"Estado: {estado}\n")
                archivo.write(f"Fecha inicio: {inicio}\n")
                archivo.write(f"Fecha fin: {fin}\n")
                archivo.write(f"Duración total: {duracion_minutos} minutos\n")
                archivo.write(f"Precio inicial: ${costo_inicial}\n")
                archivo.write(f"Ganador: {ganador}\n\n")

                # Estadísticas
                cant_pujas = len(lista)

                if cant_pujas == 0:
                    archivo.write("No hubo pujas en esta subasta.\n\n")
                    continue

                montos = [p["monto"] for p in lista]
                monto_max = max(montos)
                monto_min = min(montos)
                promedio = round(sum(montos) / cant_pujas, 2)

                # Rentabilidad
                if costo_inicial > 0:
                    rentabilidad = ((monto_max - costo_inicial) / costo_inicial) * 100
                else:
                    rentabilidad = 0

                archivo.write("Estadísticas:\n")
                archivo.write(f" - Cantidad de pujas: {cant_pujas}\n")
                archivo.write(f" - Monto máximo: ${monto_max}\n")
                archivo.write(f" - Monto mínimo: ${monto_min}\n")
                archivo.write(f" - Promedio ofertado: ${promedio}\n")
                archivo.write(f" - Rentabilidad: {rentabilidad:.2f}%\n\n")

                # Participantes
                archivo.write("Participantes:\n")
                participantes = {}

                for participante in lista:
                    usr = participante["usuario"]
                    if usr not in participantes:
                        participantes[usr] = []
                    participantes[usr].append(participante["monto"])

                for usuario, montos_usr in participantes.items():
                    total = sum(montos_usr)
                    archivo.write(f" - {usuario}: {len(montos_usr)} pujas, ${total} ofertados\n")

                archivo.write("\n Historial de pujas:\n")

                lista_ordenada = sorted(lista, key=lambda p: p["timestamp"])

                for i, participante in enumerate(lista_ordenada, start=1):
                    archivo.write(
                        f" {i}) {participante['usuario']} | ${participante['monto']} | {participante['timestamp']}\n"
                    )

                archivo.write("\n\n")

        print(f"Informe generado exitosamente en {nombre_archivo}\n")

    except Exception as e:
        print(f"Error generando informe: {e}")
        return False

    # Vista previa
    print("----- VISTA PREVIA -----")
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        print(f.read())
    print("------------------------")

    return True


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
                print()
            
                if confirmacion == "si" or confirmacion == "no":
                    break
                else:
                    print("Opción no válida. Por favor escribe 'si' o 'no'.\n")

            if confirmacion == 'si':
                usuario["solicitud_admin"] = True
                guardar_usuario(usuarios)
                print("Solicitud enviada con éxito, espera a que un admin revise tu peticion\n")
                # se actualiza la variable global para reflejar el cambio en memoria
                USUARIO_ACTUAL = usuario 
            else:
                print("Operación cancelada.\n")
            return

def gestionar_nuevos_admins():
    """
    Funcion para el ADMIN.
    Lista los usuarios que pidieron ser admin y permite aprobarlos.
    """
    print("\n--- GESTIÓN DE SOLICITUDES DE ADMIN ---\n")
    
    usuarios = obtener_usuarios()
    
    # Filtramos los usuarios que tienen la solicitud activa
    candidatos = [usuario for usuario in usuarios if usuario.get("solicitud_admin") is True]
    
    if not candidatos:
        print("no hay solicitudes pendientes en este momento.\n")
        return

    print(f"Hay {len(candidatos)} solicitudes pendientes:\n")
    for u in candidatos:
        print(f"ID: {u['id']} | Usuario: {u['nombre']}")
    
    print("\nIngrese el ID del usuario al que desea DARLE PERMISOS de Administrador.")
    print("(O ingrese '0' para volver atrás)\n")
    
    while True:
        try:
            id_elegido = pedir_entero("ID de usuario a aprobar: ")
            print()
            
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
                        print()

                        if confirmar == "si" or confirmar == "no":
                            break
                    except Exception as e:
                        print("Debe ingresar un id o '0', intente nuevamente...\n")

                if confirmar == "si":
                    #se cambia el rol
                    usuario_a_modificar["rol"] = "admin"
                    #se borra la solicitud
                    del usuario_a_modificar["solicitud_admin"]
                    
                    guardar_usuario(usuarios)
                    print(f"El usuario {usuario_a_modificar['nombre']} ahora es Administrador.\n")
                    return
                else:
                    print("Operación cancelada.\n")
                    return
            else:
                print("ID no es correcto o el usuario NO tiene una solicitud pendiente.\n")
                continue

        except Exception as e:
            print(f"Ocurrió un error: {e}\n")

def cerrar_sesion():
    global USUARIO_ACTUAL

    if not USUARIO_ACTUAL:
        return False, print("No hay un usuario logueado actualmente.")

    else:
        USUARIO_ACTUAL = None
        return True, print("...cerrando sesion..."), 

def reactivar_subasta():
    """
    permite al admin seleccionar una subasta YA FINALIZADA y modificar sus valores (si EL desea) y relanzarla con un NUEVO ID.
    """
    print("\n--- REACTIVAR SUBASTA ---")

    subastas = leer_archivo(PATH_SUBASTAS)

    # se filtran SOLO las finalizadas
    finalizadas = [subasta for subasta in subastas if subasta.get("estado") == "finalizada"]

    if not finalizadas:
        print("No hay subastas finalizadas para reactivar.\n")
        return

    # se muestran las finalizadas para que elija
    print(f"Subastas finalizadas disponibles ({len(finalizadas)}):")
    for sub in finalizadas:
        print(f"ID: {sub['id']} | Nombre: {sub['nombre']} | Terminó: {sub['fecha_fin']}")
    print()

    #eleccion de subasta
    red = True
    while red is True:
        try:
            id_elegido = pedir_entero("Ingrese el ID de la subasta a reactivar (0 para volver): ")
            if id_elegido == 0:
                return
            
            #se busca la subasta original en la lista de finalizadas
            subasta_origen = None
            for subasta in finalizadas:
                if subasta["id"] == id_elegido:
                    subasta_origen = subasta
                    break
            
            if subasta_origen:
                break
            else:
                print("ID invalido o la subasta no esta finalizada, intente nuevamente.")
        except Exception as e:
            print(f"Error al ingresar el ID: {e}")

    print(f"\n--- Configurando nueva subasta basada en: '{subasta_origen['nombre']}")

    #se pregunta si desea modificar el precio 
    nuevo_costo = subasta_origen['costo_inicial']
    print(f"Costo inicial original: ${nuevo_costo}")
    red = True
    while red is True:
        cambiar_precio = input("Desea modificar el precio inicial? (si/no): ").strip().lower()
        if cambiar_precio == "si":
            nuevo_costo = pedir_entero("Ingrese el nuevo precio inicial: ", 1)
            break
        elif cambiar_precio == "no":
            break
        else:
            print("Por favor ingrese 'si' o 'no'.")

    # se define nueva duración 
    print("\nindique la duracion para la nueva ronda.")
    duracion_min = pedir_entero("Ingrese la duracion en min: ", 10)
    
    # se calcula la fecha
    ahora = datetime.now()
    duracion_segundos = duracion_min * 60
    fecha_fin = (ahora + timedelta(seconds=duracion_segundos)).isoformat(timespec="seconds")    #se usa isoformat para guardar bien la fecha

    # se genera un ID nuevo xq es otra subasta por mas q se repita
    nuevo_id = generar_id_subasta() 

    nueva_subasta = {
        "id": nuevo_id,
        "nombre": subasta_origen["nombre"],       # mismo nombre
        "categoria": subasta_origen["categoria"], # misma categoria
        "descripcion": subasta_origen["descripcion"], #misma descripcion
        "costo_inicial": nuevo_costo,             # posible nuevo precio o no
        "estado": "activa",                       
        "fecha_inicio": str(ahora.isoformat(timespec="seconds")),  #se usa isoformat para guardar bien la fecha
        "fecha_fin": str(fecha_fin),
        "monto_actual": 0,                        #se resetean las pujas
        "ganador": None                           #se resetea el ganador
    }

    subastas.append(nueva_subasta)
    guardar_subastas(subastas)
    print(f"\nexito: subasta reactivada con el NUEVO ID: {nuevo_id}")

def solicitar_dinero():
    """
    Realiza todo el proceso para solicitar carga de dinero con sus validaciones.
    """
    global USUARIO_ACTUAL

    usuarios = obtener_usuarios()

    print("--- SOLICITUD DE DINERO ---\n")

    print("Para cargar dinero debe realizar una transferencia al alias: SUBASTAS.COM.MP")
    print("Luego debe ingresar el valor del deposito y el Nro de comprobante de la transferencia y esperar a la confirmacion de un administrador. \n")

    while True:
        dineroTransferido = pedir_entero("Ingrese el valor de la transferencia (minimo de transferencia: $5000): $", 5000)
        print()

        nroComprobante = pedir_entero("ingrese el Nro de comprobante (entre 1000-9999): Nro-", 1000,9999)
        print()

        break

    usuarios.remove(USUARIO_ACTUAL)

    USUARIO_ACTUAL["saldo_pendiente"]+=dineroTransferido

    usuarios.append(USUARIO_ACTUAL)

    guardar_usuario(usuarios)

    print(f"Su solicitud de ${dineroTransferido} ha sido enviada, espere a que un administrador la acepte,\n")
    
    

def solicitudes_dinero():
    """
    Realiza todo el proceso de aceptar o denegar una solicitud de dinero
    """

    usuarios = obtener_usuarios()

    usuariosConSolicitud = [user for user in usuarios if user['saldo_pendiente'] != 0]

    idConSolicitud = [user['id'] for user in usuariosConSolicitud]

    print("--- SOLICITUDES DE DINERO ---\n")

    print("Usted obtendra una lista con los usuarios que tienen pendiente una solicitud de dinero.")
    print("La lista le mostrara el ID y el valor del saldo a aceptar.\n")

    input("Ingrese 'enter' para continuar: ")
    print()

    if not usuariosConSolicitud:
        print("No hay solicitudes de usuarios.")
        return False

    for usuario in usuariosConSolicitud:

        print("----------------------")
        print(f"ID de Usuario: {usuario['id']}")
        print(f"Saldo a aprobar: ${usuario['saldo_pendiente']}")
        print("----------------------\n")

    while True:
        idSeleccionado = pedir_entero("Ingrese el valor del ID a manejar: ")
        print()
        
        if idSeleccionado in idConSolicitud:
            if idSeleccionado == USUARIO_ACTUAL['id']:
                print("Usted no puede aceptar su propia solicitud.")
                print("Volviendo al menu de administrador...\n")
                break

            print("Elija entre las opciones:")
            print(f"1- Aceptar la solicitud del ID {idSeleccionado}")
            print(f"2- Denegar la solicitud del ID {idSeleccionado}")
            print("3- Cancelar operacion sin cambios en los saldos.")

            opcion = pedir_entero("Ingrese la opcion seleccionada (1-3): ", 1, 3)
            print()


            if opcion == 1:
                usuarioAceptado = next((usuario for usuario in usuarios if usuario['id'] == idSeleccionado),None)
                usuarios.remove(usuarioAceptado)
                saldoACargar = usuarioAceptado['saldo_pendiente']
                usuarioAceptado['saldo'] += saldoACargar
                usuarioAceptado['saldo_pendiente']=0
                usuarios.append(usuarioAceptado)
                guardar_usuario(usuarios)
                print(f"La solicitud del ID {idSeleccionado}, fue aceptada con exito.\n")
                print("Volviendo al menu de administrador...\n")
                break

            elif opcion == 2:
                usuarioDenegado = next((usuario for usuario in usuarios if usuario['id'] == idSeleccionado),None)
                usuarios.remove(usuarioDenegado)
                usuarioDenegado['saldo_pendiente']=0
                usuarios.append(usuarioDenegado)
                guardar_usuario(usuarios)
                print(f"La solicitud del ID {idSeleccionado}, fue denegada con exito.\n")
                print("Volviendo al menu de administrador...\n")
                break

            elif opcion == 3:
                print("Volviendo al menu de administrador sin cambios...\n")
                break


        else:
            print("Debe elegir un ID de la lista, intente nuevamente...\n")
            continue

def revocar_admins():
    """
    realiza todo el proceso de 
    """
    print("--- REVOCAR ADMINS ---\n")

    print("Usted vera una lista con los usuarios con el rol de administrador en el sistema y elegira si revocar o no ese rol.\n")

    usuarios = obtener_usuarios()

    usuarios.remove(USUARIO_ACTUAL)

    usuariosAdmin = [user for user in usuarios if user['rol']=="admin"]

    idAdmin = [user['id'] for user in usuariosAdmin]

    if not usuariosAdmin:
        input("Presione 'enter' para contiuar...")
        print()
        print("No existen usuarios con el rol de administrador aparte de usted.\n")
        return False
    else:
        input("Presione 'enter' para ver la lista de admins")
        print()
        for usuario in usuariosAdmin:
            print("-----------------------------")
            print(f"ID del usuario admin: {usuario['id']}")
            print(f"Nombre del usuario admin: {usuario['nombre']}")
            print("-----------------------------\n")

    while True:
        idSeleccionado = pedir_entero("Ingrese el valor del ID a manejar: ")
        print()
        
        if idSeleccionado in idAdmin:
            print("Elija entre las opciones:")
            print(f"1- Revocar el permiso de admin al ID {idSeleccionado}")
            print("2- Cancelar operacion sin cambios en los roles.")

            opcion = pedir_entero("Ingrese la opcion seleccionada (1-2): ", 1, 2)
            print()


            if opcion == 1:
                usuarioAceptado = next((usuario for usuario in usuarios if usuario['id'] == idSeleccionado),None)
                usuarios.remove(usuarioAceptado)
                usuario['rol'] = "user"
                usuarios.append(usuarioAceptado)
                usuarios.append(USUARIO_ACTUAL)
                guardar_usuario(usuarios)
                print(f"Se revoco el permiso de admin del ID {idSeleccionado} con exito\n")
                print("Volviendo al menu de administrador...\n")
                break

            elif opcion == 2:
                print("Volviendo al menu de administrador sin cambios...\n")
                break


        else:
            print("Debe elegir un ID de la lista, intente nuevamente...\n")
            continue

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
                print("MENU USUARIO")
                print("--------------\n")

                print(f"Usuario: {USUARIO_ACTUAL['nombre']}")
                print(f"ID: {USUARIO_ACTUAL['id']}")
                print(f"Saldo actual: ${USUARIO_ACTUAL['saldo']}")
                if "saldo_pendiente" not in USUARIO_ACTUAL:
                    print()
                else:
                    print(f"Saldo pendiente: ${USUARIO_ACTUAL['saldo_pendiente']}\n")
                print("1- Ver subastastas disponibles")
                print("2- Registrar puja")
                print("3- Solicitar carga de dinero")
                print("4- Solicitar ser Admin")
                print("5- Cerrar Sesion")
                 
            
                opcion = pedir_entero("Ingrese una opcion valida (1-5): ", 1, 5)
            
                if opcion == 1:
                    print()
                    mostrar_subastas()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()
        
                elif opcion == 2:
                    print()
                    if USUARIO_ACTUAL['saldo'] == 0:
                        print("Su saldo es 0, no puede ofertar en ninguna subasta.")
                    else:
                        registrar_puja()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()

                elif opcion == 3:
                    print()
                    solicitar_dinero()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()

                elif opcion == 4:
                    print()
                    solicitar_rol_admin()
                    input("\nPresione 'enter' para volver al menu principal")
                
                elif opcion == 5:
                    print()
                    cerrar_sesion()
            
            else:
                print("------------------")
                print("MENU ADMINISTRADOR")
                print("------------------\n")

                print(f"Usuario: {USUARIO_ACTUAL['nombre']}")
                print(f"ID: {USUARIO_ACTUAL['id']}")
                print(f"Saldo actual: ${USUARIO_ACTUAL['saldo']}")
                if "saldo_pendiente" not in USUARIO_ACTUAL:
                    print()
                else:
                    print(f"Saldo pendiente: ${USUARIO_ACTUAL['saldo_pendiente']}\n")
                print("1- Ver subastastas disponibles")
                print("2- Registrar puja")
                print("3- Solicitar dinero")
                print("4- Crear subasta")
                print("5- Generar informe")
                print("6- Gestionar cargas de dinero")
                print("7- Gestionar nuevos admins") 
                print("8- Revocar permisos de admins")
                print("9- Reactivar subastas") 
                print("10- Cerrar Sesion")

                opcion = pedir_entero("Ingrese una opcion valida (1-10): ", 1, 10)

                if opcion == 1:
                    print()
                    mostrar_subastas()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()

                elif opcion == 2:
                    print()
                    if USUARIO_ACTUAL['saldo'] == 0:
                        print("Su saldo es 0, no puede ofertar en ninguna subasta.")
                    else:
                        registrar_puja()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()

                elif opcion == 3:
                    print()
                    solicitar_dinero()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()
                
                elif opcion == 4:
                    print()
                    crear_subasta()

                elif opcion == 5:
                    print()
                    generar_informe()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()

                elif opcion == 6:
                    print()
                    solicitudes_dinero()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()
                    pass

                elif opcion == 7: 
                    print()
                    gestionar_nuevos_admins()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()

                elif opcion == 8:
                    print()
                    revocar_admins()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()
                
                elif opcion == 9: 
                    print()
                    reactivar_subasta()
                    input("\nPresione 'enter' para volver al menu principal")
                    print()

                elif opcion == 10:
                    print()
                    cerrar_sesion()
                
 
 
main()
 