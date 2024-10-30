"""
TODO
"""

def generate_dialog_prompt(json):
    """
    Genera un prompt eficiente para diálogos usando los datos proporcionados en el JSON.
    """
    # Base del prompt con la historia y la configuración de escenas y personajes
    prompt = f"Story: {json['story']}. "
    prompt += f"Scenes: {json['settings']['number_of_scenes']}, "

    # Agregar los personajes y sus atributos de forma compacta
    prompt += "Characters: "
    for character in json['characters']:
        # Crear un string compacto con los atributos del personaje
        char_attrs = ", ".join([f"{x['name']}: {x['value']}" for x in character['attributes']])
        prompt += f"{character['name']} ({character['name'][0]}): {char_attrs}. "

    # Instrucción clara y específica sobre cómo manejar los caracteres
    prompt += f"""
    Generate a concise dialog using initials for characters and divide it into {json['settings']['number_of_scenes']} Scene. 
    Do not use contractions. so the entire dialog is in a single line .
    Format the dialog as follows: Scene 1 [A: line, L: line,...] Scene 2 [...]  the Scene force without line breaks .
    """

    return prompt
