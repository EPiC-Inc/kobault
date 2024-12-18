from pathlib import Path
from typing import Annotated, Optional

from fastapi import Cookie, Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import fetch, auth
from .objects import User


app = FastAPI(openapi_url=None)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
app.mount("/fetch", fetch.fetch)

templates = Jinja2Templates(Path(__file__).parent / "templates")
TemplateResponse = templates.TemplateResponse


@app.get("/")
def index(request: Request, user: Annotated[Optional[User], Depends(auth.get_session)]):
    return TemplateResponse(request, "_core/index.j2", context={
        "current_user": user
    })


@app.get("/login")
def login(request: Request):
    return TemplateResponse(request, "_core/login.j2")


@app.post("/login")
def post_login():
    return ""


@app.get("/signup")
def signup(request: Request):
    return TemplateResponse(request, "_core/signup.j2")


@app.post("/signup")
def post_signup():
    return ""


@app.get("/characters/{game}/new")
@auth.authentication_required
def new_character(request: Request, game: fetch.Games, npc: bool = False):
    if npc:
        return TemplateResponse(request, f"{game.value}/new_npc.html")
    character_id = fetch.new_character("test", game)
    return RedirectResponse(request.url_for("character_sheet", character_id=character_id))


@app.get("/character/{character_id}")
def character_sheet(request: Request, character_id: str):
    return fetch.fetch_character(character_id)
