"""
Modulo que maneja la extraccion de la cookie del archivo de recovery
"""

from os import path, listdir, environ
import lz4
from datos import SESSION_NAME, DOMAIN


def ruta_sesiones_firefox():
    """ Busca, en un usuario linux, el archivo de recovery de firefox y devuelve la ruta """
    not_dev_edition = lambda x: 'default' in x and 'dev-edition' not in x

    lugar = path.abspath(path.join(environ['HOME'], '.mozilla/firefox'))
    firefox_settings = [path.join(lugar, x) for x in listdir(lugar) if not_dev_edition(x)][0]
    return path.join(firefox_settings, 'sessionstore-backups/recovery.jsonlz4')


def extraer_datos_cookie(ruta):
    """
    Recibe la ruta del archivo recovery, el nombre de la sesion y el host.
    Devuelve el valor de la sesion
    """
    with open(ruta, mode="rb") as archivo:
        _ = archivo.read(8)
        return lz4.block.decompress(archivo.read()).decode('utf-8')


def devolver_value_cookie(data):
    """
    Recive la data del archivo recovery, el host y el nombre de la sesion para
    devolver el valor
    """
    host = '"host":"{}"'.format(DOMAIN)
    indice = data.find(SESSION_NAME)
    desde = data.find(host, indice - 100, indice)
    if desde == -1:
        desde = data.find(host, indice - 200)
    if '"value"' in data[desde:indice]:
        parte = data[desde:indice].split('"value":')[1]
        return parte[1: parte.find('","')]


def cookie_value(ruta=ruta_sesiones_firefox()):
    """
    A un archivo, le aplica la extraccion del valor de la cookie
    :param ruta: opcional, la ruta del archivo de donde sacar la cookie
    :return: el valor almacenado en el archivo de recovery
    """
    datos = extraer_datos_cookie(ruta)
    return devolver_value_cookie(datos)

def parsed_cookie(ruta=None):
    """
    Devuelve el valor de cookie de sesion para agregar a los headers
    :param ruta: opcional, la ruta al archivo de recovery
    :return: devuelve el header element parseado para agregar
    """
    value = cookie_value(ruta) if ruta else cookie_value()
    return "lang=en; {}={}".format(SESSION_NAME, value)
