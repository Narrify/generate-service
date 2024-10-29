"""
TODO
"""
import re

import os
#import json
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

API_KEY = os.getenv("API_KEY_OPENAI")

if API_KEY is None:
    print("Error: La variable API_KEY_OPENAI no se ha cargado.")


client = OpenAI(api_key=API_KEY)


async def make_request(prompt: dict, model: str = "gpt-4o-mini"):
    """
    TODO
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a dialog and story generator for videogames."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=750,
            n=1,
            temperature=0.7
        )
        response=response.choices[0].message.content

        print(response)
        try:
            if response[:3]=="```":
                response=response[7:-3]

            response_json = json.loads(response)
            return response_json

        except json.JSONDecodeError as e:
            print("Error al decodificar JSON:", e)

        return response
    except OpenAIError as error:
        print(f'ocurrio un error en la llamada a OpenAI: ${error}')

        return None


def format_dialog_to_json(dialog_text):
    """
    Convierte el texto de formato 'Scene X [Personaje: diálogo]' en formato JSON estructurado.
    """
    scenes_data = []

    # Usar una expresión regular para dividir el texto en escenas
    scene_blocks = re.split(r"Scene (\d+)", dialog_text)

    # Iterar por las escenas, cada escena tiene su número y el texto de los diálogos
    for i in range(1, len(scene_blocks), 2):
        scene_id = int(scene_blocks[i].strip())  # Número de la escena
        scene_dialogs = scene_blocks[i + 1].strip()  # Diálogos de la escena

        # Extraer el contenido entre los corchetes y dividir los diálogos por los personajes
        dialog_content = re.search(r"\[(.*?)\]", scene_dialogs)
        if dialog_content:
            dialog_lines = re.findall(r'([A-Z]): (.*?)(?=\s[A-Z]:|$)', dialog_content.group(1))

            dialog = []
            for speaker, line_text in dialog_lines:
                dialog.append({"speaker": speaker.strip(), "line": line_text.strip()})

            # Añadir la escena y sus diálogos al resultado final
            scenes_data.append({"scene_id": scene_id, "dialog": dialog})
        else:
            print(f"Advertencia: formato inesperado en la escena {scene_id}")

    return scenes_data
