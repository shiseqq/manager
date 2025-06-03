from fastapi import FastAPI
from fastapi.websockets import WebSocket
import uvicorn

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        # Обработка данных от клиента...
        await websocket.send_json({"status": "OK"})