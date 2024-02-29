from pathlib import Path
import streamlit as st
from ultralytics import YOLO
from utils import infer_uploaded_webcam, play_webcam
from PIL import Image

# setting page layout
# st.set_page_config(
#     page_title="Interactive Interface for YOLOv8",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded"
#     )

st.set_page_config(
    page_title="Fall Detector",
    # page_icon=":abc:",
    # layout="wide",

    initial_sidebar_state="expanded"
)

# Load the image for the title
title_image = Image.open("camera_icon.png")

# Display the title image
st.image(title_image, use_column_width=True)

# sidebar
st.sidebar.header("Model Config")
model = YOLO('best.pt')

# image/video options
st.sidebar.header("Input Config")
source_selectbox = st.sidebar.selectbox(
    "Select Source",
    ["Webcam", "Image", "Video"]
)

# confidence = float(st.sidebar.slider(
#     "Select Model Confidence", 30, 100, 50)) / 100

if source_selectbox == "Webcam": # Webcam
    # infer_uploaded_webcam(confidence, model)
    infer_uploaded_webcam(conf=0.5, model=model)
else:
    st.error("Currently only 'Image' and 'Video' source are implemented")
