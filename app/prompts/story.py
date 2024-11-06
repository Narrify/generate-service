def generate_story_prompt(json_input):
    """
    Genera un prompt para una historia basado en la entrada flexible del usuario.
    Asegura que la respuesta final se adhiera a un formato estructurado, sin importar el formato de entrada.
    """
    story = json_input.get("story", "A new tale unfolds.") 
    
    title = json_input.get("title", "Untitled Story")

    settings = json_input.get("settings", {})
    size = settings.get("size", "medium") 
    attributes = settings.get("attributes", [])
    
    characters = json_input.get("characters", [])

    prompt = f"Title: {title}. Story size: {size}. "

    if attributes:
        prompt += "Attributes: " + ", ".join([f"{x['name']}: {x['value']}" for x in attributes]) + ". "
    
    if characters:
        prompt += "Characters: "
        for character in characters:
            char_name = character.get("name", "Unnamed Character")
            char_attrs = character.get("attributes", [])
            if char_attrs:
                char_attrs_str = ", ".join([f"{x['name']}: {x['value']}" for x in char_attrs])
                prompt += f"{char_name} ({char_name[0]}): {char_attrs_str}. "
            else:
                prompt += f"{char_name} ({char_name[0]}): No attributes. "
    else:
        prompt += "Characters: No characters provided. "

    prompt += ("Generate an engaging story structured in the following format: "
               "Json with the keys 'title', 'characters' (only names) and 'story' containing the following sections: "
               "'introduction', 'conflict', 'rising_action', 'climax', 'falling_action', and 'resolution'. "
               "Use the provided information and fill in any missing details to ensure a complete response. "
               "Do not repeat the provided information, only include the story created with the basic information.")

    return prompt
