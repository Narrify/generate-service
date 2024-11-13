"""
This module contains the function that validates the token and returns the user data.
"""

from os import getenv
from time import time

from fastapi import HTTPException, status
from httpx import AsyncClient

from app.clients.mongo import insert_track


async def validate(token: str, route: str, start_time):
    """
    This function validates the token and returns the user data.
    """

    if not token:
        insert_track(route, 401, start_time, time())

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_service_url = getenv("USER_SERVICE_URL")
    headers = {"Authorization": f"Bearer {token}"}

    async with AsyncClient() as client:
        user_response = await client.get(user_service_url, headers=headers)

    if user_response.status_code != 200:
        insert_track(route, user_response.status_code, start_time, time())

        raise HTTPException(
            status_code=user_response.status_code,
            detail=user_response.json().get("detail")
        )

    return user_response.json()
