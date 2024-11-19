"""
This module contains the functions to interact with the MongoDB database.
"""

from time import time
from uuid import uuid4

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.utils.log import Stream, log

client = MongoClient("mongodb://localhost:27017/")

try:
    client.server_info()
except PyMongoError:
    log.error("MongoDB is not SET.")

log.info("MongoDB Ready")

db = client["narrify"]

# storage
stories = db["stories"]
dialogs = db["dialogs"]

# tracking
tracking = db["tracking"]


def save_story(user_id: str, story: dict):
    """
    Save a story to the database.
    """

    document = {
        "id": user_id,
        "timestamp": time(),
        "response": story
    }

    try:
        stories.insert_one(document)
        log.info(f"story saved for user: {user_id}", stream=Stream.MONGO)
        return True
    except PyMongoError:
        log.info(f"story not saved for user: {user_id}", stream=Stream.MONGO)
        return False


def get_stories(user_id: str):
    """
    Get all stories for a given id.
    """

    return stories.find({"id": user_id})


def save_dialog(user_id: str, dialog: dict):
    """
    Save a dialog to the database.
    """

    document = {
        "id": user_id,
        "timestamp": time(),
        "response": dialog
    }

    try:
        dialogs.insert_one(document)
        log.info(f"dialog saved for user: {user_id}", stream=Stream.MONGO)
        return True
    except PyMongoError:
        log.error(f"dialog not saved for user: {user_id}", stream=Stream.MONGO)
        return False


def get_dialogs(user_id: str):
    """
    Get all dialogs for a given id.
    """

    return dialogs.find({"id": user_id})


def insert_track(route: str, status_code: int, start_date, end_date):
    """
    Insert a tracking record into the database.
    """

    try:
        tracking.insert_one({
            "id": str(uuid4()),
            "route": route,
            "status_code": status_code,
            "start_date": start_date,
            "end_date": end_date,
            "latency": start_date - end_date
        })

        return True
    except PyMongoError:
        return False
