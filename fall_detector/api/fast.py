from ultralytics import YOLO
import cv2
import asyncio
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fall_detector.params import *
from fall_detector.utils.fall_detection import fall_detection_time
from fall_detector.ml_logic.predict import detection, detection_json

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

async def detect_json(websocket: WebSocket, queue: asyncio.Queue):
    alert_send = False
    falling_time = 0
    while True:
        bytes = await websocket.receive_bytes()
        data = np.frombuffer(bytes, dtype=np.uint8)
        img = cv2.imdecode(data, 1)
        detections = detection_json(model, img, CLASS_NAMES, MODEL_CONFIDENCE, MODEL_CONFIDENCE_VISIBILITY)
        if alert_send == False and (falling_time := fall_detection_time(detections, falling_time)) == MODEL_TIME_ALERT:
            print('Alert was sending')
            alert_send = True
        await websocket.send_json(detections)

@app.websocket("/fall-detection")
async def fall_detection(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await detect(websocket, None)

    except WebSocketDisconnect:
        await websocket.close()

@app.websocket("/fall-detection-classes")
async def fall_detection_json(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await detect_json(websocket, None)

    except WebSocketDisconnect:
        await websocket.close()

@app.get("/")
def healthcheck():
    return {'success': True}


import uvicorn
if __name__ == "__main__":
   uvicorn.run("fast:app", host=API_ADDRESS, port=API_PORT, reload=True)
