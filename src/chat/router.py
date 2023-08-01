from fastapi import APIRouter, WebSocket, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from auth.base_config import current_user
from auth.models import User
from .manager import websocket_manager


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.get("/", response_class=HTMLResponse)
async def websocket_chat(request: Request, user: User = Depends(current_user)):
    print('USER: ', user.id)
    return templates.TemplateResponse("index.html", {"request": request})


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)

    try:
        while True:
            message = await websocket.receive_text()
            await websocket_manager.broadcast(message)
    except WebSocketDisconnect:
        await websocket_manager.disconnect(websocket)
