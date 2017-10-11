"""
Brawler Bot, para harem heroes, hecho en python 2.7 con el fin de reducir el tamanio del ejecutable
Y que sea llamado stand-alone desde un crontable
"""
from http.client import HTTPConnection
from functools import reduce
from bs4 import BeautifulSoup
from datos import DOMAIN, ENEMIGOS
from respuestas import respuesta_pelea, respuesta_unzip_http
from headers import make_header
from parametros import params_pelea, encodear_parametro


def pelear_contra_troll(enemy, conn=None):
    """
    Esta funcion recibe un enemigo, y opcionalmente una conexion compartida
    Pelea contra el enemigo una vez y devuelve una respuesta parseada de la pelea
    :param enemy:
    :param conn:
    :return:
    """
    if not conn:
        conn = HTTPConnection(DOMAIN)

    params = params_pelea(enemy)
    headers = make_header('battle.htm?id_troll={}'.format(enemy['id_troll']))

    conn.request('POST', '/ajax.php', params, headers)
    return respuesta_pelea(conn.getresponse())


def definir_oponente(conn=None):
    """
    Hace request para ver que troll, ordenado de menor a mayor aun tiene alguna chica cautiva
    :param conn: HTTPConnection, opcional. Si se pasa, se evita crear una nueva conexion.
    Sino se instancia una nueva
    :return: El troll de nivel mas bajo que aun tenga una chica cautiva
    """
    if not conn:
        conn = HTTPConnection(DOMAIN)
    for enemy in ENEMIGOS:
        headers = make_header('world/{}'.format(enemy['id_world']), explorar=True)
        params = encodear_parametro({'id_troll': enemy['id_troll']})

        conn.request('GET', '/battle.html?'+params, headers=headers)
        descomprimido = respuesta_unzip_http(conn.getresponse())

        soup = BeautifulSoup(descomprimido, 'html.parser')
        set_relativo = soup.find_all('div', class_='slot girl-slot')

        if len(set_relativo) // 2 != 0:
            return enemy


def pelear():
    """
    Funcion que pelea contra los trolls
    :return: None
    """
    conn = HTTPConnection(DOMAIN)
    enemy = definir_oponente(conn)

    respuestas = list(filter(_str_energy, [pelear_contra_troll(enemy, conn) for _ in range(10)]))

    es_dinero = list(filter(_numero, respuestas))
    no_es_dinero = list(filter(_dict, respuestas))

    total = reduce(lambda c, x: c + x, es_dinero, 0)
    print("\nRecaudaste $", total)

    if no_es_dinero:
        print("\nY tambien conseguiste otras cosas\n")
        print(no_es_dinero)


def _str_energy(elem):
    if isinstance(elem, str) and "Not enough energy" in elem:
        return False
    return True

def _numero(elem):
    return isinstance(elem, int)

def _dict(elem):
    return isinstance(elem, dict)


pelear()
