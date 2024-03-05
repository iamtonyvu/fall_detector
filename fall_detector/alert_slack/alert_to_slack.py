from slack_sdk import WebClient
from fall_detector.params import *
import cv2

def alert(img, encode_param):
    client = WebClient(SLACK_TOKEN)

    ret, buffer = cv2.imencode('.jpg', img, encode_param)
    client.files_upload_v2(
                channel=SLACK_CHANNELID,
                initial_comment = ALERT['text'],
                filename = "falling.jpg",
                content = buffer.tobytes()
                )
