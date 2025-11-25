import pytest
from validaciones.validaciones import (
    validarNombre,
    validarContrasena,
    usuario_existe,
    validar_credenciales,
    validar_monto_subasta
)
#prueba para validar validarNombre
def test_nombre_valido():
    """prueba que un nombre correcto devuelva true"""
    assert validarNombre('UsuarioValido1') is True

def test_nombre_corto_invalido():
    """prueba que un nombre muy corto devuelva false"""
    assert validarNombre('U') is False

def test_nombre_con_simbolos_invalido():
    """prueba que un nombre con simbolos prohibidos devuelva false"""
    assert validarNombre("Usuario!") is False
#pruebas para validar validarContrasena
def test_password_valida():
    """prueba una contraseña que cumple todos los requisitos"""
    assert validarContrasena('PassValida123!') is True

def test_password_sin_mayuscula():
    """prueba que falle si falta la mayuscula"""
    assert validarContrasena("passvalida123!") is False

def test_password_sin_numero():
    """prueba que falle si falta el numero"""
    assert validarContrasena("PassValida!") is False

def test_password_sin_simbolo():
    """prueba que falle si falta el caracter especial"""
    assert validarContrasena("PassValida123") is False

def test_password_corta():
    """prueba que falle si es muy corta"""
    assert validarContrasena("P1!") is False
#prueba para ver si un usuario existe
def test_usuario_si_existe_mock():
    """
    prueba que la funcion encuentre a un usuario dentro de una lista falsa o mock
    NO lee el archivo real
    """
    lista_mock = [
        {"nombre": "Nico", "password": "123"}, 
        {"nombre": "Pepe", "password": "abc"}
    ]    
    resultado = usuario_existe("Nico", lista_mock)
    assert resultado is True

def test_usuario_no_existe_mock():
    """prueba que devuelva false si el usuario no esta en la lista falsa o mock"""
    lista_mock = [{"nombre": "Nico"}]    
    resultado = usuario_existe("Franco", lista_mock)
    assert resultado is False
#prueba de credenciales
def test_credenciales_correctas_falsa():
    """prueba un login exitoso con datos falsos"""
    lista_mock = [{"nombre": "admin_test", "password": "123"}]    
    resultado = validar_credenciales("admin_test", "123", lista_mock)
    
    assert resultado is not False
    assert resultado["nombre"] == "admin_test"

def test_credenciales_password_incorrecta_mock():
    """prueba un login fallido por contraseña incorrecta"""
    lista_mock = [{"nombre": "admin_test", "password": "123"}]
    
    resultado = validar_credenciales("admin_test", "clave_erronea", lista_mock)
    assert resultado is False

def test_credenciales_usuario_inexistente_mock():
    """prueba un login fallido porque el usuario no existe en la lista"""
    lista_mock = [{"nombre": "admin_test", "password": "123"}]
    
    resultado = validar_credenciales("usuario_fantasma", "123", lista_mock)
    assert resultado is False
# pruebas monto subasta
def test_monto_subasta_cero_es_invalido():
    """prueba que un monto de 0 sea rechazado"""
    subasta_mock = {"costo_inicial": 100, "monto_actual": 0}
    usuario_mock = {"saldo": 5000}
    resultado = validar_monto_subasta(0, subasta_mock, usuario_mock)
    assert resultado is False

def test_monto_valido_inicial():
    """
    prueba una oferta valida inicial (mayor al costo base).
    """
    subasta_mock = {"costo_inicial": 100, "monto_actual": 0}
    usuario_mock = {"saldo": 5000}
    resultado = validar_monto_subasta(150, subasta_mock, usuario_mock)
    assert resultado == 150

def test_monto_valido_supera_puja():
    """
    prueba una oferta valida que supera la puja actual
    """
    subasta_mock = {"costo_inicial": 100, "monto_actual": 200}
    usuario_mock = {"saldo": 5000}
    resultado = validar_monto_subasta(300, subasta_mock,usuario_mock)
    assert resultado == 300