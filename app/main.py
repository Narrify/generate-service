"""
Main file for the FastAPI application
"""

from fastapi import FastAPI, Request

from app.clients.mongo import get_dialogs, get_stories
from app.routes import generate

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

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
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        status_code = response.status_code

        if 200 <= status_code < 300:
            counts["2xx"] += 1
        elif 400 <= status_code < 500:
            counts["4xx"] += 1
        elif 500 <= status_code < 600:
            counts["5xx"] += 1

        return response


app.add_middleware(
    CounterMiddleware
)


@app.get("/")
async def hello_world():
    """
    Root route
    """

    return "Hello World"


@app.get("/metrics")
async def get_metrics():
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
def stories():
    """
    Get all stories for the user.
    """

    entries = get_stories("user_id")

    return entries


@app.get("/dialogs")
def dialogs():
    """
    Get all dialogs for the user.
    """

    entries = get_dialogs("user_id")

    return entries


app.include_router(generate.router, prefix="/generate")
