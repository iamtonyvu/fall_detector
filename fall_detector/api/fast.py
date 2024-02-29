from ultralytics import YOLO
import cv2
import asyncio
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fall_detector.params import *
from fall_detector.ml_logic.predict import detection

app = FastAPI()

model = YOLO(MODEL_PATCH)

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), MODEL_COMPRESSION]

async def detect(websocket: WebSocket, queue: asyncio.Queue):
    while True:
        bytes = await websocket.receive_bytes()
        data = np.frombuffer(bytes, dtype=np.uint8)
        img = cv2.imdecode(data, 1)
        img = detection(model, img, CLASS_NAMES, MODEL_CONFIDENCE, MODEL_CONFIDENCE_VISIBILITY)
        ret, buffer = cv2.imencode('.jpg', img, encode_param)
        await websocket.send_bytes(buffer.tobytes())

@app.websocket("/fall-detection")
async def fall_detection(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await detect(websocket, None)

    except WebSocketDisconnect:
        await websocket.close()

import uvicorn
if __name__ == "__main__":
   uvicorn.run("fast:app", host=API_ADDRESS, port=API_PORT, reload=True)
