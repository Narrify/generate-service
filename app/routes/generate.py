"""
This module contains the routes for generating stories and dialogs.
"""

from fastapi import HTTPException, APIRouter, status

from app.clients.llm import make_dialog_request, make_story_request

from app.models.story import StoryRequest
from app.models.dialog import DialogRequest

router = APIRouter()


@router.post("/story")
def story(request: StoryRequest):
    """
    Generates a story based on the input prompt.
    """

    entry = request.model_dump()
    response = make_story_request(entry)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error making request",
        )

    # save_story(user["id"], response)

    return response


@router.post("/dialog")
def dialog(request: DialogRequest):
    """
    Generates a dialog based on the input prompt.
    """

    entry = request.model_dump()
    response = make_dialog_request(entry)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error making request",
        )

    # save_story(user["id"], response)

    return response
