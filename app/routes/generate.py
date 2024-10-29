
import json

"""
TODO
"""

from fastapi import APIRouter
from app.models.dialog import DialogRequest
from app.models.story import StoryRequest, StoryResponse

from app.prompts.dialog import generate_dialog_prompt
from app.prompts.story import generate_story_prompt

from app.clients.llm import make_request

from app.clients.mongo import insert_prompt

router = APIRouter()
from pydantic import ValidationError

from fastapi import HTTPException

@router.post("/story")
async def generate_story(request: StoryRequest):
    try:
        json_request = request.model_dump()
        prompt = generate_story_prompt(json_request)
        response = await make_request(prompt)

        if isinstance(response, dict):
            return response
        else:
            return {"error": "Unexpected response type from make_request", "response": response}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Invalid input format")


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
