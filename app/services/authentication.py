from os import getenv
from httpx import AsyncClient

from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

USER_ENDPOINT = getenv('USER_ENDPOINT')

bearer_scheme = HTTPBearer


async def authenticate(token: str):
	headers = {"Authorization": f"Bearer {token}"}

	async with AsyncClient() as client:
		response = await client.get(f"{USER_ENDPOINT}/me", headers=headers)

	if response.status_code != status.HTTP_200_OK:
		return None

	return response.json()
