"""
TODO
"""

import os
import json
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