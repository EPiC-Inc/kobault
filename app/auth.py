from functools import wraps
from json import dump, load
from pathlib import Path
from typing import Any, Callable

from fastapi import Request
from fastapi.exceptions import HTTPException

from .objects import User

LOCKS: set[str] = set()
# REVIEW - move this logic into fetch.py with the other folders?
USERS_DIRECTORY = Path(__file__).parent.parent / "users"
if not USERS_DIRECTORY.exists():
    USERS_DIRECTORY.mkdir()
elif not USERS_DIRECTORY.is_dir():
    raise FileExistsError("users folder is not a folder??????")


def authentication_required(func: Callable):
    """Marks functions that a user needs to be authenticated for."""

    @wraps(func)
    def inner(*args, request: Request, **kwargs) -> Any:
        session_id: str | None = request.cookies.get("session")
        if not session_id:
            raise HTTPException(status_code=401, detail="Not logged in!")
        return func(*args, request=request, **kwargs)

    return inner
