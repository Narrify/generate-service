"""
This module contains the Pydantic models for the story.
"""

from typing import List
from pydantic import BaseModel

from app.models.shared import Attribute, Character


class StorySettings(BaseModel):
    """
    Pydantic model for the story settings.
    """

    size: str
    attributes: List[Attribute]


class StoryRequest(BaseModel):
    """
    Pydantic model for the story request.
    """

    title: str
    settings: StorySettings
    characters: List[Character]
