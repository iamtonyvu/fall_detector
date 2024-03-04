FROM python:3.10.6-slim-bullseye

COPY fall_detector /fall_detector
COPY requirements.txt /requirements.txt
COPY model /model
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip cache purge
CMD uvicorn fall_detector.api.fast:app --host 0.0.0.0 --port $PORT
