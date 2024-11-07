"""
This module contains functions that format data.
"""


def format_characters(prompt: str, entry: dict):
    """
    Formats a list of characters into a string.
    """

    for character in entry['characters']:
        prompt += f"{character['name']}("

        for attribute in character['attributes']:
            prompt += f"{str(attribute['value']).lower()},"

        prompt = prompt[:-1] + ");"
