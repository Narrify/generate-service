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

router = APIRouter()

oauth = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/story")
def story(request: StoryRequest, token: str = Depends(oauth)):
    """
    Generates a story based on the input prompt.
    """

    start_time = time()

    user = validate(token, "generate/story", start_time)
    entry = request.model_dump()
    response = make_story_request(entry)

    if not response:
        insert_track("generate/story", 500, start_time, time())

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error making request",
        )

    save_story(user["id"], response)

    insert_track("generate/story", 200, start_time, time())

    return response


@router.post("/dialog")
def dialog(request: DialogRequest, token: str = Depends(oauth)):
    """
    Generates a dialog based on the input prompt.
    """

    start_time = time()

    user = validate(token, "generate/dialog", start_time)
    entry = request.model_dump()
    response = make_dialog_request(entry)

    if not response:
        insert_track("generate/dialog", 500, start_time, time())

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error making request",
        )

    save_dialog(user["id"], response)

    insert_track("generate/dialog", 200, start_time, time())

    return response
