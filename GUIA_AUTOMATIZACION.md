# Ruta Local — CI/CD y pruebas automatizadas (MVP GitHub Pages)

**Repositorio:** `los-ultimos-estudIA/proyecto_estudia`  
**Sitio público:** https://los-ultimos-estudia.github.io/proyecto_estudia/  
**Origen editable:** `trabajo/` (HTML, CSS e imágenes)  
**Publicación:** GitHub Pages mediante GitHub Actions, solo si pasan las pruebas.

Esta actualización **no requiere AWS, credenciales, servidores adicionales ni paquetes Python externos**. Se construyó para usarse con la versión de `scripts/herramientas.py` que soporta imágenes, respaldos y SHA-256 (la actualización anterior del proyecto). **No reemplaza ese script.**

## 1. ¿Qué se automatiza?

| Momento | Operación | Resultado / evidencia |
|---|---|---|
| Al abrir o actualizar un Pull Request a `main` | Generar `docs/` temporalmente desde `trabajo/`, validar HTML y recursos, ejecutar 5 pruebas funcionales | ✅/❌ en la pestaña **Actions** y archivo `reporte-pruebas-*` |
| Al aprobar un cambio y subirlo a `main` | Ejecutar pruebas, crear un respaldo con hashes SHA-256, guardar artefactos y **publicar solo si todo pasa** | `respaldo-sitio-*` + nueva versión en Pages |
| Cada lunes a las 7:23 a. m. de Colombia | Repetir pruebas, respaldar y comprobar que la URL pública y sus recursos responden correctamente | Registro histórico en **Actions** |
| Desde **Actions → Run workflow** | Ejecutar manualmente el mismo flujo sin usar comandos en tu computador | Evidencia de prueba demostrable en sustentación |

**Seguridad:** los escenarios de error se ejecutan en `tempfile.TemporaryDirectory()` dentro del runner de GitHub. No modifican la web real ni publican errores. La web queda intacta si las pruebas fallan.

## 2. Instalar una sola vez

1. Confirma que tu repositorio ya tenga la última versión de `scripts/herramientas.py`, con soporte de `migrar-imagenes`, `sincronizar`, `respaldar`, `restaurar` y `verificar-respaldo`. También debe existir `scripts/validar_sitio.py`.
2. **Muy importante:** incorpora `team.jpeg` y cualquier foto personalizada a `trabajo/images/`. Si la imagen solo está en `docs/images/`, corre **una sola vez**:

   ```powershell
   python scripts/herramientas.py migrar-imagenes
   ```

   Sube las imágenes incorporadas a `trabajo/` al repositorio. La automatización considera a `trabajo/` la única fuente de publicación; no guardará en él archivos que estén únicamente en el `docs/` remoto.
3. Extrae este ZIP y copia sus **tres elementos** dentro de la raíz del repositorio, conservando las rutas:

   ```text
   .github/workflows/ruta-local-ci-cd.yml
   tests/test_flujo.py
   scripts/verificar_publicacion.py
   GUIA_AUTOMATIZACION.md
   EVIDENCIA_AUTOMATIZACION.md
   ```

   Conserva todo lo anterior: `trabajo/`, `docs/`, `sitio_v2/`, `scripts/herramientas.py`, `scripts/validar_sitio.py`, `respaldos/`.
4. Asegúrate de que Pages **deje de desplegar directamente desde `/docs`**. En tu repositorio GitHub entra a **Settings → Pages → Build and deployment → Source → GitHub Actions**. Este paso es imprescindible: con `Deploy from a branch`, una actualización de `docs/` podría publicarse aunque fallara el workflow de pruebas.
5. En **Settings → Actions → General**, verifica que la organización permita GitHub Actions y el uso de las acciones oficiales de GitHub. No hacen falta secretos ni tokens personales.
6. Prueba localmente si lo deseas, desde la raíz:

   ```powershell
   python scripts/herramientas.py sincronizar
   python scripts/validar_sitio.py
   python -m unittest discover -s tests -p "test_*.py" -v
   ```

   La carpeta `trabajo/images/` debe tener todas las imágenes que usa el HTML, incluyendo `team.jpeg`.
7. Sube el código a GitHub:

   ```powershell
   git add .github/workflows/ruta-local-ci-cd.yml tests/test_flujo.py scripts/verificar_publicacion.py GUIA_AUTOMATIZACION.md EVIDENCIA_AUTOMATIZACION.md trabajo/
   git commit -m "Automatizar pruebas, respaldo y despliegue Ruta Local"
   git push origin main
   ```

   **Si protegiste `main`**, crea una rama, haz `git push -u origin mi-rama` y abre un Pull Request; el workflow comprobará el cambio antes de fusionarlo.
8. En **Actions**, abre `Ruta Local - Calidad y publicacion`. Verifica los jobs `Calidad y recuperacion` y `Publicacion controlada`. Visita Pages para comprobar el resultado.

**Nota sobre archivos ignorados:** conviene ignorar `respaldos/`, `reportes/`, `__pycache__/` y `*.pyc`; son salidas locales o temporales. El workflow guarda los respaldos como artefactos de ejecución, no los incorpora a Git.

## 3. Nuevo flujo diario (sin pasos manuales de sincronización, pruebas ni respaldo)

1. Cambia `trabajo/index.html`, `trabajo/styles.css` o añade recursos dentro de `trabajo/images/`.
2. Haz `commit` y `push` (o abre un PR). **Ya no necesitas ejecutar manualmente `sincronizar`, `validar_sitio` ni `respaldar`**.
3. GitHub Actions generará `docs/` en su entorno temporal y comprobará todo automáticamente.
4. Si las pruebas pasan y el cambio está en `main`, lo publicará en Pages. Si fallan, no habrá despliegue de ese cambio.

**Aclaración importante:** la carpeta `docs/` del *repositorio* no se actualiza automáticamente, porque el workflow no hace commits a Git. La carpeta `docs/` usada para **publicar** se construye desde `trabajo/` en el runner. Eso mantiene separados los permisos de escritura del equipo y los permisos temporales de publicación. Puedes seguir usando `sincronizar` localmente si quieres mantener ambas carpetas idénticas en Git, pero no es necesario para publicar con este flujo. No continúes usando `Deploy from a branch`.

## 4. ¿Qué pruebas contiene?

- **Test 01:** sincronización de HTML, CSS e imágenes.
- **Test 02:** respaldo, error simulado, eliminación de una imagen y restauración con comparación SHA-256.
- **Test 03:** detecta un respaldo manipulado y rechaza restaurarlo.
- **Test 04:** evita borrar imágenes únicas de `docs/` y prueba su migración.
- **Test 05:** actualiza V2 preservando las imágenes personalizadas.
- **Validación estática:** enlaces locales, archivos de imágenes, `alt`, `lang`, navegación, etiquetas semánticas (según las comprobaciones del script actual).
- **Vigilancia web:** respuesta HTTP y recursos enlazados del sitio público; no equivale a una auditoría completa de accesibilidad WCAG ni mide disponibilidad continua minuto a minuto.

## 5. Respaldos y restauración real

- **Cada push a `main`, ejecución manual y ciclo semanal:** el job `calidad` crea un respaldo y lo guarda en **Actions → Workflow run → Artifacts → `respaldo-sitio-...`** durante **14 días** (el periodo puede estar limitado por la organización).
- Los respaldos incluyen `manifest.json` con SHA-256 de HTML/CSS/imágenes.
- **Los artefactos de GitHub no son copias independientes permanentes**: expiran y están en el mismo proveedor que el repositorio. Para cumplir la recuperación frente a pérdidas reales, descarga respaldos periódicamente y guárdalos en almacenamiento externo autorizado.
- **La recuperación real sigue requiriendo seleccionar qué versión volver a publicar**, pues restaurar en automático después de un fallo visual podría sobrescribir cambios correctos. Descarga el respaldo, verifica su contenido, restáuralo localmente si hace falta, y súbelo como PR aprobado. El pipeline validará y publicará el sitio restaurado.

Ejemplo de restauración local de un respaldo descargado y descomprimido en `respaldos/NOMBRE`:

```powershell
python scripts/herramientas.py verificar-respaldo --respaldo respaldos/NOMBRE
python scripts/herramientas.py restaurar --respaldo respaldos/NOMBRE
```

Después confirma los archivos mediante Git y crea un PR o haz push (según las reglas de tu organización).

## 6. Integración con B05: protección de main

En **Settings → Branches → Add branch protection rule** (o **Settings → Rules → Rulesets**), orienta la regla a `main`, exige Pull Request y una aprobación, y exige que pase el check **`Calidad y recuperacion`**. **Deja que se ejecute al menos una vez primero**, para que GitHub pueda ofrecerlo como check seleccionable. No habilites reglas que impidan a la acción oficial publicar en el environment `github-pages`.

Esto mejora la demostración de permisos: los editores presentan cambios, las verificaciones se hacen automáticamente y un revisor acepta el despliegue.

**Plan gratuito:** para repositorios públicos de organizaciones GitHub Free las reglas estándar de rama protegida están disponibles; revisa los permisos de administración de tu organización.

## 7. Sustentación y evidencia

1. Enseña el archivo `.github/workflows/ruta-local-ci-cd.yml` y explica los eventos `pull_request`, `push`, `schedule` y `workflow_dispatch`.
2. Abre **Actions**: muestra los cinco tests y el check `Calidad y recuperacion` en verde.
3. Descarga el artefacto de respaldo del último run y presenta su `manifest.json`.
4. En un PR de prueba (no directamente en `main`), cambia una ruta de imagen a una inexistente; el workflow debe fallar la validación y **no debe haber despliegue**. Corrige el error, confirma un nuevo check verde y cierra o fusiona el PR.
5. Muestra cómo una actualización válida en `main` publica automáticamente y verifica la URL.
6. Demuestra `Publicacion controlada` y `Comprobacion semanal de la web` y anota resultados en `EVIDENCIA_AUTOMATIZACION.md`.

## 8. Solución de problemas

- **`No se realizó la operación: Hay imágenes en docs/ ...`**: ejecuta `migrar-imagenes` en tu computador, sube también `trabajo/images/` y vuelve a ejecutar.
- **`Archivo referenciado inexistente: images/team.jpeg`**: la fotografía no está en `trabajo/images/`. Incorpórala y haz push.
- **Workflow en verde pero la web no cambió**: comprueba que **Settings → Pages → Source** sea `GitHub Actions` y que `Publicacion controlada` también esté verde.
- **`deploy-pages` sin permisos**: revisa `Settings → Actions`, `Settings → Pages` y `Environments → github-pages`. El job de publicación ya solicita `pages: write` e `id-token: write`.
- **Se ejecutan dos despliegues**: hay otro workflow de Pages creado manualmente que sigue desplegando. Desactiva o elimina el workflow viejo si ahora usas este. El workflow estándar de Pages basado en rama debe dejar de publicar al cambiar el origen a Actions.
- **Pruebas fallan al crear respaldo**: verifica que `trabajo/` contiene las imágenes y que no tienes subcarpetas no admitidas dentro de `images/`.

## 9. Límites y seguridad

- Esta configuración **no utiliza credenciales personales ni secrets**. El job de publicación obtiene un permiso temporal limitado al despliegue.
- La comprobación programada corre semanalmente, pero puede retrasarse por la programación de GitHub Actions.
- Los artefactos tienen retención limitada. No subas contraseñas ni datos reales; este reto trabaja con información ficticia.
- No se activó una restauración automática sin revisión humana: se puede hacer, pero no conviene para este MVP ni para B05.
- Una validación de HTML y recursos no sustituye pruebas visuales, evaluación manual con teclado, lectores de pantalla o una auditoría WCAG completa.
