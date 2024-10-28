from typing import List, Optional
from pydantic import BaseModel

class StorySettings(BaseModel):
    """
    Clase que define los ajustes de la historia, como el tamaño y atributos.
    """
    size: Optional[str] = "medium"
    attributes: Optional[List[dict]] = []

class Character(BaseModel):
    """
    Clase que representa un personaje en la historia.
    """
    name: str
    attributes: Optional[List[dict]] = []

class StorySection(BaseModel):
    """
    Cada sección de la historia representada por texto.
    """
    introduction: Optional[str] = None
    conflict: Optional[str] = None
    rising_action: Optional[str] = None
    climax: Optional[str] = None
    falling_action: Optional[str] = None
    resolution: Optional[str] = None

class StoryResponse(BaseModel):
    """
    Respuesta con la historia generada dividida en partes.
    """
    title: str
    genre: Optional[str] = None  # El género puede ser opcional si no se proporciona
    characters: dict  # Esperamos un diccionario de personajes y sus atributos
    setting: Optional[dict] = None  # Los ajustes pueden ser opcionales
    story: StorySection  # Cada sección de la historia

class StoryRequest(BaseModel):
    """
    Clase que define la solicitud para generar una historia.
    """
    title: Optional[str] = "Untitled Story"
    settings: StorySettings
    characters: List[Character]
    plots: Optional[int] = 1
    endings: Optional[int] = 1
