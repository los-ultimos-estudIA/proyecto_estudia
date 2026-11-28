"""Ruta Local - GitHub Pages: versiones, imágenes, respaldos y restauración.

Fuente de publicación: trabajo/ -> docs/. Se incluyen imágenes de forma recursiva.
Los respaldos nuevos llevan SHA-256 de cada archivo (HTML, CSS y recursos de images/).

Compatible con respaldos antiguos que solo contienen index.html y styles.css.
Python 3.9+ y biblioteca estándar; no se necesitan paquetes adicionales.
"""

from pathlib import Path, PurePosixPath
import argparse
import datetime
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "trabajo"
DOCS = ROOT / "docs"
BACKUPS = ROOT / "respaldos"
REQUIRED = ("index.html", "styles.css")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif", ".svg", ".ico"}


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fecha():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def verificar_subruta(path, raiz):
    path, raiz = path.resolve(), raiz.resolve()
    if path == raiz or raiz not in path.parents:
        raise ValueError("Ruta fuera de la carpeta autorizada: " + str(path))
    return path


def validar_nombre(rel):
    if not isinstance(rel, str) or "\\" in rel or rel.startswith("/"):
        raise ValueError("Ruta inválida en respaldo: " + repr(rel))
    partes = PurePosixPath(rel).parts
    if not partes or any(p in {"..", ".", ""} or p.startswith(".") for p in partes):
        raise ValueError("Ruta inválida en respaldo: " + repr(rel))
    if rel in REQUIRED:
        return rel
    if len(partes) >= 2 and partes[0] == "images" and PurePosixPath(rel).suffix.lower() in IMAGE_SUFFIXES:
        return rel
    raise ValueError("Archivo no permitido en respaldo: " + repr(rel))


def listar_imagenes(carpeta):
    img = carpeta / "images"
    if not img.exists():
        return {}
    if img.is_symlink() or not img.is_dir():
        raise ValueError("images/ debe ser una carpeta real, no un enlace simbólico.")
    archivos = {}
    for ruta in sorted(img.rglob("*")):
        if ruta.is_symlink():
            raise ValueError("No se permiten enlaces simbólicos: " + str(ruta))
        if not ruta.is_file():
            continue
        rel = ruta.relative_to(carpeta).as_posix()
        if any(p.startswith(".") for p in PurePosixPath(rel).parts):
            continue  # Archivos de sistema (por ejemplo .DS_Store)
        validar_nombre(rel)
        archivos[rel] = ruta
    return archivos


def listar_sitio(carpeta):
    if not carpeta.is_dir() or carpeta.is_symlink():
        raise ValueError("No existe la carpeta del sitio: " + str(carpeta))
    archivos = {}
    for rel in REQUIRED:
        ruta = carpeta / rel
        if not ruta.is_file() or ruta.is_symlink():
            raise ValueError("Falta archivo del sitio: " + str(ruta))
        archivos[rel] = ruta
    archivos.update(listar_imagenes(carpeta))
    return archivos


def copiar_archivos(archivos, destino):
    for rel, origen in archivos.items():
        validar_nombre(rel)
        salida = destino.joinpath(*PurePosixPath(rel).parts)
        verificar_subruta(salida, destino)
        salida.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origen, salida)


def eliminar_imagenes_sobrantes(carpeta, esperadas):
    for rel, ruta in listar_imagenes(carpeta).items():
        if rel not in esperadas:
            ruta.unlink()
    img = carpeta / "images"
    if img.is_dir():
        for folder in sorted((p for p in img.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
            if not any(folder.iterdir()):
                folder.rmdir()


def comprobar_compatibilidad():
    """Evita borrar imágenes que el usuario solo subió a docs/ anteriormente."""
    en_docs = set(listar_imagenes(DOCS)) if DOCS.exists() else set()
    en_trabajo = set(listar_imagenes(WORK))
    extras = sorted(en_docs - en_trabajo)
    if extras:
        muestra = ", ".join(extras[:4])
        raise ValueError(
            "Hay imágenes en docs/ que todavía no están en trabajo/: " + muestra +
            ". Ejecuta primero 'python scripts/herramientas.py migrar-imagenes'."
        )


def sincronizar_docs(proteger_imagenes=True):
    archivos = listar_sitio(WORK)
    if DOCS.exists() and proteger_imagenes:
        comprobar_compatibilidad()
    DOCS.mkdir(parents=True, exist_ok=True)
    copiar_archivos(archivos, DOCS)
    eliminar_imagenes_sobrantes(DOCS, set(listar_imagenes(WORK)))
    (DOCS / ".nojekyll").touch(exist_ok=True)
    print(f"Sincronizados {len(archivos)} archivos (incluidas {len(archivos)-len(REQUIRED)} imágenes): trabajo/ -> docs/.")
    print("Para publicarlos en GitHub Pages, sube los cambios de docs/ al repositorio.")


def migrar_imagenes():
    """Una única importación segura de fotografías que existían solo en docs/."""
    listar_sitio(WORK)
    origenes = listar_imagenes(DOCS) if DOCS.exists() else {}
    destino = listar_imagenes(WORK)
    pendientes = {rel: ruta for rel, ruta in origenes.items() if rel not in destino}
    copiar_archivos(pendientes, WORK)
    print(f"Importadas {len(pendientes)} imágenes desde docs/images/ a trabajo/images/.")
    print("Las imágenes existentes en trabajo/ no se sobrescribieron.")


def crear_respaldo():
    archivos = listar_sitio(WORK)
    comprobar_compatibilidad()
    destino = BACKUPS / fecha()
    verificar_subruta(destino, BACKUPS)
    destino.mkdir(parents=True)
    copiar_archivos(archivos, destino)
    manifest = {rel: sha256(destino.joinpath(*PurePosixPath(rel).parts)) for rel in sorted(archivos)}
    (destino / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Respaldo creado: " + str(destino.relative_to(ROOT)))
    print(f"Archivos: {len(manifest)}; imágenes: {len(manifest)-len(REQUIRED)}. Integridad: SHA-256.")
    print("Guarda una copia de esta carpeta fuera del repositorio de GitHub.")


def cargar_respaldo(carpeta):
    archivo = carpeta / "manifest.json"
    if not archivo.is_file() or archivo.is_symlink():
        raise ValueError("No existe manifest.json en el respaldo indicado.")
    manifest = json.loads(archivo.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or not set(REQUIRED).issubset(manifest):
        raise ValueError("El manifiesto del respaldo es inválido o incompleto.")
    for rel, hash_esperado in manifest.items():
        validar_nombre(rel)
        ruta = carpeta.joinpath(*PurePosixPath(rel).parts)
        verificar_subruta(ruta, carpeta)
        if not ruta.is_file() or ruta.is_symlink():
            raise ValueError("Falta archivo de respaldo: " + rel)
        if not isinstance(hash_esperado, str) or len(hash_esperado) != 64 or sha256(ruta) != hash_esperado:
            raise ValueError("Error de integridad SHA-256: " + rel)
    return manifest


def restaurar_respaldo(ruta_respaldo):
    if not ruta_respaldo:
        raise ValueError("Indica --respaldo respaldos/NOMBRE_DEL_RESPALDO.")
    carpeta = verificar_subruta(ROOT / ruta_respaldo, BACKUPS)
    manifest = cargar_respaldo(carpeta)  # Valida TODO antes de modificar archivos.
    solo_texto = set(manifest) == set(REQUIRED)
    archivos = {rel: carpeta.joinpath(*PurePosixPath(rel).parts) for rel in manifest}
    if solo_texto:
        print("Aviso: respaldo antiguo o sin imágenes. Las imágenes actuales no se borrarán.")
        # Para compatibilidad, conserva imágenes existentes aunque el respaldo no las cubra.
        copiar_archivos(archivos, WORK)
        sincronizar_docs(proteger_imagenes=True)
    else:
        copiar_archivos(archivos, WORK)
        imagenes_guardadas = {rel for rel in manifest if rel.startswith("images/")}
        eliminar_imagenes_sobrantes(WORK, imagenes_guardadas)
        sincronizar_docs(proteger_imagenes=False)
    print(f"Restauración correcta desde {carpeta.relative_to(ROOT)}: {len(manifest)} archivos verificados.")


def main():
    parser = argparse.ArgumentParser(description="Ruta Local: publicación, versiones y respaldos con imágenes.")
    parser.add_argument("accion", choices=[
        "preparar", "actualizar", "migrar-imagenes", "sincronizar", "respaldar",
        "simular-error", "restaurar", "verificar-respaldo"
    ])
    parser.add_argument("--respaldo", help="Ejemplo: respaldos/20261121_101704_493083")
    args = parser.parse_args()
    try:
        if args.accion == "preparar":
            if WORK.exists():
                raise ValueError("trabajo/ ya existe; no se sobrescribe. Usa 'sincronizar'.")
            origenes = listar_sitio(ROOT / "sitio_v1")
            WORK.mkdir()
            copiar_archivos(origenes, WORK)
            migrar_imagenes()
            sincronizar_docs()
            print("Preparada Versión 1 en trabajo/ y docs/.")
            return
        if not WORK.is_dir():
            raise ValueError("No existe trabajo/. Ejecuta 'preparar' primero.")
        if args.accion == "migrar-imagenes":
            migrar_imagenes()
        elif args.accion == "actualizar":
            origenes = listar_sitio(ROOT / "sitio_v2")
            copiar_archivos(origenes, WORK)  # Conserva fotografías personalizadas en trabajo/.
            sincronizar_docs()
            print("Actualizada Versión 2 en trabajo/ y docs/.")
        elif args.accion == "sincronizar":
            sincronizar_docs()
        elif args.accion == "respaldar":
            crear_respaldo()
        elif args.accion == "simular-error":
            (WORK / "index.html").write_text(
                "<!doctype html><html lang='es'><meta charset='utf-8'>"
                "<title>Error simulado</title><h1>Catálogo incorrecto</h1>"
                "<p>Versión de error para practicar la restauración.</p></html>",
                encoding="utf-8",
            )
            sincronizar_docs()
            print("Error simulado en trabajo/ y docs/. Respaldos intactos.")
        elif args.accion == "restaurar":
            restaurar_respaldo(args.respaldo)
        elif args.accion == "verificar-respaldo":
            if not args.respaldo:
                raise ValueError("Indica --respaldo respaldos/NOMBRE_DEL_RESPALDO.")
            carpeta = verificar_subruta(ROOT / args.respaldo, BACKUPS)
            manifest = cargar_respaldo(carpeta)
            print(f"Respaldo íntegro: {len(manifest)} archivos verificados con SHA-256.")
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(1, "No se realizó la operación: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
