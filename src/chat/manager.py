import json
from starlette.websockets import WebSocket

from .schema import ChatDataSchema, ChatSchema


class WebSocketManager:
    def __init__(self):
        self.connected_clients = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connected_clients.add(websocket)
        await self.broadcast("Client connected to the chat")

    async def disconnect(self, websocket: WebSocket):
        self.connected_clients.remove(websocket)
        await self.broadcast(f"Client bla left the chat")

    async def send(self, websocket: WebSocket, username: str, message: str):
        response = self.create_response(username, message)
        await websocket.send_text(json.dumps(response))

    async def broadcast(self, message: str):
        for connection in self.connected_clients:
            await self.send(connection, "Anonymous", message)

    @staticmethod
    def create_response(author, text):
        return ChatSchema(data=ChatDataSchema(author=author, text=text)).dict()


websocket_manager = WebSocketManager()
