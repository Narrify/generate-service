"""
TODO
"""

from fastapi import APIRouter

from app.models.dialog import DialogRequest
from app.models.story import StoryRequest

from app.prompts.dialog import generate_dialog_prompt
from app.prompts.story import generate_story_prompt

from app.clients.llm import make_request

from app.clients.mongo import insert_prompt

router = APIRouter()


@router.post("/story")
async def generate_story(request: StoryRequest):
    """
    TODO
    """

    json_request = request.model_dump()
    prompt = generate_story_prompt(json_request)

    response = await make_request(prompt)

    #to do that insert user in db
    insert_prompt(prompt, response)

    return {
        "response": response
    }


@router.post("/dialog")
async def generate_dialog(request: DialogRequest):
    """
    TODO
    """

    json_request = request.model_dump()
    prompt = generate_dialog_prompt(json_request)

    response = await make_request(prompt)

    insert_prompt(prompt,response)

    return {
        "response": response
    }
