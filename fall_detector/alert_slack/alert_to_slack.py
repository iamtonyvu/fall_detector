from slack_sdk import WebClient
from fall_detector.params import *
import cv2

def alert(img, encode_param):
    client = WebClient(SLACK_TOKEN)

    ret, buffer = cv2.imencode('.jpg', img, encode_param)
    client.files_upload(
                channels=SLACK_CHANNELID,
                initial_comment = "Your grandmother fell down!",
                filename = "falling",
                content = buffer.tobytes()
                )
