import json

from fastapi import APIRouter, WebSocket, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from auth.base_config import current_user
from auth.models import User
from auth.schemas import UserRead
from .manager import websocket_manager


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.get("/", response_class=HTMLResponse)
async def websocket_chat(request: Request, user: User = Depends(current_user)):
    response = templates.TemplateResponse("index.html", {"request": request})
    user_data = UserRead.from_orm(user).dict()
    response.set_cookie('user', json.dumps(user_data))
    return response


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    user_cookie = websocket.cookies.get('user')

    if user_cookie is None:
        raise WebSocketDisconnect(reason="Unauthorized")

    user = json.loads(user_cookie)
    await websocket_manager.connect(websocket, user)

    try:
        while True:
            message = await websocket.receive_text()
            await websocket_manager.message(websocket, message)
    except WebSocketDisconnect:
        await websocket_manager.disconnect(websocket)
