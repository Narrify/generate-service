"""
TODO
"""
import json
import re

import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError


load_dotenv()

API_KEY = os.getenv("API_KEY_OPENAI")

if API_KEY is None:
    print("Error: La variable API_KEY_OPENAI no se ha cargado.")


client = OpenAI(api_key=API_KEY)


async def make_request(prompt: dict, model: str = "gpt-4o-mini", response_type: str = "story"):
    """
    Generates a response from the model, returning it as JSON if valid.
    """
    system_prompt = "You are a dialog and story generator for videogames."
    if response_type == "h":
        system_prompt += " Generate the response as a structured dialogue with speakers and their lines."
    elif response_type == "story":
        system_prompt += " Generate the response as a structured story with sections like introduction, conflict, and resolution."

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
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
        response_text = response.choices[0].message.content

        if response_text[:3] == "```":
            response_text = response_text[7:-3]

        if response_type == "dialog":
            structured_response = format_dialog_to_json(response_text)
            if structured_response:
                return {"scenes": structured_response}
            else:
                return {"error": "Could not parse dialog response", "response": response_text}

        elif response_type == "story":
            try:
                response_json = json.loads(response_text)
                return response_json
            except json.JSONDecodeError:
                return {"error": "Could not parse story response", "response": response_text}

    except OpenAIError as error:
        return {"error": "API call failed", "details": str(error)}


def format_dialog_to_json(dialog_text):
    """
    Convierte el texto de formato 'Scene X [Personaje: diálogo]' en formato JSON estructurado.
    """
    scenes_data = []

    scene_blocks = re.split(r"Scene (\d+)", dialog_text)

    for i in range(1, len(scene_blocks), 2):
        scene_id = int(scene_blocks[i].strip())
        scene_dialogs = scene_blocks[i + 1].strip()

        dialog_content = re.search(r"\[(.*?)\]", scene_dialogs)
        if dialog_content:
            dialog_lines = re.findall(r'([A-Z]): (.*?)(?=\s[A-Z]:|$)', dialog_content.group(1))

            dialog = []
            for speaker, line_text in dialog_lines:
                dialog.append({"speaker": speaker.strip(), "line": line_text.strip()})

            scenes_data.append({"scene_id": scene_id, "dialog": dialog})
        else:
            print(f"Advertencia: formato inesperado en la escena {scene_id}")

    return scenes_data
