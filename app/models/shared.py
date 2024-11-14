"""
This module contains the shared models for the application.
"""

from typing import List, Optional
from pydantic import BaseModel


class Attribute(BaseModel):
    """
    Pydantic model for an attribute.
    """

    key: str
    value: str


class Character(BaseModel):
    """
    Pydantic model for a character.
    """

    name: str
    attributes: Optional[List[Attribute]] = None
