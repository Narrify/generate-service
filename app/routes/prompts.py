import json
from tokenize import Token

from fastapi.security import OAuth2PasswordBearer
import httpx

"""
TODO
"""

from fastapi import APIRouter, Depends, status

from app.clients.mongo import get_records

router = APIRouter()
from pydantic import ValidationError

from fastapi import HTTPException

oauth = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/get")
async def get_prompts(token: str = Depends(oauth)):
    """
    Get all prompts.
    """

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_service_url = "http://127.0.0.1:8000/users/me"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        user_response = await client.get(user_service_url, headers=headers)

    if user_response.status_code != 200:
        raise HTTPException(
            status_code=user_response.status_code,
            detail="Error al obtener el usuario",
        )

    user_data = user_response.json()
    user_id = user_data.get("username")

    try:
        records = get_records(user_id)
        return records
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener los registros",
        )
