from pathlib import Path
import argparse, datetime, hashlib, json, shutil, sys
ROOT = Path(__file__).resolve().parents[1]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(): return datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
def inside(p, parent):
    p = p.resolve()
    if p == parent.resolve() or parent.resolve() not in p.parents:
        raise ValueError("La ruta debe estar dentro de " + str(parent))
    return p

FILES = ("index.html", "styles.css")
WORK = ROOT / "trabajo"
parser = argparse.ArgumentParser(description="Laboratorio Ruta Local. Opera solo sobre trabajo y respaldos de este paquete.")
parser.add_argument("accion", choices=["preparar", "actualizar", "respaldar", "simular-error", "restaurar"])
parser.add_argument("--respaldo", help="Carpeta de respaldo generada por este script, dentro de respaldos")
args = parser.parse_args()
try:
    inside(WORK, ROOT)
    if args.accion == "preparar":
        if WORK.exists(): raise ValueError("Ya existe trabajo. No se sobrescribe; continúe con su copia actual.")
        WORK.mkdir()
        for name in FILES: shutil.copy2(ROOT / "sitio_v1" / name, WORK / name)
        print("Versión 1 preparada en trabajo. Conserve intactas sitio_v1 y sitio_v2.")
    elif not WORK.is_dir(): raise ValueError("Ejecute primero: python scripts/herramientas.py preparar")
    elif args.accion == "actualizar":
        for name in FILES: shutil.copy2(ROOT / "sitio_v2" / name, WORK / name)
        print("Versión 2 publicada en la copia local trabajo.")
    elif args.accion == "respaldar":
        folder = inside(ROOT / "respaldos" / stamp(), ROOT / "respaldos")
        folder.mkdir(parents=True)
        for name in FILES: shutil.copy2(WORK / name, folder / name)
        manifest = {name: digest(folder / name) for name in FILES}
        (folder / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print("Respaldo creado: " + str(folder.relative_to(ROOT)))
        print("Guarde esta ruta: se necesita para restaurar la versión elegida.")
    elif args.accion == "simular-error":
        (WORK / "index.html").write_text("<!doctype html><html lang='es'><meta charset='utf-8'><title>Error simulado</title><h1>Catálogo incorrecto</h1><p>Versión de error para practicar la restauración.</p></html>", encoding="utf-8")
        print("Error simulado SOLO en trabajo/index.html. Las fuentes y los respaldos permanecen intactos.")
    elif args.accion == "restaurar":
        if not args.respaldo: raise ValueError("Indique --respaldo con la ruta que recibió al respaldar")
        folder = inside(ROOT / args.respaldo, ROOT / "respaldos")
        manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
        if set(manifest) != set(FILES): raise ValueError("El manifiesto no corresponde al sitio de este ejercicio")
        for name in FILES:
            if digest(folder / name) != manifest[name]: raise ValueError("El respaldo cambió o está incompleto: " + name)
        for name in FILES: shutil.copy2(folder / name, WORK / name)
        print("Restauración terminada. Compruebe en el navegador la versión y el contenido.")
except (ValueError, OSError, KeyError) as e:
    parser.exit(1, "No se realizó la operación: " + str(e) + "\n")
