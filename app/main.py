from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(openapi_url=None)
templates = Jinja2Templates(Path(__file__).parent / "templates")
TemplateResponse = templates.TemplateResponse

@app.get("/")
def index():
    return "Base :3"
