"""
This module contains the functions to generate prompts for the dialog model.
"""

from app.utils.format import format_characters


def get_dialog_content():
    """
    Generates the content for the dialog model.
    """

    system_content = (
        "You are a creative writing assistant."
        "Generate a JSON response containing a concise list of scenes."
        "Keep the response around 500 tokens,"
        "each scene should include 'scene_number' and "
        "an array of 'dialogues' where each dialogue has a 'character' and 'line'. "
        "Characters may speak in any order, with one character able "
        "to have multiple lines before another responds."
        "Keep responses brief but coherent, focusing on natural interactions. "
        "Output in JSON format as: "
        "[{\"scene_number\": 1, \"dialogues\": [{\"character\": \"name\", \"line\": \"text\"}]}] "
        "with minimal whitespace."
    )

    return system_content


def generate_dialog_prompt(entry: dict):
    """
    Generates a prompt for the dialog model based on the given entry.
    """

    prompt = f"story={entry['story']}|"
    prompt += f"scenes={entry['settings']['number_of_scenes']}|"

    prompt += "characters="

    prompt = format_characters(prompt, entry)

    return prompt
