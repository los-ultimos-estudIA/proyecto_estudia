"""Pruebas del MVP Ruta Local (Python stdlib, sin servicios de pago).

Todas las mutaciones se realizan en un repositorio TEMPORAL y nunca en el
repositorio real ni en el sitio publicado. Se ejecuta desde la raiz del repo:
    python -m unittest discover -s tests -p 'test_*.py' -v
"""

from hashlib import sha256
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]
SCRIPT = BASE / 'scripts' / 'herramientas.py'


def huella(ruta):
    return sha256(ruta.read_bytes()).hexdigest()


class PruebasAutomatizadasRutaLocal(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory(prefix='rutalocal-ci-')
        self.raiz = Path(self.temporal.name)
        (self.raiz / 'scripts').mkdir()
        shutil.copy2(SCRIPT, self.raiz / 'scripts' / 'herramientas.py')
        shutil.copytree(BASE / 'trabajo', self.raiz / 'trabajo')
        if (BASE / 'sitio_v2').is_dir():
            shutil.copytree(BASE / 'sitio_v2', self.raiz / 'sitio_v2')

    def tearDown(self):
        self.temporal.cleanup()

    def comando(self, *args, exitoso=True):
        resultado = subprocess.run(
            [sys.executable, str(self.raiz / 'scripts' / 'herramientas.py'), *args],
            cwd=self.raiz,
            text=True,
            capture_output=True,
            timeout=30,
        )
        if exitoso:
            self.assertEqual(resultado.returncode, 0, resultado.stdout + resultado.stderr)
        else:
            self.assertNotEqual(resultado.returncode, 0, 'Se esperaba un fallo controlado')
        return resultado

    def respaldo_nuevo(self):
        self.comando('respaldar')
        respaldos = list((self.raiz / 'respaldos').iterdir())
        self.assertEqual(len(respaldos), 1)
        return respaldos[0]

    def test_01_sincroniza_html_css_e_imagenes(self):
        # Se comprueba con una imagen sintética, además de las imágenes del sitio.
        extra = self.raiz / 'trabajo' / 'images' / 'prueba-ci.png'
        extra.parent.mkdir(parents=True, exist_ok=True)
        extra.write_bytes('Archivo sintético para CI, no se publica'.encode('utf-8'))
        self.comando('sincronizar')
        for carpeta in ['trabajo', 'docs']:
            self.assertTrue((self.raiz / carpeta / 'index.html').is_file())
            self.assertTrue((self.raiz / carpeta / 'styles.css').is_file())
            self.assertTrue((self.raiz / carpeta / 'images' / 'prueba-ci.png').is_file())
        self.assertEqual(huella(extra), huella(self.raiz / 'docs/images/prueba-ci.png'))

    def test_02_respaldar_simular_error_y_restaurar(self):
        self.comando('sincronizar')
        originales = {
            p.relative_to(self.raiz / 'trabajo').as_posix(): huella(p)
            for p in (self.raiz / 'trabajo').rglob('*') if p.is_file()
        }
        respaldo = self.respaldo_nuevo()
        relativo = respaldo.relative_to(self.raiz).as_posix()
        self.comando('verificar-respaldo', '--respaldo', relativo)
        self.comando('simular-error')
        self.assertNotEqual(huella(self.raiz / 'trabajo/index.html'), originales['index.html'])
        # Destruimos una fotografía del sitio TEMPORAL, nunca del real.
        imagenes = list((self.raiz / 'trabajo/images').rglob('*')) if (self.raiz / 'trabajo/images').exists() else []
        imagenes = [p for p in imagenes if p.is_file()]
        if imagenes:
            imagenes[0].unlink()
        self.comando('restaurar', '--respaldo', relativo)
        for rel, hash_original in originales.items():
            self.assertEqual(huella(self.raiz / 'trabajo' / rel), hash_original, rel)
            self.assertEqual(huella(self.raiz / 'docs' / rel), hash_original, rel)

    def test_03_detecta_respaldo_manipulado_y_no_lo_restaurara(self):
        self.comando('sincronizar')
        respaldo = self.respaldo_nuevo()
        relativo = respaldo.relative_to(self.raiz).as_posix()
        (respaldo / 'index.html').write_text('ARCHIVO ALTERADO', encoding='utf-8')
        huella_antes = huella(self.raiz / 'trabajo/index.html')
        salida = self.comando('verificar-respaldo', '--respaldo', relativo, exitoso=False)
        self.assertIn('SHA-256', salida.stderr)
        self.comando('restaurar', '--respaldo', relativo, exitoso=False)
        self.assertEqual(huella(self.raiz / 'trabajo/index.html'), huella_antes)

    def test_04_protege_y_migra_imagenes_exclusivas_de_docs(self):
        self.comando('sincronizar')
        ruta = self.raiz / 'docs/images/foto-solo-docs.png'
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_bytes(b'fotografia sintetica')
        self.comando('sincronizar', exitoso=False)  # Evita borrado accidental.
        self.assertTrue(ruta.exists())
        self.comando('migrar-imagenes')
        self.comando('sincronizar')
        self.assertEqual(huella(self.raiz / 'trabajo/images/foto-solo-docs.png'), huella(ruta))

    def test_05_actualizar_a_v2_sin_perder_imagenes_personalizadas(self):
        if not (self.raiz / 'sitio_v2/index.html').is_file():
            self.skipTest('No se incluye sitio_v2/ en este checkout')
        nueva = self.raiz / 'trabajo/images/foto-personalizada.png'
        nueva.parent.mkdir(parents=True, exist_ok=True)
        nueva.write_bytes(b'foto personalizada')
        self.comando('actualizar')
        self.assertTrue((self.raiz / 'docs/images/foto-personalizada.png').exists())
        self.assertEqual(huella(nueva), huella(self.raiz / 'docs/images/foto-personalizada.png'))
        self.assertEqual(huella(self.raiz / 'sitio_v2/index.html'), huella(self.raiz / 'docs/index.html'))


if __name__ == '__main__':
    unittest.main()
