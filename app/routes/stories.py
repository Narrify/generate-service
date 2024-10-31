"""
This module contains the routes for the stories endpoint.
"""

from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.clients.mongo import get_stories
from app.services.authentication import authenticate

router = APIRouter()

bearer = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/")
def get_stories(token: str = Depends(bearer)):
	"""
	Get all stories for the user.
	"""

	if not token:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Unauthorized",
			headers={"WWW-Authenticate": "Bearer"},
		)

	user = authenticate(token)

	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Unauthorized",
			headers={"WWW-Authenticate": "Bearer"},
		)

	stories = get_stories(user["id"])

	return stories
