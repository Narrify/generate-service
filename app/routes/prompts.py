import json
from tokenize import Token
from turtledemo.penrose import start

from fastapi.security import OAuth2PasswordBearer
import httpx

"""
TODO
"""
import os
from dotenv import load_dotenv
from time import time
from fastapi import APIRouter, Depends, status

from app.clients.mongo import get_records, insert_tracking

router = APIRouter()
from pydantic import ValidationError

from fastapi import HTTPException


oauth = OAuth2PasswordBearer(tokenUrl="token")


try: 
    USER_SERVICE_HOST=os.getenv("USER_SERVICE_HOST")
except Exception as e:
    print(f"OCURRIO UN ERROR AL CARGAR LA VARIABLE DE ENTORNO USER_SERVICE_HOST, {e}")

@router.get("/get")
async def get_prompts(token: str = Depends(oauth)):
    """
    Get all prompts.
    """

    startt = time()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_service_url = f"http://{USER_SERVICE_HOST}/users/me"
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

    endt = time()

    try:
        insert_tracking(
            route="/prompts/get",
            status_code=200,
            start_date=startt,
            end_date=endt,
            latency=endt - startt,
        )
        records = get_records(user_id)
        return records
    except Exception as e:
        print(e)
        insert_tracking(
            route="/prompts/get",
            status_code=500,
            start_date=startt,
            end_date=endt,
            latency=endt - startt,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener los registros",
        )
