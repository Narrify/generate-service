"""
This module contains the prompts for the story model.
"""

from app.utils.format import format_characters


def get_story_content():
    """
    Generates the content for the story model.
    """

    system_content = (
        "You are a creative writing assistant. "
        "Generate a concise story in JSON format based on the input. "
        "Include the keys: 'title', 'characters' (only names), and 'story' with sections: "
        "'introduction', 'conflict', 'rising_action', 'climax', 'falling_action', 'resolution'. "
        "Limit the story to around 500 tokens, focusing on key moments and essential interactions. "
        "Ensure coherence, prioritize impactful progression, and reflect character development. "
        "Avoid extended descriptions or subplots. "
        "Format: {\"title\": \"str\", \"characters\": [\"str\"], \"story\": {\"introduction\": "
        "\"str\", \"conflict\": \"str\", \"rising_action\": \"str\", \"climax\": \"str\", "
        "\"falling_action\": \"str\", \"resolution\": \"string\"}} with minimal whitespace."
    )

    return system_content


# TODO:
def generate_story_prompt(entry: dict):
    """
    Generates a prompt for the dialog model based on the given entry.
    """

    prompt = f"title={entry['title']}|"
    prompt += "attributes="

    for attribute in entry['settings']['attributes']:
        prompt += f"{str(attribute['value']).lower()},"

    prompt = prompt[:-1] + "|"
    prompt += "characters="

    format_characters(prompt, entry)

    return prompt
