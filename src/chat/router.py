import json

from fastapi import APIRouter, WebSocket, Request, Depends, Cookie, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect
from typing import Annotated

from auth.base_config import current_user, auth_backend
from auth.models import User
from auth.schemas import UserRead
from auth.utils import get_jwt_strategy
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
    user = json.loads(websocket.cookies.get('user'))
    await websocket_manager.connect(websocket, user)

    try:
        while True:
            message = await websocket.receive_text()
            await websocket_manager.message(websocket, message)
    except WebSocketDisconnect:
        await websocket_manager.disconnect(websocket)
