# Antes de comenzar

El objetivo es publicar un sitio informativo, actualizar su contenido y recuperar una versión correcta después de un error. Usen la ficha del reto y el plan que definieron en el primer encuentro. Elijan y expliquen su propia solución de infraestructura.

## Qué contiene este paquete

sitio_v1 y sitio_v2: dos versiones del catálogo ficticio. scripts/herramientas.py: apoyo opcional para preparar una copia de trabajo y practicar respaldos. PLANTILLA_EVIDENCIAS.md y la última página de esta guía: registro editable de las pruebas.

## Preparación del equipo

1. Extraigan todo el ZIP en una carpeta local; no ejecuten archivos desde el visor de comprimidos.
2. Comprueben que disponen de navegador y Python 3 si utilizarán los scripts. En Windows prueben python --version; si no existe ese comando, prueben py --version y sustituyan python por py en esta guía.
3. Identifiquen quién configura, quién prueba y quién documenta. Todos deben entender el procedimiento.
4. Si tienen acceso educativo a nube, verifiquen con el facilitador el servicio habilitado y los límites. No contraten servicios para el ejercicio.

## La decisión que deben registrar

Indiquen si demostrarán una publicación en nube o una simulación local. En local se puede comprobar funcionamiento y recuperación, pero el control de acceso del proveedor y la publicación externa quedarán pendientes. Abrir un HTML en el computador no equivale a desplegarlo en nube.

## Organización sugerida del encuentro 2

10 min: retomar el plan. 100 min: construir. 15 min: pausa. 60 min: probar. 35 min: ajustar. 15 min: documentar. 5 min: cierre. Distribución orientadora para cuatro horas; el facilitador puede ajustarla.



# Publicación y actualización

## Una copia de trabajo para las pruebas

Abran una terminal en la carpeta que contiene LEEME.txt. La primera acción crea trabajo a partir de sitio_v1. Si trabajo ya existe, el script se detiene para conservar lo que hayan hecho.

```text
python scripts/herramientas.py preparar
```

Para una demostración HTTP local, ejecuten este comando desde la misma carpeta y mantengan esa terminal abierta:

```text
python -m http.server 8000 --bind 127.0.0.1 --directory trabajo
```

Abran http://127.0.0.1:8000 en el navegador y comprueben que aparece Versión 1. El enlace solo funciona en ese computador. Para detener el servidor utilicen Ctrl+C en su terminal. Este servidor es de laboratorio, no de producción [1].

## Si publican en nube

Elijan el alojamiento habilitado para el equipo. Carguen index.html y styles.css desde trabajo, configuren index.html como documento inicial cuando el servicio lo requiera y obtengan la dirección de consulta. Si el servicio dispone de HTTPS, utilicen esa dirección. Comprueben que los estilos cargan y que la URL abre desde una ventana privada. No otorguen permisos de edición al público.

## Una actualización visible

Antes de actualizar, creen un respaldo siguiendo la página 3. Luego, desde otra terminal abierta en la carpeta del paquete, copien la versión 2 a trabajo:

```text
python scripts/herramientas.py actualizar
```

Recarguen el navegador. Deben ver Versión 2 y la nueva experiencia Ruta de espacios verdes. Si publicaron en nube, vuelvan a cargar allí los archivos actualizados; el script solo modifica la copia local. Registren la dirección y una captura de cada versión.



# Respaldo y recuperación

## Primero respalden una versión que funciona

```text
python scripts/herramientas.py respaldar
```

El script imprime una carpeta dentro de respaldos con fecha y hora. Contiene ambos archivos y un manifiesto SHA-256 para comprobar su integridad. Anoten esa ruta y la versión que respaldaron. Un respaldo no está validado hasta que prueban su recuperación.

## Después provoquen un error controlado

```text
python scripts/herramientas.py simular-error
```

Solo se modifica trabajo/index.html. El navegador debe mostrar Catálogo incorrecto al recargar. El servidor podría seguir respondiendo HTTP 200: eso no demuestra que el contenido sea correcto. Las carpetas sitio_v1, sitio_v2 y respaldos no se modifican.

## Restauren la copia elegida

Sustituyan FECHA por el nombre real que imprimió el respaldo; no escriban literalmente FECHA.

```text
python scripts/herramientas.py restaurar --respaldo respaldos/FECHA
```

El script verifica las huellas antes de copiar. Recarguen el navegador y comprueben la versión, el catálogo y los estilos. Si restauraron un respaldo de la versión 1, el resultado correcto es Versión 1. Si era de la versión 2, deben recuperar Versión 2.

## Para una publicación en nube

La restauración local no cambia automáticamente el sitio alojado. Restauren o vuelvan a publicar los archivos en el servicio y verifiquen la URL externa. Expliquen dónde guardan una copia independiente del lugar que puede fallar y quién puede acceder a ella.

## La evidencia que necesitan

Registren versión inicial, ruta del respaldo, error provocado, hora de inicio y fin de la recuperación, versión recuperada y capturas antes y después. Identifiquen cuáles pasos son manuales y cuáles automatizarían.



# Decisiones de nube y problemas frecuentes

## Permisos que deben distinguir

Lectura: consultar el sitio. Actualización: cargar o modificar archivos. Administración: cambiar la configuración y los permisos. Identifiquen quién necesita cada acceso. Si el proveedor lo permite, prueben que una consulta sin sesión abre el contenido, pero no permite editarlo; prueben aparte el acceso autorizado de actualización. No incluyan claves ni capturas de credenciales en las evidencias.

## Esquema que deben explicar

Dibujen navegador, alojamiento del sitio, acceso de actualización y ubicación del respaldo. Escriban para qué sirve cada componente. Si trabajan localmente, señalen qué elemento reemplazaría cada componente en nube y qué configuraciones quedan pendientes.

## Problemas frecuentes

No aparece la nueva versión: comprueben la carpeta publicada y hagan una recarga completa o una consulta privada; revisen caché si el proveedor la utiliza.
El sitio no tiene estilos: verifiquen que styles.css está junto a index.html y que coincide el nombre, incluidas mayúsculas.
Puerto ocupado: cambien 8000 por 8001 en el comando y en la URL.
No se encuentra Python: prueben py en Windows o pidan apoyo; pueden hacer las copias manualmente si documentan el procedimiento.
El respaldo no coincide: elijan una copia íntegra. No modifiquen el manifiesto para forzar la restauración.
No hay cuenta de nube: demuestren la ruta local y describan qué no pudieron validar del despliegue externo.

## Costos y cierre

Indiquen qué podría generar consumo: almacenamiento, transferencia, solicitudes o dominio. No inventen tarifas ni contraten recursos. Al cerrar, retiren solo los recursos de prueba que crearon, según las instrucciones del entorno, y conserven las evidencias y el respaldo.

## Referencia oficial

[1] Servidor HTTP de Python: https://docs.python.org/3/library/http.server.html
Consultado el 19 de noviembre de 2026. Los procedimientos y límites específicos del proveedor se verifican en su documentación oficial.



# Pruebas y entregables

## Lista de comprobación

B01 — Publicación. Abrir la dirección correcta y reconocer la versión inicial y sus estilos. Si fue local, indicarlo.
B02 — Actualización. Publicar la versión 2 y comprobar el nuevo contenido.
B03 — Respaldo. Identificar ubicación, versión y archivos incluidos.
B04 — Recuperación. Provocar el error en una copia y recuperar el contenido esperado; medir el tiempo.
B05 — Permisos. Explicar y, cuando haya entorno, demostrar la diferencia entre lectura, actualización y administración. En local, marcar la prueba de permisos de nube como no realizada.
B06 — Repetibilidad. Otro integrante repite la actualización o recuperación siguiendo las instrucciones del equipo.

## Qué entregar

• Dirección de consulta o instrucciones para la demostración local.
• Archivos del sitio y versión que presentan.
• Esquema de infraestructura con permisos y ubicación del respaldo.
• Instrucciones para publicar, actualizar y recuperar.
• Registro de las pruebas, capturas y dificultades.
• Pendientes y mejoras que priorizarán en el tercer encuentro.

## Cómo mostrarlo en la demostración

Expliquen primero el problema de Ruta Local. Luego muestren la versión correcta, el error y la recuperación. Señalen quién puede actualizar, dónde está el respaldo y qué harían ante una falla del alojamiento. Terminen con una limitación real y la mejora que propone el equipo.

## Comprobación final

Completar comandos no basta: deben poder explicar qué cambió en la infraestructura y cómo comprobaron el resultado. Si utilizaron los scripts de ayuda, indiquen qué decisiones tomaron y qué parte del procedimiento aún depende de una persona.



# Bitácora editable del equipo

Completen esta página en Word o utilicen PLANTILLA_EVIDENCIAS.md. Dupliquen la ficha de prueba para cada verificación. No escriban contraseñas ni claves.

## Identificación y decisiones

Equipo: [completar]
Integrantes y responsabilidades: [completar]
Fecha y modalidad — nube, local o diseño: [completar]
Dirección del sitio y versión: [completar]
Alojamiento y motivo de elección: [completar]
Accesos de lectura y actualización: [completar]
Ubicación del respaldo: [completar]
Ayudas utilizadas y cambios propios: [completar]

## Ficha de una prueba

ID y objetivo: [completar]
Estado inicial y versión: [completar]
Pasos para repetir: [completar]
Resultado esperado: [completar]
Resultado observado: [completar]
Inicio, fin y duración: [completar]
Archivo o captura de evidencia: [completar]
Estado — cumple, parcial, no cumple o no realizado: [completar]
Error, ajuste y resultado al repetir: [completar]

## Continuidad

Qué funciona y qué queda pendiente: [completar]
Mejora priorizada para el encuentro 3: [completar]

