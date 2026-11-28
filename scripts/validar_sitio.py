"""Verifica archivos estáticos y controles básicos de accesibilidad de Ruta Local."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs'

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.ids = []
        self.h1 = 0
        self.lang = ''
        self.viewport = False
        self.main = 0
        self.nav = 0
        self.title = 0
        self.error = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'html': self.lang = d.get('lang', '')
        if tag == 'h1': self.h1 += 1
        if tag == 'main': self.main += 1
        if tag == 'nav': self.nav += 1
        if tag == 'title': self.title += 1
        if tag == 'meta' and d.get('name') == 'viewport': self.viewport = True
        if 'id' in d: self.ids.append(d['id'])
        if tag == 'img':
            self.images.append(d)
            if 'alt' not in d: self.error.append('Imagen sin atributo alt: '+d.get('src','?'))
        if tag in ('img', 'script', 'source') and d.get('src'): self.links.append(d['src'])
        if tag == 'a' and d.get('href'): self.links.append(d['href'])
        if tag == 'link' and d.get('href'): self.links.append(d['href'])


def main():
    i = Inspector()
    i.feed((SITE/'index.html').read_text(encoding='utf-8'))
    e = i.error
    if i.lang != 'es': e.append('Falta lang="es".')
    if i.h1 != 1: e.append('Debe haber exactamente un h1.')
    if i.main != 1: e.append('Debe haber un solo main.')
    if i.nav < 1: e.append('Falta navegación semántica.')
    if not i.viewport: e.append('Falta meta viewport.')
    if len(set(i.ids)) != len(i.ids): e.append('Existen IDs duplicados.')
    for link in i.links:
        uri = urlsplit(link)
        if uri.scheme or uri.netloc or link.startswith('mailto:'): continue
        if uri.path == '' and uri.fragment:
            if unquote(uri.fragment) not in i.ids: e.append('Ancla sin destino: '+link)
            continue
        if uri.path:
            ruta = (SITE / unquote(uri.path)).resolve()
            if SITE.resolve() not in ruta.parents and SITE.resolve() != ruta:
                e.append('Ruta fuera de docs: '+link)
            elif not ruta.exists():
                e.append('Archivo referenciado inexistente: '+link)
    if e:
        print('Validación con problemas:')
        for m in e: print(' -',m)
        raise SystemExit(1)
    print('Validación básica correcta: HTML, CSS, enlaces locales, imágenes y estructura accesible.')
    print(f'Imágenes referenciadas: {len(i.images)}; esto no reemplaza una auditoría completa WCAG.')

if __name__ == '__main__':
    main()
