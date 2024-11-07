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
        "Generate a concise JSON response representing a story based on the input."
        "Keep the story around 500 tokens, "
        "focusing on key moments and essential character interactions. "
        "Maintain coherence while prioritizing brevity and impactful narrative progression. "
        "Reflect character development "
        "without extended descriptions or subplots. "
        "Output in JSON format as: {\"title\": \"string\", \"story\": \"string\"} "
        "with minimal whitespace."
    )

    return system_content


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


example_story = {
    "title": "The Quest of the Lost Kingdom",
    "settings": {
        "attributes": [
            {
                "key": "location",
                "value": "ancient forest and forgotten ruins"
            },
            {
                "key": "climate",
                "value": "mysterious mist with sporadic sunlight"
            },
            {
                "key": "era",
                "value": "medieval fantasy"
            }
        ]
    },
    "characters": [
        {
            "name": "Eldrin",
            "attributes": [
                {
                    "key": "role",
                    "value": "brave warrior"
                },
                {
                    "key": "personality",
                    "value": "determined and loyal"
                },
                {
                    "key": "goal",
                    "value": "to restore honor to his family"
                }
            ]
        },
        {
            "name": "Lyra",
            "attributes": [
                {
                    "key": "role",
                    "value": "wise healer"
                },
                {
                    "key": "personality",
                    "value": "empathetic but reserved"
                },
                {
                    "key": "goal",
                    "value": "to find the ancient healing stone"
                }
            ]
        },
        {
            "name": "Morrick",
            "attributes": [
                {
                    "key": "role",
                    "value": "cunning rogue"
                },
                {
                    "key": "personality",
                    "value": "sarcastic but clever"
                },
                {
                    "key": "goal",
                    "value": "to uncover hidden treasures for personal gain"
                }
            ]
        }
    ],
}
