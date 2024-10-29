"""
TODO
"""
from pymongo import MongoClient
from pymongo.errors import PyMongoError

client = MongoClient("mongodb://localhost:27017/")

db = client["db"]
records = db["record"]


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
		return result

	except PyMongoError as e:
		print(f"Ocurrió un error al insertar el documento: {e}")
		return None
