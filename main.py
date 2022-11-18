import json
import os

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from adapters.fedex import fedex_tracking_response_adapter
from providers.fed_ex.client import FedExClient
from providers.fed_ex.credentials import fedex_authorization_manager

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/fedex", response_class=HTMLResponse)
async def say_hello(request: Request, trackingNumber: str = Form()):
    async with FedExClient(base_url=os.getenv("FEDEX_API_URL"),
                           authorization_manager=fedex_authorization_manager) as client:
        tracking_response = fedex_tracking_response_adapter(await client.get_tracking_details(trackingNumber))
        return templates.TemplateResponse("index.html",
                                          {"request": request,
                                           "tracking_number": trackingNumber,
                                           "data": json.dumps(tracking_response.dict(), indent=4)})


if __name__ == '__main__':
    uvicorn.run(app)
