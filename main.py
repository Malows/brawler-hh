"""
Brawler Bot, para harem heroes, hecho en python 2.7 con el fin de reducir el tamanio del ejecutable
Y que sea llamado stand-alone desde un crontable
"""
from sys import argv
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


def get_info_troll(enemy, conn=None):

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
        lista_hidratada = list(map(get_info_troll, filter( lambda x: str(x['id_troll']) in argv[1:], ENEMIGOS )))

    if reduce(lambda c,x: c + x['chicas_cautivas'], lista_hidratada, 0) > 0:
        lista_enemigos = lista_hidratada

    for enemy in lista_enemigos:
        enemy = get_info_troll(enemy, conn)

        if enemy['chicas_cautivas'] != 0:
            return enemy


def reduce_arena_opponent_info(opponent):
    href = opponent['href']
    ego = opponent.find('div', class_='opponents_ego')
    ego = ego.string.strip()
    ego = ego.replace('Ego ','').replace(',','')
    ego = int(ego)
    return (ego, href)

def definir_enemigo_arena(conn=None):
    """ Si no encuentro trolles busco en la arena """
    if not conn:
        conn = HTTPConnection(DOMAIN)
    headers = make_header('home.html', explorar=True)

    conn.request('GET', '/arena.html', headers=headers)
    descomprimido = respuesta_unzip_http(conn.getresponse())

    soup = BeautifulSoup(descomprimido, 'html.parser')
    guachos = soup.find_all('div', class_='sub_block one_opponent')
    guachos = sorted(map(reduce_arena_opponent_info, guachos), key=lambda x: x[0])
    return guachos[0]


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
    print("Recaudaste $", total)

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


# print(definir_enemigo_arena())
# print(len(argv))
# print(definir_oponente())
pelear()
