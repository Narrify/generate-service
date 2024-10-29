"""
TODO
"""
from pymongo import MongoClient
from pymongo.errors import PyMongoError

client = MongoClient("mongodb://localhost:27017/")

db = client["db"]
collection = db["record"]

def insert_prompt(prompt: dict, response: dict):
    """
    Inserta un documento en la colección de MongoDB.
    """
    try:
        record = {
            "prompt": prompt,
            "response": response
        }
        result = collection.insert_one(record)
        return result

    except PyMongoError as e:
        print(f"Ocurrió un error al insertar el documento: {e}")
        return None
