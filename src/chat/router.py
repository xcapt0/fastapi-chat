import json
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter(
    prefix="/ws",
    tags=["Chat"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def websocket_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

connected_clients = []

@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    response = {
        "type": "message",
        "data": {
            "timestamp": datetime.utcnow().timestamp(),
            "color": "blue",
            "author": "bla",
            "text": "bla"
        }
    }
    await websocket.send_text(json.dumps(response))

    try:
        while True:
            data = await websocket.receive_text()

            for client in connected_clients:
                response = {
                    "type": "message",
                    "data": {
                        "timestamp": datetime.utcnow().timestamp(),
                        "color": "blue",
                        "author": "bla",
                        "text": data
                    }
                }
                await client.send_text(json.dumps(response))
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
