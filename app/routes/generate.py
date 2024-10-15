import json
from fastapi import APIRouter
from app.models.dialog import DialogRequest
from app.models.story import StoryRequest

from app.prompts.dialog import generate_dialog_prompt
from app.prompts.story import generate_story_prompt

from app.clients.llm import make_request

router = APIRouter()


@router.post("/story")
async def generate_story(request: StoryRequest):
    """
    Generates a story based on the StoryRequest.
    """

    json_request = request.model_dump()
    prompt = generate_story_prompt(json_request)

    response = await make_request(prompt)

    if isinstance(response, str):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON response from make_request",
                "response": response
            }

    return response 


@router.post("/dialog")
async def generate_dialog(request: DialogRequest):
    """
    Generates a dialog based on the DialogRequest.
    """

    json_request = request.model_dump()
    prompt = generate_dialog_prompt(json_request)

    response = await make_request(prompt)

    if isinstance(response, str):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON response from make_request",
                "response": response
            }

    return response 