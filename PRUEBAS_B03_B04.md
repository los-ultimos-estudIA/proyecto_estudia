# Pruebas complementarias para B03 y B04 — Ruta Local

Completa este registro **después de ejecutar** la prueba. No marques pasos como realizados si aún no se ejecutaron.

## B03 — Respaldo del catálogo y de las imágenes

1. Confirma que `trabajo/images/team.jpeg` exista (si no, ejecuta `migrar-imagenes`).
2. Ejecuta `python scripts/herramientas.py respaldar`.
3. Abre el respaldo generado y verifica que incluya `index.html`, `styles.css`, la carpeta `images/` y `manifest.json`.
4. Ejecuta `python scripts/herramientas.py verificar-respaldo --respaldo respaldos/NOMBRE`.
5. Conserva una **copia independiente** fuera del repositorio compartido.

**Nombre del respaldo:** [completar]

**Versión:** [completar]

**Número de imágenes:** [completar]

**Ubicación independiente de la copia:** [completar]

**Capturas:** [completar]

**Resultado observado:** [completar]

## B04 — Restauración de archivos e imágenes

1. Anota hora inicial [completar].
2. Crea un respaldo nuevo íntegro antes de provocar el error.
3. Ejecuta `python scripts/herramientas.py simular-error` (solo trabajo y docs locales).
4. Verifica que `docs/index.html` diga *Catálogo incorrecto*.
5. Opcionalmente elimina **una imagen únicamente en el sitio de trabajo**, no en el respaldo, para comprobar que también se recupera.
6. Ejecuta `python scripts/herramientas.py restaurar --respaldo respaldos/NOMBRE`.
7. Comprueba HTML, CSS y **las imágenes recuperadas** en `trabajo/` y `docs/`.
8. Anota hora final [completar] y duración [completar].
9. Si necesitas demostrarlo en GitHub Pages, después de cada paso relevante realiza commit/push y espera a que termine Pages; diferencia los tiempos locales de los del despliegue público.

**Respaldo utilizado:** [completar]

**Archivo afectado:** [completar]

**Inicio y fin:** [completar]

**Resultado observado y capturas:** [completar]

**¿Se verificó la URL pública?:** [Sí/No; enlace y captura]

**Precaución:** si usas un respaldo del script antiguo, no esperes recuperar imágenes eliminadas, porque no estaban en su manifiesto.
