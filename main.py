from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Serve frontend folder statically at /static
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def get_index():
    return FileResponse("frontend/index.html")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

def save_message(message: str):
    with open("messages.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    # Send old messages
    if os.path.exists("messages.txt"):
        with open("messages.txt", "r", encoding="utf-8") as f:
            for line in f:
                await websocket.send_text(line.strip())

    try:
        while True:
            data = await websocket.receive_text()
            save_message(data)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
