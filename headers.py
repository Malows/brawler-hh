"""
Modulo encargado del parseado de headers
"""
from datos import DOMAIN
from cookie import get_cookie


HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "DNT": "1",
    "Host": DOMAIN,
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0",
    "X-Requested-With": "XMLHttpRequest"
}

GET_INFO_ENEMY_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': DOMAIN,
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0',
}


def make_header(referer=False, explorar=False):
    """
    Hace una aplicacion parcial de la cookie, y agrega el referer de donde deberia venir la peticion
    :param referer: opcional: si existe, lo agrega
    :param explorar: opcional: si se desea explorar datos, el header es distinto
    :return: headers correspondientes para hacer una peticion
    """
    headers = GET_INFO_ENEMY_HEADERS if explorar else HEADERS
    headers['Cookie'] = get_cookie()
    if referer:
        headers['Referer'] = "http://{}/{}".format(DOMAIN, referer)
    return headers
