"""
Modulo encargado del parseado de headers
"""
from datos import DOMAIN
from cookie import parsed_cookie


HEADERS = {
    "Host": DOMAIN,
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/56.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "DNT": "1",
    "Connection": "keep-alive"
}

GET_INFO_ENEMY_HEADERS = {
    'Host': DOMAIN,
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}


def make_header(referer=False, explorar=False):
    """
    Hace una aplicacion parcial de la cookie, y agrega el referer de donde deberia venir la peticion
    :param referer: opcional: si existe, lo agrega
    :param explorar: opcional: si se desea explorar datos, el header es distinto
    :return: headers correspondientes para hacer una peticion
    """
    headers = GET_INFO_ENEMY_HEADERS if explorar else HEADERS
    headers['Cookie'] = parsed_cookie()
    if referer:
        headers['Referer'] = "http://{}/{}".format(DOMAIN, referer)
    return headers
