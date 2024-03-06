from ultralytics import YOLO
import cv2
import asyncio
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.staticfiles import StaticFiles
from fall_detector.params import *
from fall_detector.utils.fall_detection import fall_detection_time
from fall_detector.ml_logic.predict import detection, detection_json
from fall_detector.alert_slack.alert_to_slack import alert
from fall_detector.utils.fall_detection import build_message

app = FastAPI()

#model = YOLO(MODEL_PATCH)

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), MODEL_COMPRESSION]

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_image(self, message: str, websocket: WebSocket):
        await websocket.send_bytes(message)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

manager = ConnectionManager()

@app.websocket("/fall-detection/{speed}/{wait}/{model}/{confidence}")
async def fall_detection(websocket: WebSocket, speed: int, wait: int, model: str, confidence: int):
    model = YOLO(MODEL_PATCH[model])
    await manager.connect(websocket)
    try:
        alert_send = False
        falling_time = 0
        while True:
            bytes = await websocket.receive_bytes()
            data = np.frombuffer(bytes, dtype=np.uint8)
            img = cv2.imdecode(data, 1)
            img, detections = detection(model, img, CLASS_NAMES, confidence, MODEL_CONFIDENCE_VISIBILITY)
            if alert_send == False and (falling_time := fall_detection_time(detections, falling_time)) == (wait * (1000/speed)):
                print('Alert was sending')
                alert_send = True
            ret, buffer = cv2.imencode('.jpg', img, encode_param)
            await manager.send_image(buffer.tobytes(), websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.websocket("/fall-detection-classes/{speed}/{wait}/{model}/{confidence}")
async def fall_detection_json(websocket: WebSocket, speed: int, wait: int, model: str, confidence: int):
    model = YOLO(MODEL_PATCH[model])
    await manager.connect(websocket)
    try:
        alert_send = False
        falling_time = 0
        while True:
            bytes = await websocket.receive_bytes()
            data = np.frombuffer(bytes, dtype=np.uint8)
            img = cv2.imdecode(data, 1)
            img, detections = detection_json(model, img, CLASS_NAMES, confidence, MODEL_CONFIDENCE_VISIBILITY)
            if alert_send == False and (falling_time := fall_detection_time(detections, falling_time)) == (wait * (1000/speed)):
                alert(img, encode_param)
                await manager.send_message(build_message('alert', [ALERT]), websocket)
                alert_send = True
            await manager.send_message(build_message('message', list(detections.values())), websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

app.mount("/", StaticFiles(directory=FRONTEND_PATH, html=True), name="frontend")


import uvicorn
if __name__ == "__main__":
   uvicorn.run("fast:app", host=API_ADDRESS, port=API_PORT, reload=True)
