import io
from uuid import uuid4
import json
import os
import base64
from fastapi import FastAPI, File, UploadFile, Form
from typing import List
import uvicorn
from dotenv import load_dotenv
from openai import OpenAI
import ebooklib
from ebooklib import epub
from fastapi.responses import StreamingResponse

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_json(transcription):
    return transcription.replace("```json", "").replace("```", "").strip()

@app.post('/epub')
async def transcribe_image(file: List[UploadFile] = File(...), book_title: str = Form("Fragmento AirLib")):
    print(len(file))
    content = []

    for i in file:
        file_content = await i.read()
        
        base64_image = base64.b64encode(file_content).decode('utf-8')

        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[  
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": """
                                                    Actúa como un transcriptor experto de libros. Analiza la imagen y devuelve únicamente un objeto JSON con la siguiente estructura:

                                                    1. 'titulo': Un nombre breve y representativo que identifique el texto.
                                                    2. 'contenido': Una transcripción 100% fiel y literal del texto de la imagen. Debes mantener los párrafos exactamente como están, respetar cada signo de puntuación y conservar el estilo original.

                                                    Reglas de formato obligatorias:
                                                    - Usa etiquetas HTML básicas (<p>, <b>, <i>) dentro del campo 'contenido' para maquetar el texto.
                                                    - No incluyas etiquetas estructurales como <html>, <body> o <!DOCTYPE>.
                                                    - No añadas comentarios ni texto extra fuera del JSON. 
                                                    - La finalidad es que el contenido pueda leerse de corrido como un libro digital profesional.
                        
                                                    IMPORTANTE: Si al final de una línea en la imagen una palabra está cortada por un guion (ej: 'correspon-'),
                                                    debes unir la palabra completa ('corresponder') y eliminar el guion de corte. El texto debe fluir de forma continua,
                                                    sin cortes de línea artificiales que dependan del formato físico del libro original
                                                    """},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
        )

        clean_text = clean_json(response.choices[0].message.content) 

        final_text = json.loads(clean_text)

        content.append(final_text["contenido"])

    buffer = await create_epub(content, final_text["titulo"])
    
    return StreamingResponse(buffer, media_type="application/epub+zip")

async def create_epub(pages, title):
    
    book = epub.EpubBook()
    book.set_identifier(book.set_identifier(str(uuid4()))) 
    chapter = epub.EpubHtml(title=title, file_name='pagina.xhtml')
    chapter.content = "".join(pages)
    book.add_item(chapter)
    book.spine = ['nav', chapter]

    buffer = io.BytesIO()
    epub.write_epub(buffer, book)
    buffer.seek(0)
   
    return buffer

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)