"""
This module contains the client for the OpenAI API.
"""

from os import getenv
from time import time
from json import loads

from openai import OpenAI, OpenAIError

from app.prompts.story import get_story_content, generate_story_prompt
from app.prompts.dialog import get_dialog_content, generate_dialog_prompt

from app.log import logger

API_KEY = getenv("API_KEY")

if API_KEY is None:
    logger.error("API_KEY is not SET.")

logger.info("OpenAI Ready")

client = OpenAI(api_key=API_KEY)


def make_request(content: str, prompt: str, model: str = "gpt-4o-mini"):
    """
    Makes a request to the OpenAI API.
    """

    start_time = time()

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

        logger.info("Request completed in %s seconds.", time() - start_time)

        return response.choices[0].message.content
    except OpenAIError as error:
        logger.error("An error occurred in the OpenAI call: %s", error)
        return None


def make_story_request(entry: dict, model: str = "gpt-4o-mini"):
    """
    Makes a request to the OpenAI API for a story.
    """

    return loads(make_request(get_story_content(), generate_story_prompt(entry), model))


def make_dialog_request(entry: dict, model: str = "gpt-4o-mini"):
    """
    Makes a request to the OpenAI API for a dialog.
    """

    return loads(make_request(get_dialog_content(), generate_dialog_prompt(entry), model))
