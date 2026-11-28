# Evidencia — Automatización de pruebas, respaldos y despliegue

**Proyecto:** Ruta Local — Los Últimos EstudIA  
**Repositorio:** https://github.com/los-ultimos-estudIA/proyecto_estudia  
**Fecha:** __________________  
**Responsable(s):** __________________

## A01 — Integración continua (CI)

- [ ] Workflow ubicado en `.github/workflows/ruta-local-ci-cd.yml`.
- [ ] Captura de GitHub **Actions** con ejecución satisfactoria.
- [ ] Captura de pruebas `test_01` a `test_05` y validación estática.
- **ID del workflow ejecutado:** __________________
- **Resultado real:** __________________
- **Observaciones:** __________________

## A02 — Publicación continua (CD)

- [ ] GitHub Pages está configurado con fuente **GitHub Actions**.
- [ ] Se verificó que el despliegue depende de `Calidad y recuperacion`.
- [ ] Captura de `Publicacion controlada` en verde.
- [ ] Captura de la web actualizada en navegador incógnito.
- **URL comprobada:** __________________
- **Versión / cambio visible:** __________________
- **Resultado real:** __________________

## A03 — Respaldos automáticos (B03)

- [ ] Se descargó un artefacto `respaldo-sitio-*` desde Actions.
- [ ] Contiene `index.html`, `styles.css`, `images/` y `manifest.json`.
- [ ] Se revisaron hashes SHA-256 y se conservó una copia fuera de GitHub.
- **ID / nombre del respaldo:** __________________
- **Ubicación de copia externa:** __________________
- **Resultado real:** __________________

## A04 — Recuperación segura (B04)

- [ ] Test `test_02` pasó: error simulado y restauración en entorno temporal.
- [ ] Test `test_03` pasó: rechazo de respaldo alterado.
- [ ] Opcional: restauración real en rama de prueba, PR y publicación tras aprobación.
- **Tiempo de restauración medido:** __________________
- **Resultado real:** __________________

## A05 — Permisos y control de cambios (B05)

- [ ] PR requerido para cambios en `main`.
- [ ] Revisión y aprobación configuradas.
- [ ] Check requerido `Calidad y recuperacion`.
- [ ] Captura del PR bloqueado por un error y posteriormente aprobado (si se probó).
- **Resultado real:** __________________

## A06 — Repetibilidad y vigilancia (B06)

- [ ] Otro integrante ejecutó **Actions → Run workflow**.
- [ ] Se probó la comprobación de la URL pública.
- [ ] Se explicó la programación semanal (lunes 07:23 Colombia).
- **Resultado real:** __________________

## Riesgos y mejoras pendientes

- Respaldo en GitHub Actions: retención limitada; mantener copia independiente.
- La vigilancia programada no equivale a disponibilidad continua.
- La accesibilidad necesita pruebas manuales adicionales.
- ___________________________________________________

> No marques elementos que no hayas ejecutado. Esta plantilla no afirma que las pruebas de GitHub se hayan realizado antes de instalar el workflow.
