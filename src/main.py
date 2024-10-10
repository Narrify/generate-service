"""
TODO
"""

import uvicorn

from fastapi import FastAPI

from src.models.dialog import DialogRequest
from src.models.story import StoryRequest

from src.prompt.dialog import generate_dialog_prompt
from src.prompt.story import generate_story_prompt

from src.client.llm import make_request

app = FastAPI()


@app.get("/")
async def hello_world():
    """
    TODO

    :return:
    """

    return "Hello World"


@app.post('/generate/story')
async def generate_story(request: StoryRequest):
    """
    TODO
    """

    json = request.model_dump()
    prompt = generate_story_prompt(json)

    response = await make_request(prompt)

    return {
        "response": response
    }


@app.post('/generate/dialog')
async def generate_dialog(request: DialogRequest):
    """
    TODO
    """

    json = request.model_dump()
    prompt = generate_dialog_prompt(json)

    response = await make_request(prompt)

    return {
        "response": response
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0")