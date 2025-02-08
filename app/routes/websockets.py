from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

websocket_router = APIRouter()

class WebSocketManager:
    def __init__(self):

        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = WebSocketManager()

@websocket_router.websocket("/ws/decisions")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:

        while True:
            await websocket.receive_text()  # Keep connection open
    except WebSocketDisconnect:
        await manager.disconnect(websocket)

async def send_decision_update(message: dict):
    await manager.send_message(message)
