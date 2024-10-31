"""
This module contains the authentication service.
"""

from os import getenv
from httpx import AsyncClient

from fastapi import status

USER_ENDPOINT = getenv('USER_ENDPOINT')


async def authenticate(token: str):
    """
    Authenticate the user.
    """

    headers = {"Authorization": f"Bearer {token}"}

    async with AsyncClient() as client:
        response = await client.get(f"{USER_ENDPOINT}/me", headers=headers)

    if response.status_code != status.HTTP_200_OK:
        return None

    return response.json()
