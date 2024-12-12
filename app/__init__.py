from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from .fetch import fetch

app = FastAPI(openapi_url=None)
templates = Jinja2Templates(Path(__file__).parent / "templates")
TemplateResponse = templates.TemplateResponse


@app.get("/")
def index():
    return (Path(__file__).parent.parent / "data").exists()


app.mount("/fetch", fetch)
