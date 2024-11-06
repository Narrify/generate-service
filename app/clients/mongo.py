"""
TODO
"""
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from uuid import uuid4

client = MongoClient("mongodb://localhost:27017/")

db = client["db"]
records = db["record"]
tracking = db["tracking"]


def insert_tracking(route: str, status_code: int, start_date, end_date, latency):
    """
    Inserta un documento en la colección de MongoDB.
    """

    try:
        document = {
            "id": str(uuid4()),
            "route": route,
            "status_code": status_code,
            "start_date": start_date,
            "end_date": end_date,
            "latency": latency
        }
        result = tracking.insert_one(document)
        print("Inserted document ID:", result.inserted_id)
        return result

    except PyMongoError as e:
        print(f"Ocurrió un error al insertar el documento: {e}")
        return None


def insert_record(id: str, response: dict):
    """
    Inserta un documento en la colección de MongoDB.
    """
    try:
        document = {
            "id": id,
            "response": response
        }
        result = records.insert_one(document)
        print("Inserted document ID:", result.inserted_id)
        return result

    except PyMongoError as e:
        print(f"Ocurrió un error al insertar el documento: {e}")
        return None


def get_records(id: str):
    """
    Retrieves all documents from the MongoDB collection with the specified id.
    """
    try:
        cursor = records.find({"id": id})

        documents = []
        for document in cursor:
            document["_id"] = str(document["_id"])
            documents.append(document)

        return documents

    except PyMongoError as e:
        print(f"An error occurred while retrieving documents: {e}")
        return []
