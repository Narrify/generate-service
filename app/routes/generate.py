import json

from fastapi.security import OAuth2PasswordBearer
import httpx

"""
TODO
"""

from fastapi import APIRouter, Depends, status
from app.models.dialog import DialogRequest
from app.models.story import StoryRequest, StoryResponse

from app.prompts.dialog import generate_dialog_prompt
from app.prompts.story import generate_story_prompt

from app.clients.llm import make_request
from app.clients.mongo import insert_record

router = APIRouter()
from pydantic import ValidationError

from fastapi import HTTPException

oauth = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/story")
async def generate_story(request: StoryRequest, token: str = Depends(oauth)):
	"""
	Generates a story based on the StoryRequest.
	"""

	if not token:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Unauthorized",
			headers={"WWW-Authenticate": "Bearer"},
		)

	user_service_url = "http://127.0.0.1:8000/users/me"
	headers = {"Authorization": f"Bearer {token}"}

	async with httpx.AsyncClient() as client:
		user_response = await client.get(user_service_url, headers=headers)

	if user_response.status_code != 200:
		raise HTTPException(
			status_code=user_response.status_code,
			detail="Error al obtener el usuario",
		)

	user_data = user_response.json()
	user_id = user_data.get("username")

	try:
		json_request = request.model_dump()
		prompt = generate_story_prompt(json_request)
		response = await make_request(prompt)

		if isinstance(response, dict):
			insert_record(user_id, response)
			return response
		else:
			return {"error": "Unexpected response type from make_request", "response": response}
	except ValidationError as e:
		raise HTTPException(status_code=422, detail="Invalid input format")


@router.post("/dialog")
async def generate_dialog(request: DialogRequest, token: str = Depends(oauth)):
	"""
	Generates a dialog based on the DialogRequest.
	"""

	if not token:
		raise HTTPException(status_code=401, detail="Token not found")

	user_service_url = "http://127.0.0.1:8000/users/me"
	headers = {"Authorization": f"Bearer {token}"}

	async with httpx.AsyncClient() as client:
		user_response = await client.get(user_service_url, headers=headers)

	if user_response.status_code != 200:
		raise HTTPException(
			status_code=user_response.status_code,
			detail="Error al obtener el usuario",
		)

	user_data = user_response.json()
	user_id = user_data.get("username")

	json_request = request.model_dump()
	prompt = generate_dialog_prompt(json_request)

	response = await make_request(prompt)

	if isinstance(response, dict):
		try:
			insert_record(user_id, response)
			return response
		except json.JSONDecodeError:
			return {
				"error": "Invalid JSON response from make_request",
				"response": response
			}

	return response
