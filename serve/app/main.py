import logging
from typing import Dict, Optional

import torch
from allennlp.version import VERSION as allennlp_version
from fastapi import FastAPI, Request
from fastapi.logger import logger
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from model import get_predictor
from pydantic import BaseModel

app = FastAPI(title="date2iso")
templates = Jinja2Templates(directory="templates")
predictor = get_predictor()

# logging hassle
gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
logger.handlers = gunicorn_error_logger.handlers
logger.setLevel(logging.INFO)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, i: Optional[str] = None):
    torch_version = torch.__version__.split("+", maxsplit=1)[0]
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "i": i,
            "version": f"AllenNLP {allennlp_version}, Torch {torch_version}",
        },
    )


@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return PlainTextResponse("User-Agent: *\nDisallow: /\n")


class PredictPayload(BaseModel):
    i: str

    class Config:
        schema_extra = {
            "example": {
                "i": "January 5 2016",
            }
        }


@app.post("/")
async def predict(payload: PredictPayload):
    p = predictor
    out = p.predict(payload.i)

    result = {
        "input": payload.i,
        "model_output": out,
        "result": "".join(out["predicted_tokens"]).strip(),
        "version": p.version,
    }

    logger.info(result)

    return result
