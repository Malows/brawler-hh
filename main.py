"""
Brawler Bot, para harem heroes, hecho en python 2.7 con el fin de reducir el tamanio del ejecutable
Y que sea llamado stand-alone desde un crontable
"""
from sys import argv
from http.client import HTTPConnection
from functools import reduce
import json
from bs4 import BeautifulSoup
from datos import DOMAIN, ENEMIGOS
from respuestas import respuesta_pelea, respuesta_unzip_http
from headers import make_header
from parametros import params_pelea, encodear_parametro


def extraer_datos_de_troll(unparsed):
    """ Extrae los datos de pelea para formar los params """
    donde_esta_id = unparsed.find('id_troll')

    open_llave = donde_esta_id
    while not unparsed[open_llave] == "{":
        open_llave -= 1

    close_llave = donde_esta_id
    while not unparsed[close_llave] == "}":
        close_llave += 1

    datos = unparsed[open_llave:close_llave + 1]
    print('payload de datos', datos)
    return json.loads(datos)


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

    headers = make_header('world/{}'.format(enemy['id_world']), explorar=True)
    params = encodear_parametro({'id_troll': enemy['id_troll']})

    conn.request('GET', '/battle.html?' + params, headers=headers)
    descomprimido = respuesta_unzip_http(conn.getresponse()).decode('utf-8')

    params = params_pelea(extraer_datos_de_troll(descomprimido))
    print('parametros antes de la pelea', params)

    headers = make_header('battle.htm?id_troll={}'.format(enemy['id_troll']))
    print('headers antes de la pelea', headers)

    conn.request('POST', '/ajax.php', params, headers)
    return respuesta_pelea(conn.getresponse())


def get_info_troll(enemy, conn=None):
    """ scrapper de datos de los trolls """
    if not conn:
        conn = HTTPConnection(DOMAIN)

    headers = make_header('world/{}'.format(enemy['id_world']), explorar=True)
    params = encodear_parametro({'id_troll': enemy['id_troll']})

    conn.request('GET', '/battle.html?' + params, headers=headers)
    descomprimido = respuesta_unzip_http(conn.getresponse())

    soup = BeautifulSoup(descomprimido, 'html.parser')
    set_relativo = soup.find_all('div', class_='slot girl-slot')
    enemy['chicas_cautivas'] = len(set_relativo) // 2
    return enemy


def get_info_cantidad_energia(conn=HTTPConnection(DOMAIN)):
    """ scrapper que obtiene la cantidad de energia de la cuenta """
    headers = make_header('home.html', True)
    conn.request('GET', '/home.html', headers=headers)
    descomprimido = respuesta_unzip_http(conn.getresponse())

    soup = BeautifulSoup(descomprimido, 'html.parser')
    energia = soup.find('span', {'hero': 'energy_fight'})
    try:
        return int(energia.string)
    except:
        return energia.string


def definir_oponente(conn=None):
    """
    Hace request para ver que troll, ordenado de menor a mayor aun tiene alguna chica cautiva
    :param conn: HTTPConnection, opcional. Si se pasa, se evita crear una nueva conexion.
    Sino se instancia una nueva
    :return: El troll de nivel mas bajo que aun tenga una chica cautiva
    """
    lista_enemigos = ENEMIGOS

    if not conn:
        conn = HTTPConnection(DOMAIN)

    if len(argv) >= 2:
        lista_hidratada = list(
            map(get_info_troll, filter(lambda x: str(x['id_troll']) in argv[1:], ENEMIGOS))
        )
        if reduce(lambda c, x: c + x['chicas_cautivas'], lista_hidratada, 0) > 0:
            lista_enemigos = lista_hidratada

    for enemy in lista_enemigos:
        enemy = get_info_troll(enemy, conn)

        if enemy['chicas_cautivas'] != 0:
            return enemy


def pelear():
    """
    Funcion que pelea contra los trolls
    :return: None
    """
    conn = HTTPConnection(DOMAIN)
    enemy = definir_oponente(conn)
    energia = get_info_cantidad_energia(conn)

    respuestas = list(
        filter(_str_energy, [pelear_contra_troll(enemy, conn) for _ in range(energia)])
    )

    es_dinero = list(filter(_numero, respuestas))
    no_es_dinero = list(filter(_dict, respuestas))

    total = reduce(lambda c, x: c + x, es_dinero, 0)
    with open('brawler.log', 'a') as file:
        file.write("Recaudaste de {} $ {}\n".format(enemy['nombre'], total))

        if no_es_dinero:
            file.write("\nY tambien conseguiste otras cosas\n")
            file.write(no_es_dinero)


def _str_energy(elem):
    if isinstance(elem, str) and "Not enough energy" in elem:
        return False
    return True

def _numero(elem):
    return isinstance(elem, int)

def _dict(elem):
    return isinstance(elem, dict)


# print(definir_enemigo_arena())
# print(len(argv))
# print(argv)
# print(definir_oponente())
pelear()
