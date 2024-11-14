"""
This module contains the routes for generating stories and dialogs.
"""

from time import time

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordBearer

from app.clients.llm import make_dialog_request, make_story_request
from app.clients.mongo import insert_track, save_dialog, save_story

from app.models.story import StoryRequest
from app.models.dialog import DialogRequest
from app.utils.external import validate

import os
from dotenv import load_dotenv

router = APIRouter()

oauth = OAuth2PasswordBearer(tokenUrl="token")


try: 
    USER_SERVICE_HOST=os.getenv("USER_SERVICE_HOST")
except Exception as e:
    print(f"OCURRIO UN ERROR AL CARGAR LA VARIABLE DE ENTORNO USER_SERVICE_HOST, {e}")    

@router.post("/story")
async def story(request: StoryRequest, token: str = Depends(oauth)):
    """
    Generates a story based on the input prompt.
    """

    start_time = time()

    user = await validate(token, "generate/story", start_time)
    entry = request.model_dump()
    response = make_story_request(entry)

    if not response:
        insert_track("generate/story", 500, start_time, time())

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error making request",
        )

    user_service_url = f"http://{USER_SERVICE_HOST}/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    save_story(user["id"], response)

    insert_track("generate/story", 200, start_time, time())

    return response


@router.post("/dialog")
async def dialog(request: DialogRequest, token: str = Depends(oauth)):
    """
    Generates a dialog based on the input prompt.
    """

    start_time = time()

    user = await validate(token, "generate/dialog", start_time)
    entry = request.model_dump()
    response = make_dialog_request(entry)

    user_service_url = f"http://{USER_SERVICE_HOST}/users/me"
    headers = {"Authorization": f"Bearer {token}"}
    if not response:
        insert_track("generate/dialog", 500, start_time, time())

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error making request",
        )

    save_dialog(user["id"], response)

    insert_track("generate/dialog", 200, start_time, time())

    return response
