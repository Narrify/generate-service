"""
This module contains the functions to interact with the MongoDB database.
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError

client = MongoClient("mongodb://localhost:27017/")

db = client["narrify"]

stories = db["stories"]
dialogs = db["dialogs"]


def save_story(id: str, story: dict):
	"""
	Save a story to the database.
	"""

	try:
		stories.insert_one({"id": id, **story})
		return True
	except PyMongoError:
		return False


def get_stories(id: str):
	"""
	Get all stories for a given id.
	"""

	return stories.find({"id": id})


def save_dialog(id: str, dialog: dict):
	"""
	Save a dialog to the database.
	"""

	try:
		dialogs.insert_one({"id": id, **dialog})
		return True
	except PyMongoError:
		return False


def get_dialogs(id: str):
	"""
	Get all dialogs for a given id.
	"""

	return dialogs.find({"id": id})
