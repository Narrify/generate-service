def generate_story_prompt(json_input):
    """
    Genera un prompt para una historia basado en la entrada flexible del usuario.
    Asegura que la respuesta final se adhiera a un formato estructurado, sin importar el formato de entrada.
    """
    # Contenido de la historia
    story = json_input.get("story", "A new tale unfolds.")  # Predeterminado si no se proporciona 'story'
    
    # Título (opcional, puede ser proporcionado o inferido)
    title = json_input.get("title", "Untitled Story")

    # Configuración
    settings = json_input.get("settings", {})
    size = settings.get("size", "medium")  # Indica longitud o complejidad de la historia
    attributes = settings.get("attributes", [])
    
    # Personajes
    characters = json_input.get("characters", [])
    
    # Generar contenido del prompt
    prompt = f"Title: {title}. Story size: {size}. "

    # Añadir atributos de la historia
    if attributes:
        prompt += "Attributes: " + ", ".join([f"{x['name']}: {x['value']}" for x in attributes]) + ". "
    
    # Añadir personajes y sus atributos
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

    # Añadir instrucción guía para el LLM
    prompt += (" Generate an engaging story structured in the following format: "
               "JSON with keys 'title', 'genre', 'characters', and 'story' containing the following sections: "
               "'introduction', 'conflict', 'rising_action', 'climax', 'falling_action', and 'resolution'. "
               "Use the provided information and fill in any missing details to ensure a complete response.")

    return prompt
