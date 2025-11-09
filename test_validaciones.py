from validaciones.validaciones import(
    validarNombreContrasena,
    usuario_existe,
    validar_credenciales,
    validar_monto_subasta
)

#prueba para validarNombreContrasena 
def test_nombre_y_password_validos():
    '''
    prueba el caso de exito con un nombre y un pass correctos.
    '''
    resultado = validarNombreContrasena('UsuarioValido1', 'PassValida123!')
    assert resultado [0] is True

def test_nombre_corto_invalido ():
    '''
    prueba un nombre muy corto
    '''
    resultado = validarNombreContrasena('U', 'PassValida123!')
    assert resultado [0] is False
    assert 'Nombre inválido' in resultado[1] 

def test_nombre_con_simbolos_invalido():
    """
    prueba un nombre con caracteres no permitidos
    """
    resultado = validarNombreContrasena("Usuario!", "PassValida123!")
    assert resultado[0] is False
    assert "Nombre inválido" in resultado[1]

def test_password_sin_mayuscula():
    """
    prueba una pass sin mayuscula
    """
    resultado = validarNombreContrasena("UsuarioValido1", "passvalida123!")
    assert resultado[0] is False
    assert "Contraseña inválida" in resultado[1]

def test_password_sin_numero():
    """
    prueba una password sin numero
    """
    resultado = validarNombreContrasena("UsuarioValido1", "PassValida!")
    assert resultado[0] is False
    assert "Contraseña inválida" in resultado[1]

def test_password_sin_simbolo():
    """
    prueba una password sin simbolo
    """
    resultado = validarNombreContrasena("UsuarioValido1", "PassValida123")
    assert resultado[0] is False
    assert "Contraseña inválida" in resultado[1]

def test_password_corta():
    """
    prueba una password demasiado corto
    """
    resultado = validarNombreContrasena("UsuarioValido1", "P1!")
    assert resultado[0] is False
    assert "Contraseña inválida" in resultado[1]


#puebas para el usuario que existe
def test_usuario_si_existe():
    """
    prueba que la validacion de un usuario que SI está en la lista
    """
    lista_mock = [{"nombre": "Nico"}, {"nombre": "Pepe"}]
    #la funcion en caso de que sea verdadero devuelve (true, "mensaje") 
    resultado = usuario_existe("Nico", lista_mock)
    assert resultado[0] is True

def test_usuario_no_existe():
    """
    prueba la validacion de un usuario que NO está en la lista
    """
    lista_mock = [{"nombre": "Nico"}, {"nombre": "Pepe"}]
    #la funcion en caso de que sea falso devuelve (false, "mensaje") 
    resultado = usuario_existe("Franco", lista_mock)
    assert resultado[0] is False