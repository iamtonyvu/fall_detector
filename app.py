# from pathlib import Path
import streamlit as st
from ultralytics import YOLO
from play_webcam import *

st.set_page_config(
    page_title="Fall Detector",
    initial_sidebar_state="expanded"
)

# Load the image for the title
# title_image = Image.open("camera_icon.png")

# Display the title image
# st.image(title_image, use_column_width=True)

# sidebar
st.sidebar.header("Model Config")
model_path = 'best.pt'
model = load_model(model_path)

# confidence = float(st.sidebar.slider(
#     "Select Model Confidence", 30, 100, 50)) / 100

infer_uploaded_webcam(conf=0.5, model=model)
