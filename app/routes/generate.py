"""
This module contains the routes for generating stories and dialogs.
"""

from fastapi import HTTPException, APIRouter, status

from app.clients.llm import make_dialog_request, make_story_request
from app.clients.mongo import save_story

from app.models.story import StoryRequest
from app.models.dialog import DialogRequest

from app.prompts.story import generate_story_prompt
from app.prompts.dialog import generate_dialog_prompt

from app.utils.validate import validate_user

router = APIRouter()
token = ""


@router.post("/story")
def post_story(request: StoryRequest):
    """
    Generates a story based on the input prompt.
    """

    user = validate_user(token)
    entry = request.model_dump()
    prompt = generate_story_prompt(entry)
    response = make_story_request(prompt)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error making request",
        )

    save_story(user["id"], response)

    return response


@router.post("/dialog")
def post_dialog(request: DialogRequest):
    """
    Generates a dialog based on the input prompt.
    """
    user = validate_user(token)
    entry = request.model_dump()
    prompt = generate_dialog_prompt(entry)
    response = make_dialog_request(prompt)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error making request",
        )

    save_story(user["id"], response)

    return response
