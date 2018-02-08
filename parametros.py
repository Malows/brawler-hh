"""
Modulo encargado del parseo de parametros
"""

from urllib.parse import urlencode


def params_pelea(enemy):
    """ Devuelve los parametros necesarios para peleac contra un troll """
    return encodear_parametro(parsear_parametros_para_enemigo(enemy))


def parsear_parametros_para_enemigo(enemy):
    """ Devuelve los parametros, en forma de diccionario, aplicando datos del troll """
    return {
        'class': 'Battle',
        'action': 'fight',
        'who[id_troll]': enemy['id_troll'],
        'who[orgasm]': enemy['orgasm'],
        'who[ego]': enemy['ego'],
        'who[x]': enemy['x'],
        'who[d]': enemy['d'],
        'who[nb_org]': enemy['nb_org'],
        'who[figure]': enemy['figure'],
        'who[id_world]': enemy['id_world']
    }

def encodear_parametro(param):
    """ Encodea un diccionario de parametros para ser enviado por POST/PUT/DELETE """
    return urlencode(param)
