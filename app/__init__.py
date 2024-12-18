from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import fetch, auth


app = FastAPI(openapi_url=None)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
app.mount("/fetch", fetch.fetch)

templates = Jinja2Templates(Path(__file__).parent / "templates")
TemplateResponse = templates.TemplateResponse


@app.get("/")
def index(request: Request):
    return TemplateResponse(request, "_core/index.j2")


@app.get("/characters/{game}/new")
@auth.authentication_required
def new_character(request: Request, game: str, npc: bool = False):
    if npc:
        return TemplateResponse(request, f"{game}/new_npc.html")
    character_id = fetch.new_character("test", game)
    return RedirectResponse(request.url_for('character_sheet', game=game, character_id=character_id))
