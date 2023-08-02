import json
from typing import Dict

from starlette.websockets import WebSocket

from .schema import ChatDataSchema, ChatSchema
from .utils import generate_color


class WebSocketManager:
    def __init__(self):
        self.connected_clients: Dict[WebSocket, dict] = {}
        self.system_user = {"username": "System", "color": "red"}

    async def connect(self, websocket: WebSocket, user: dict):
        await websocket.accept()

        user['color'] = generate_color()
        self.connected_clients[websocket] = user
        await self.send(message=f"{user['username']} connected to the chat", user=self.system_user)

    async def disconnect(self, websocket: WebSocket):
        user = self.connected_clients.pop(websocket, None)
        await self.send(message=f"{user['username']} left the chat", user=self.system_user)

    async def message(self, websocket: WebSocket, message: str):
        user = self.connected_clients[websocket]
        await self.send(message=message, user=user)

    async def send(self, message: str, user: dict):
        for websocket in self.connected_clients:
            response = self.create_response(user, message)
            await websocket.send_text(json.dumps(response))

    @staticmethod
    def create_response(user, text):
        return ChatSchema(data=ChatDataSchema(author=user["username"], text=text, color=user["color"])).dict()


websocket_manager = WebSocketManager()
