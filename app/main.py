"""
Main file for the FastAPI application
"""

from time import time

from fastapi import Depends, FastAPI, Request
from fastapi.security import OAuth2PasswordBearer

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.clients.mongo import get_dialogs, get_stories, insert_track
from app.routes import generate
from app.utils.external import validate

app = FastAPI(
    title="Narrify | Generation API",
    version="1.0.0"
)

origins = [
    "http://localhost:8002",
    "http://127.0.0.1:8002"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

counts = {
    "2xx": 0,
    "4xx": 0,
    "5xx": 0
}


class CounterMiddleware(BaseHTTPMiddleware):
    """
    Middleware to count the number of requests.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Middleware to count the number of requests.
        """

        response = await call_next(request)
        status_code = response.status_code

        if 200 <= status_code < 300:
            counts["2xx"] += 1
        elif 400 <= status_code < 500:
            counts["4xx"] += 1
        elif 500 <= status_code < 600:
            counts["5xx"] += 1

        return response

    def useless_method(self):
        """
        Use this method to test the code analysis.
        """

        return self


app.add_middleware(
    CounterMiddleware
)

oauth = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def hello_world():
    """
    Root route
    """

    return "Hello World"


@app.get("/metrics")
async def get_metrics():
    """
    Get the metrics for the API.
    """

    try:
        availability = counts["2xx"] / (counts["2xx"] + counts["5xx"])
    except ZeroDivisionError:
        availability = 1.0

    try:
        reliability = counts["2xx"] / (counts["2xx"] + counts["4xx"])
    except ZeroDivisionError:
        reliability = 1.0

    return {
        "availability": availability,
        "reliability": reliability,
        "counts": counts
    }


@app.get("/stories")
async def stories(token: str = Depends(oauth)):
    """
    Get all stories for the user.
    """

    start_time = time()

    user = await validate(token, "/stories", start_time)
    entries = get_stories(user["id"])

    insert_track("/stories", 200, start_time, time())

    return [{k: v for k, v in document.items() if k != "_id"} for document in entries]


@app.get("/dialogs")
async def dialogs(token: str = Depends(oauth)):
    """
    Get all dialogs for the user.
    """

    start_time = time()

    user = await validate(token, "/dialogs", start_time)
    entries = get_dialogs(user["id"])

    insert_track("/dialogs", 200, start_time, time())

    return [{k: v for k, v in document.items() if k != "_id"} for document in entries]


app.include_router(generate.router, prefix="/generate")
