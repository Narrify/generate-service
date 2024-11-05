"""
Main file for the FastAPI application
"""

from fastapi import Depends, FastAPI, status
from fastapi.security import OAuth2PasswordBearer

from app.routes import generate

from app.utils.validate import validate_user

app = FastAPI(
    title="Narrify | Generation API",
    version="1.0.0"
)

token = ""


@app.get("/", status_code=status.HTTP_200_OK)
async def hello_world():
    """
    Root route
    """

    return "Hello World"


@app.get("/stories")
def get_stories():
    """
    Get all stories for the user.
    """

    user = validate_user(token)
    stories = get_stories(user["id"])

    return stories


@app.get("/dialogs")
def get_dialogs():
    """
    Get all dialogs for the user.
    """

    user = validate_user(token)
    dialogs = get_dialogs(user["id"])

    return dialogs


app.include_router(generate.router, prefix="/generate")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
