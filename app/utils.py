from ultralytics import YOLO
import streamlit as st
import cv2
from PIL import Image
from config import *
from streamlit_webrtc import webrtc_streamer, webrtc_streamer
import numpy as np
import av

def _display_detected_frames(conf, model, st_count, st_frame, image):
    """
    Display the detected objects on a video frame using the YOLOv8 model.
    :param conf (float): Confidence threshold for object detection.
    :param model (YOLOv8): An instance of the `YOLOv8` class containing the YOLOv8 model.
    :param st_frame (Streamlit object): A Streamlit object to display the detected video.
    :param image (numpy array): A numpy array representing the video frame.
    :return: None
    """
    # Resize the image to a standard size
    #image = cv2.resize(image, (720, int(720 * (9 / 16))))

    # Predict the objects in the image using YOLOv8 model
    res = model.predict(image, conf=conf)

    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )


# # @st.cache_resource
# def load_model(model_path):
#     """
#     Loads a YOLO object detection model from the specified model_path.

#     Parameters:
#         model_path (str): The path to the YOLO model file.

#     Returns:
#         A YOLO object detection model.
#     """
#     model = YOLO(model_path)
#     return model

def infer_uploaded_webcam(conf, model):
    """
    Execute inference for webcam (Plays a webcam stream on local).
    :param conf: Confidence of YOLOv8 model
    :param model: An instance of the `YOLOv8` class containing the YOLOv8 model.
    :return: None
    """
    try:
        flag = st.button(
            label="Stop running"
        )
        vid_cap = cv2.VideoCapture(0)  # local camera
        st_count = st.empty()
        st_frame = st.empty()

        while not flag:
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(
                        conf,
                        model,
                        st_count,
                        st_frame,
                        image
                    )
                else:
                    vid_cap.release()
                    break
    except Exception as e:
        st.error(f"Error loading video: {str(e)}")

def play_webcam(conf, model):
    """
    Plays a webcam stream on cloud. Detects Objects in real-time using the YOLO object detection model.

    Returns:
        None

    Raises:
        None
    """
    # st.sidebar.title("Webcam Object Detection")

    def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        image = frame.to_ndarray(format="bgr24")


        orig_h, orig_w = image.shape[0:2]
        width = 720  # Set the desired width for processing

        # cv2.resize used in a forked thread may cause memory leaks
        processed_image = np.asarray(Image.fromarray(image).resize((width, int(width * orig_h / orig_w))))

        if model is not None:
            # Perform object detection using YOLO model
            res = model.predict(processed_image, conf=conf)
            # print(f'resboxes: {res.boxes}')

            # Plot the detected objects on the video frame
            res_plotted = res[0].plot()
            # print(f'resplotted: {res_plotted}')


        return av.VideoFrame.from_ndarray(res_plotted, format="bgr24")


    webrtc_streamer(
        key="example",
        # video_transformer_factory=lambda: MyVideoTransformer(conf, model),
        video_frame_callback = video_frame_callback,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": False},
    )