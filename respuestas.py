"""
Modulo encargado de la gestion de respuestas
"""
import json
import zlib

def respuesta_http_dict(response):
    """ Toma un HTTPResponse, lo lee y lo devuelve como un str """
    return json.loads(''.join(response.read().decode('utf-8')))


def respuesta_unzip_http(response):
    """ Toma un HTTPResponse, lo descomprime usando gzip y lo devuelve como un str """
    return zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)


def respuesta_pelea(respuesta):
    """ Toma una respuesta parseada, y en base a los datos obtenidos, genera datos para devolver """
    respuesta = respuesta_http_dict(respuesta)
    if not respuesta['success']:
        return respuesta['error']

    resultado = respuesta['end']

    if resultado['winner'] != 1:
        print("\n\nNo ganaste. Hay que revisar las stats.\n\n")

    if 'up2' not in resultado.keys():
        return resultado

    loot = resultado['up2']

    if 'drops' not in resultado.keys() or "slot slot_SC" not in resultado['drops']:
        print("\n\nNo te dio dinero, tal vez una chica o un item de aventura.\n\n")
        return loot

    if 'soft_currency' in loot.keys() and loot['soft_currency']:
        return loot['soft_currency']

    return respuesta
