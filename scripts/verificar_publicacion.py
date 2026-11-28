"""Comprueba la disponibilidad de GitHub Pages y sus recursos locales.

Ejemplo:
    python scripts/verificar_publicacion.py --url https://los-ultimos-estudia.github.io/proyecto_estudia/

No modifica el sitio. No requiere paquetes externos.
"""

import argparse
from html.parser import HTMLParser
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen


class Recursos(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recursos = set()

    def handle_starttag(self, tag, attrs):
        campos = dict(attrs)
        recurso = None
        if tag in ('img', 'script', 'source'):
            recurso = campos.get('src')
        elif tag == 'link' and campos.get('rel'):
            relaciones = campos['rel'].split()
            if 'stylesheet' in relaciones or 'icon' in relaciones:
                recurso = campos.get('href')
        if recurso:
            self.recursos.add(recurso)


def descargar(url, timeout=15):
    peticion = Request(url, headers={'User-Agent': 'RutaLocal-CI-monitor/1.0'})
    with urlopen(peticion, timeout=timeout) as respuesta:
        if not 200 <= respuesta.status < 300:
            raise RuntimeError(f'HTTP {respuesta.status} en {url}')
        return respuesta.read()


def comprobar(url):
    pagina = descargar(url)
    texto = pagina.decode('utf-8', errors='replace')
    if '<html' not in texto.lower() or 'ruta local' not in texto.lower():
        raise RuntimeError('La pagina no contiene el HTML esperado de Ruta Local')
    inspector = Recursos()
    inspector.feed(texto)
    origen = urlsplit(url)
    contador = 0
    for recurso in sorted(inspector.recursos):
        partes = urlsplit(recurso)
        if partes.scheme in ('mailto', 'tel', 'data') or recurso.startswith('#'):
            continue
        url_recurso = urljoin(url, recurso)
        destino = urlsplit(url_recurso)
        if destino.netloc != origen.netloc:
            continue   # No depender de servidores externos al verificar este MVP.
        descargar(url_recurso)
        print('OK recurso:', url_recurso)
        contador += 1
    print(f'OK sitio: {url} ({len(pagina)} bytes HTML; {contador} recursos locales comprobados)')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--intentos', type=int, default=3)
    parser.add_argument('--espera', type=int, default=10, help='segundos entre intentos')
    args = parser.parse_args()
    if args.intentos < 1 or args.espera < 0:
        parser.error('Los intentos deben ser >= 1 y la espera >= 0')
    for n in range(1, args.intentos + 1):
        try:
            comprobar(args.url)
            return
        except (RuntimeError, HTTPError, URLError, TimeoutError, UnicodeError) as e:
            print(f'Intento {n}/{args.intentos}: {e}')
            if n == args.intentos:
                raise SystemExit(1)
            time.sleep(args.espera)


if __name__ == '__main__':
    main()
