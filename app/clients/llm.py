"""
This module contains the client for the OpenAI API.
"""

from os import getenv
from time import time
from json import loads

from openai import OpenAI, OpenAIError

from app.prompts.story import get_story_content, generate_story_prompt
from app.prompts.dialog import get_dialog_content, generate_dialog_prompt

from app.utils.log import Stream, log

API_KEY = getenv("API_KEY")

if API_KEY is None:
    log.error("API_KEY is not SET.")

log.info("OpenAI Ready")

client = OpenAI(api_key=API_KEY)


def make_request(content: str, prompt: str, model: str = "gpt-4o-mini"):
    """
    Makes a request to the OpenAI API.
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": content
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

        return response.choices[0].message.content
    except OpenAIError as error:
        log.error("An error occurred in the OpenAI call: %s")
        return None


def make_story_request(entry: dict, model: str = "gpt-4o-mini"):
    """
    Makes a request to the OpenAI API for a story.
    """

    start_time = time()

    prompt = generate_story_prompt(entry)
    response = loads(make_request(get_story_content(), prompt, model))

    sent_characters = len(entry["characters"])
    received_characters = len(response["characters"])

    if received_characters < sent_characters:
        log.error(
            f"story response is not ok ({time() - start_time}s) characters received/sent: {received_characters}/{sent_characters}",
            prompt,
            stream=Stream.LLM
        )
    else:
        log.info(
            f"story response is ok ({time() - start_time}s) characters received/sent: {received_characters}/{sent_characters}",
            prompt,
            stream=Stream.LLM
        )

    return response


def make_dialog_request(entry: dict, model: str = "gpt-4o-mini"):
    """
    Makes a request to the OpenAI API for a dialog.
    """

    start_time = time()

    prompt = generate_dialog_prompt(entry)
    response = loads(make_request(get_dialog_content(), prompt, model))

    sent_scenes = entry["settings"]["number_of_scenes"]
    received_scenes = len(response)

    if received_scenes != sent_scenes:
        log.error(
            f"dialog response is not ok ({time() - start_time}s) scenes received/sent: {received_scenes}/{sent_scenes}",
            prompt,
            stream=Stream.LLM
        )
    else:
        log.info(
            f"dialog response is ok ({time() - start_time}s) scenes received/sent: {received_scenes}/{sent_scenes}",
            prompt,
            stream=Stream.LLM
        )

    return response
