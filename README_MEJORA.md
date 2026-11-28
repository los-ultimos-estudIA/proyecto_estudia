# Ruta Local — actualización visual y respaldos con imágenes

Proyecto: **Los Últimos EstudIA**. Repositorio de referencia: https://github.com/los-ultimos-estudIA/proyecto_estudia

> **ESTE ZIP ES UNA ACTUALIZACIÓN PARCIAL, NO UN REEMPLAZO COMPLETO DEL REPOSITORIO.**
> La foto original `docs/images/team.jpeg` no se incluye porque ya está en tu repositorio. **No la borres ni sustituyas la carpeta `images/` completa.** Copia las carpetas y permite combinar los archivos.

## Qué se modificó

- `docs/`: sitio que publica GitHub Pages (`index.html`, `styles.css` y cuatro ilustraciones SVG originales).
- `trabajo/`: copia editable con el mismo diseño y las ilustraciones.
- `sitio_v2/`: origen de la **Versión 2** actualizado para que `actualizar` no devuelva el sitio al diseño antiguo.
- `scripts/herramientas.py`: sincroniza archivos HTML/CSS **y todas las imágenes admitidas**, mantiene respaldos SHA-256, permite restauración y da soporte a respaldos anteriores.
- `scripts/validar_sitio.py`: comprueba referencias locales, imágenes con `alt`, estructura básica accesible y archivos obligatorios.

Se conserva `sitio_v1/` para la comparación V1→V2. No se necesita AWS, JavaScript ni paquetes externos.

## Instalación en tu repositorio actual (Windows / PowerShell)

1. **Antes de modificar nada, conserva una copia de tu repo** o confirma que todos tus cambios actuales están guardados en Git.
2. Descarga y descomprime el ZIP. Abre las carpetas `docs`, `trabajo`, `sitio_v2` y `scripts` del ZIP.
3. **Copia el contenido de esas carpetas a las equivalentes de tu clon local** `proyecto_estudia/`, combinando directorios y reemplazando solo archivos con el mismo nombre. No borres `docs/images/team.jpeg` ni los respaldos existentes. No subas el ZIP como un único archivo al repositorio.
4. En PowerShell, situado en `proyecto_estudia/`, ejecuta lo siguiente **en este orden**:

```powershell
python scripts/herramientas.py migrar-imagenes
python scripts/herramientas.py sincronizar
python scripts/validar_sitio.py
python scripts/herramientas.py respaldar
```

Si `python` no funciona, prueba `py`. La primera orden **copia imágenes que estén únicamente en `docs/images/` hacia `trabajo/images/`**, incluyendo `team.jpeg`, sin sobrescribir fotos existentes en trabajo. La segunda sincroniza todo a `docs/`.

5. Para enviar la nueva versión a GitHub Pages:

```powershell
git status
git add docs trabajo sitio_v2 scripts/herramientas.py scripts/validar_sitio.py README_MEJORA.md PRUEBAS_B03_B04.md
git commit -m "Mejorar diseño Ruta Local y respaldos de imágenes"
git push origin main
```

Si `README_MEJORA.md` y `PRUEBAS_B03_B04.md` no se copiaron a la raíz, omite esos dos nombres del `git add`.

**No uses `git add .` sin revisar**: `respaldos/` puede contener copias privadas o pesadas. Guarda los respaldos independientes fuera del repositorio. Si ya están controlados por Git, consulta a tu equipo antes de quitarles seguimiento.

6. Abre https://los-ultimos-estudia.github.io/proyecto_estudia/ y comprueba que se ve **Versión 2**, las tres tarjetas y la fotografía del equipo. Verifica en GitHub `Actions` que Pages haya terminado de publicar. Si ves el diseño anterior, recarga con Ctrl + F5.

## Estructura recomendada

```text
proyecto_estudia/
├── docs/                      ← Sitio publicado
│   ├── index.html
│   ├── styles.css
│   ├── .nojekyll
│   └── images/
│       ├── team.jpeg          ← TU fotografía original; conservar
│       ├── favicon.svg
│       ├── historias.svg
│       ├── oficios.svg
│       └── espacios-verdes.svg
├── trabajo/                   ← Fuente que editas y respaldas
│   ├── index.html
│   ├── styles.css
│   └── images/                 ← Imágenes originales + SVG
├── sitio_v1/                  ← Referencia V1 original
├── sitio_v2/                  ← Fuente V2 con el nuevo diseño
├── scripts/
│   ├── herramientas.py
│   └── validar_sitio.py
└── respaldos/                 ← Copias locales, no publicarlas
```

## Uso diario

```powershell
# Después de cambiar textos, CSS o añadir imágenes dentro de trabajo/images/
python scripts/herramientas.py sincronizar
python scripts/validar_sitio.py
# Si el contenido ya está correcto, crear una copia completa antes de nuevos cambios:
python scripts/herramientas.py respaldar
# Publicar los archivos resultantes mediante un commit/push
```

Para **agregar una fotografía**, colócala en `trabajo/images/` y enlázala desde `trabajo/index.html` con una ruta relativa como `images/fotografia.webp`. No coloques recursos del sitio únicamente en la raíz del repositorio: GitHub Pages publica `/docs`.

Para **eliminar una imagen** que ya existe: quítala tanto de `trabajo/images/` como de `docs/images/`, elimina las referencias HTML y luego sincroniza. Si olvidas quitarla de docs, el script detiene la operación para evitar borrar accidentalmente una foto que solo estuviera en docs.

## Restauración compatible con respaldos anteriores

```powershell
python scripts/herramientas.py respaldar
# Anota la ruta exacta que se imprime, por ejemplo respaldos/20261127_200000_000001
python scripts/herramientas.py verificar-respaldo --respaldo respaldos/NOMBRE
python scripts/herramientas.py simular-error
python scripts/herramientas.py restaurar --respaldo respaldos/NOMBRE
python scripts/validar_sitio.py
```

- Los **respaldos nuevos** incluyen HTML, CSS, `images/` y un `manifest.json` con SHA-256 por archivo.
- Los **respaldos antiguos** siguen siendo utilizables si su manifiesto es válido. Sin embargo, **no incluyen imágenes** y no pueden recuperar una foto borrada.
- Un `restaurar` de un respaldo nuevo recupera las imágenes y suprime las imágenes sobrantes para devolver el mismo conjunto de archivos respaldado.
- La simulación de error no modifica `respaldos/`; los cambios en `trabajo/` y `docs/` **solo llegan al sitio público al hacer push**.
- Para una copia realmente independiente, guarda la carpeta del respaldo también en una unidad externa, almacenamiento separado o equipo distinto, autorizado para el ejercicio.

## Mejoras de diseño y accesibilidad

- Navegación semántica, salto al contenido, enlaces reales y foco visible para teclado.
- Diseño adaptable a móviles y pantallas grandes, tarjetas culturales y mapa ilustrado.
- Colores con contraste legible, atributos `alt`, imágenes de carga diferida, estructura con `h1`, `h2` y `h3`.
- Respeto por `prefers-reduced-motion` (reduce animaciones cuando el usuario lo solicita).
- Recursos SVG locales; sin cookies, librerías externas ni dependencias de JavaScript.

## Limitaciones

La organización Ruta Local y las experiencias son **ficticias**, conforme al reto. No se inventaron reservas, direcciones, precios ni formularios. El empaquetado no contiene la fotografía existente `team.jpeg` ni los respaldos privados. El código fue comprobado localmente, pero la publicación del ZIP en tu GitHub requiere que alguien del equipo lo suba o que conectes GitHub a ChatGPT para operar sobre tu repositorio.
