"""
This module contains the Pydantic models for the Dialog API.
"""

from typing import List
from pydantic import BaseModel

from app.models.shared import Character


class DialogSettings(BaseModel):
    """
    Pydantic model for the settings of a dialog.
    """

    number_of_scenes: int
    number_of_characters: int


class DialogRequest(BaseModel):
    """
    Pydantic model for a dialog request.
    """

    story: str
    settings: DialogSettings
    characters: List[Character]
