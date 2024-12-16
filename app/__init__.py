from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .fetch import fetch


app = FastAPI(openapi_url=None)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
app.mount("/fetch", fetch)

templates = Jinja2Templates(Path(__file__).parent / "templates")
TemplateResponse = templates.TemplateResponse


@app.get("/")
def index(request: Request):
    return TemplateResponse(request, "_core/index.j2")
