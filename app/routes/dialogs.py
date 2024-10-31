"""
This module contains the routes for the dialogs.
"""

from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.clients.mongo import get_dialogs
from app.services.authentication import authenticate

router = APIRouter()

bearer = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/")
def get_dialogs(token: str = Depends(bearer)):
	"""
	Get all dialogs for the user.
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

	dialogs = get_dialogs(user["id"])

	return dialogs
