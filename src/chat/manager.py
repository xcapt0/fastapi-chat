import json
from typing import Dict

from starlette.websockets import WebSocket

from .schema import ChatDataSchema, ChatSchema
from .utils import generate_color


class WebSocketManager:
    def __init__(self):
        self.connected_clients: Dict[WebSocket, dict] = {}

    async def connect(self, websocket: WebSocket, user: dict):
        await websocket.accept()

        user['color'] = generate_color()
        self.connected_clients[websocket] = user
        await self.broadcast(websocket, f"{user['username']} connected to the chat")

    async def disconnect(self, websocket: WebSocket):
        user = self.connected_clients.pop(websocket)

        if user:
            await self.broadcast(websocket, f"{user['username']} bla left the chat")

    async def send(self, websocket: WebSocket, message: str, user: dict):
        response = self.create_response(user, message)
        await websocket.send_text(json.dumps(response))

    async def broadcast(self, websocket: WebSocket, message: str):
        user = self.connected_clients[websocket]

        for connection in self.connected_clients:
            await self.send(connection, message, user)

    @staticmethod
    def create_response(user, text):
        return ChatSchema(data=ChatDataSchema(author=user["username"], text=text, color=user["color"])).dict()


websocket_manager = WebSocketManager()
