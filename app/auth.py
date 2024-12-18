from functools import wraps
from json import dump, load
from pathlib import Path
from typing import Annotated, Any, Callable, Optional

from fastapi import Cookie, Depends, Request
from fastapi.exceptions import HTTPException

from .objects import User

SESSIONS: dict[str, User] = {}
LOCKS: set[str] = set()
# REVIEW - move this logic into fetch.py with the other folders?
USERS_DIRECTORY = Path(__file__).parent.parent / "users"
if not USERS_DIRECTORY.exists():
    USERS_DIRECTORY.mkdir()
elif not USERS_DIRECTORY.is_dir():
    raise FileExistsError("users folder is not a folder??????")


def authentication_required(func: Callable):
    """Marks functions that a user needs to be authenticated for.
    Does not pass the resulting user object to the function.
    """

    @wraps(func)
    def inner(*args, request: Request, user: Annotated[Optional[User], Depends(get_session)], **kwargs) -> Any:
        session_id: str | None = request.cookies.get("session")
        if not session_id:
            raise HTTPException(status_code=401, detail="Not logged in!")
        return func(*args, request=request, **kwargs)

    return inner


def get_session(session: Annotated[str, Cookie()]) -> User | None:
    print("RUNNING SESSION CHECK")
    print(session)
    return User("test", "test", b"test")


def get_user(user_id: str):
    pass


def new_user(username: str):
    pass
