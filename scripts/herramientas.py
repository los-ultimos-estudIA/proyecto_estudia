"""Ruta Local: administra la copia de trabajo y la copia para GitHub Pages.

Las acciones que modifican el sitio sincronizan automáticamente trabajo/ -> docs/.
Los respaldos se crean a partir de trabajo/ y se mantienen fuera de GitHub.
"""

from pathlib import Path
import argparse
import datetime
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "trabajo"
DOCS = ROOT / "docs"
BACKUPS = ROOT / "respaldos"
FILES = ("index.html", "styles.css")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def inside(path, parent):
    path, parent = path.resolve(), parent.resolve()
    if path == parent or parent not in path.parents:
        raise ValueError("La ruta debe estar dentro de " + str(parent))
    return path


def comprobar_archivos(folder):
    for name in FILES:
        if not (folder / name).is_file():
            raise ValueError(f"Falta {folder / name}")


def sincronizar_docs():
    """Publica localmente los archivos de trabajo/ en docs/."""
    comprobar_archivos(WORK)
    inside(DOCS, ROOT)
    DOCS.mkdir(exist_ok=True)
    for name in FILES:
        shutil.copy2(WORK / name, DOCS / name)
    # Opcional para que GitHub Pages sirva los archivos sin pasar por Jekyll.
    (DOCS / ".nojekyll").touch(exist_ok=True)
    print("Sincronización local completada: trabajo/ -> docs/.")
    print("Para ver el cambio en GitHub Pages debes subir docs/ al repositorio.")


def main():
    parser = argparse.ArgumentParser(
        description="Ruta Local: preparar, actualizar, respaldar y restaurar trabajo/ y docs/."
    )
    parser.add_argument(
        "accion", choices=["preparar", "actualizar", "sincronizar", "respaldar", "simular-error", "restaurar"]
    )
    parser.add_argument(
        "--respaldo", help="Ruta generada al respaldar, por ejemplo respaldos/20261121_101704_493083"
    )
    args = parser.parse_args()

    try:
        inside(WORK, ROOT)
        inside(DOCS, ROOT)

        if args.accion == "preparar":
            if WORK.exists():
                raise ValueError(
                    "Ya existe trabajo/. No se sobrescribe. "
                    "Si ya tienes una versión en trabajo/, usa 'sincronizar'."
                )
            comprobar_archivos(ROOT / "sitio_v1")
            WORK.mkdir()
            for name in FILES:
                shutil.copy2(ROOT / "sitio_v1" / name, WORK / name)
            sincronizar_docs()
            print("Versión 1 preparada en trabajo/ y docs/.")
            return

        if not WORK.is_dir():
            raise ValueError("No existe trabajo/. Ejecuta primero 'preparar'.")

        if args.accion == "actualizar":
            comprobar_archivos(ROOT / "sitio_v2")
            for name in FILES:
                shutil.copy2(ROOT / "sitio_v2" / name, WORK / name)
            sincronizar_docs()
            print("Versión 2 actualizada en trabajo/ y docs/.")

        elif args.accion == "sincronizar":
            sincronizar_docs()

        elif args.accion == "respaldar":
            comprobar_archivos(WORK)
            folder = inside(BACKUPS / stamp(), BACKUPS)
            folder.mkdir(parents=True)
            for name in FILES:
                shutil.copy2(WORK / name, folder / name)
            manifest = {name: digest(folder / name) for name in FILES}
            (folder / "manifest.json").write_text(
                json.dumps(manifest, indent=2), encoding="utf-8"
            )
            print("Respaldo creado: " + str(folder.relative_to(ROOT)))
            print("Guarda esta ruta: la necesitarás para restaurar.")

        elif args.accion == "simular-error":
            (WORK / "index.html").write_text(
                "<!doctype html><html lang='es'><meta charset='utf-8'>"
                "<title>Error simulado</title><h1>Catálogo incorrecto</h1>"
                "<p>Versión de error para practicar la restauración.</p></html>",
                encoding="utf-8",
            )
            sincronizar_docs()
            print("Error simulado en trabajo/ y docs/. Los respaldos están intactos.")

        elif args.accion == "restaurar":
            if not args.respaldo:
                raise ValueError("Debes indicar --respaldo con una ruta de respaldos/.")
            folder = inside(ROOT / args.respaldo, BACKUPS)
            manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
            if set(manifest) != set(FILES):
                raise ValueError("El manifiesto no corresponde al sitio del ejercicio.")
            for name in FILES:
                if digest(folder / name) != manifest[name]:
                    raise ValueError("El respaldo está incompleto o cambió: " + name)
            for name in FILES:
                shutil.copy2(folder / name, WORK / name)
            sincronizar_docs()
            print("Restauración terminada en trabajo/ y docs/.")

    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(1, "No se realizó la operación: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
