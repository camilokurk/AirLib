# ✅ BookScan — TODO

> **Flujo de desarrollo:** Fases 1-3 en el PC en local → Fase 4 dockerizar y desplegar en TARS → Fases 5-6 prueba real desde el iPhone

---

## Fase 1 — Entorno local en el PC

- [X]  Verificar que Python 3.10+ está instalado en el PC (`python3 --version`)
- [X]  Crear carpeta del proyecto (`mkdir bookscan && cd bookscan`)
- [X]  Crear entorno virtual (`python3 -m venv venv`)
- [X]  Activar entorno virtual (`source venv/bin/activate` en Linux/Mac o `venv\Scripts\activate` en Windows)
- [X]  Instalar dependencias base (`pip install fastapi uvicorn python-multipart`)
- [X]  Crear archivo `main.py`
- [X]  Crear endpoint `POST /epub` que reciba N imágenes y devuelva sus nombres como confirmación
- [X]  Arrancar el servidor (`uvicorn main:app --reload --host 0.0.0.0 --port 8000`)
- [X]  Probar el endpoint desde el PC con `curl` o Postman mandando una imagen
- [X]  Verificar que se reciben las imágenes correctamente

---

## Fase 2 — Integrar OpenAI Vision

- [X]  Instalar librería OpenAI (`pip install openai`)
- [X]  Verificar que tienes créditos en platform.openai.com
- [X]  Crear archivo `.env` con la API key (`OPENAI_API_KEY=sk-...`)
- [X]  Instalar `python-dotenv` (`pip install python-dotenv`)
- [X]  Cargar la API key desde `.env` en `main.py`
- [X]  Escribir función `transcribe_image(image_bytes)` que mande la imagen a GPT-4o Vision
- [X]  Definir el prompt de transcripción dentro de esa función
- [X]  Probar la función con una sola imagen de prueba
- [X]  Integrar la función en el endpoint — procesar cada imagen recibida
- [X]  Verificar que el texto devuelto es correcto y bien formateado

---

## Fase 3 — Generar el EPUB

- [X]  Instalar `ebooklib` (`pip install ebooklib`)
- [ ]  Escribir función `create_epub(pages, title)` que reciba una lista de textos y un título
- [ ]  Cada texto de la lista = un capítulo/página en el EPUB
- [ ]  Generar el EPUB en memoria (sin guardarlo en disco)
- [ ]  Devolver el EPUB como `FileResponse` o `StreamingResponse` desde el endpoint
- [ ]  Probar descargando el EPUB desde el PC y abriéndolo en un lector
- [ ]  Verificar que los párrafos y diálogos se ven bien formateados

---

## Fase 4 — Dockerizar y desplegar en TARS

- [ ]  Crear `requirements.txt` con todas las dependencias (`pip freeze > requirements.txt`)
- [ ]  Crear `Dockerfile` en la carpeta del proyecto
- [ ]  Crear `.dockerignore` (excluir `venv/`, `.env`, `__pycache__/`)
- [ ]  Crear `docker-compose.yml` con el servicio y la variable de entorno de la API key
- [ ]  Construir la imagen localmente y verificar que arranca (`docker build` + `docker run`)
- [ ]  Subir el proyecto a TARS (via `scp` o git)
- [ ]  Desplegar el contenedor desde Portainer
- [ ]  Verificar que el servicio corre correctamente en TARS
- [ ]  Verificar que ZeroTier está activo en TARS y anotar la IP
- [ ]  Probar el endpoint desde el PC via la IP de ZeroTier

---

## Fase 5 — Montar el Atajo en iPhone

- [ ]  Verificar que el iPhone está conectado a la red ZeroTier
- [ ]  Abrir app Atajos en el iPhone
- [ ]  Crear un nuevo atajo llamado "BookScan"
- [ ]  Añadir acción: seleccionar fotos del carrete (permite selección múltiple)
- [ ]  Añadir acción: pedir texto → "Título del libro (opcional)"
- [ ]  Añadir acción: obtener contenido de URL
  - URL: `http://<ip-zerotier>:8000/epub`
  - Método: POST
  - Body: multipart/form-data con las imágenes y el título
- [ ]  Añadir acción: guardar el archivo recibido en Archivos del iPhone
- [ ]  Añadir acción: abrir el archivo en Apple Books
- [ ]  Probar el atajo completo con 2-3 fotos de prueba
- [ ]  Ajustar si algo falla (timeout, formato del body, etc.)

---

## Fase 6 — Prueba real

- [ ]  Abrir El Extranjero
- [ ]  Sacar 5 fotos de páginas consecutivas con buena luz
- [ ]  Ejecutar el atajo
- [ ]  Revisar el EPUB generado en Apple Books
- [ ]  Verificar que el texto es legible, los diálogos están bien y los párrafos respetan el original
- [ ]  Ajustar el prompt de GPT-4o si hay errores recurrentes

---

## Opcional / Mejoras futuras

- [ ]  Añadir campo `author` al EPUB
- [ ]  Añadir portada generada con el título del libro
- [ ]  Manejar errores en el Atajo (si el servidor no responde, mostrar aviso)
- [ ]  Configurar que el contenedor Docker arranque automáticamente con TARS
- [ ]  Probar con otros libros y distintas condiciones de luz
- [ ]  Versión Android con HTTP Shortcuts
