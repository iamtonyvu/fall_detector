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

model = YOLO(MODEL_PATCH)

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), MODEL_COMPRESSION]


async def detect(websocket: WebSocket, queue: asyncio.Queue):
    alert_send = False
    falling_time = 0
    while True:
        bytes = await websocket.receive_bytes()
        data = np.frombuffer(bytes, dtype=np.uint8)
        img = cv2.imdecode(data, 1)
        img, detections = detection(model, img, CLASS_NAMES, MODEL_CONFIDENCE, MODEL_CONFIDENCE_VISIBILITY)
        if alert_send == False and (falling_time := fall_detection_time(detections, falling_time)) == MODEL_TIME_ALERT:
            print('Alert was sending')
            alert_send = True
        ret, buffer = cv2.imencode('.jpg', img, encode_param)
        await websocket.send_bytes(buffer.tobytes())

async def detect_json(websocket: WebSocket, queue: asyncio.Queue):
    alert_send = False
    falling_time = 0
    while True:
        bytes = await websocket.receive_bytes()
        data = np.frombuffer(bytes, dtype=np.uint8)
        img = cv2.imdecode(data, 1)
        img, detections = detection_json(model, img, CLASS_NAMES, MODEL_CONFIDENCE, MODEL_CONFIDENCE_VISIBILITY)
        if alert_send == False and (falling_time := fall_detection_time(detections, falling_time)) == MODEL_TIME_ALERT:
            alert(img, encode_param)
            await websocket.send_json(build_message('alert', [ALERT]))
            alert_send = True
        await websocket.send_json(build_message('message', list(detections.values())))

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

app.mount("/", StaticFiles(directory=FRONTEND_PATH, html=True), name="frondend")


import uvicorn
if __name__ == "__main__":
   uvicorn.run("fast:app", host=API_ADDRESS, port=API_PORT, reload=True)
