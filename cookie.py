"""
Modulo que maneja la extraccion de la cookie del archivo de recovery
"""

from datos import SESSION_NAME

def get_cookie():
    """
    Devuelve el valor de cookie de sesion para agregar a los headers
    :return: devuelve el header element parseado para agregar
    """
    with open('nutaku.session', 'r') as file:
        value = file.readline().replace('\n', '')
        return "lang=en; {}={}; HAPBK=web1".format(SESSION_NAME, value)
