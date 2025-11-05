import random
 
def generate_ID():
    """
    generate_ID genera un ID random a cada usuario registrado
 
    Returns:
        int: un numero random [1000-5000]
    """
    return random.randint(1000,5001)