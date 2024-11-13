"""
This module contains the functions to interact with the MongoDB database.
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from uuid import uuid4
import json

client = MongoClient("mongodb://localhost:27017/")

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
        "response": story
    }

    try:
        stories.insert_one(document)
        return True
    except PyMongoError:
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
        "response": dialog
    }

    try:
        dialogs.insert_one(document)
        return True
    except PyMongoError:
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
