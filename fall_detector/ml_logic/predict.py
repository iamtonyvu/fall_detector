from ultralytics import YOLO
import cv2
import math
import logging
from fall_detector.params import *

def detection(model: YOLO, img: cv2.typing.MatLike, classNames: dict, confidence_indice: int = 50, show_confidence: bool = False) -> cv2.typing.MatLike:
    results = model(img, stream=True)
        # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            if str(int(box.cls[0])) in classNames:
                # confidence
                confidence = math.ceil((box.conf[0]*100))/100
                logging.debug("Confidence --->",confidence)
                if confidence >= confidence_indice/100:
                    # bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                    # class name
                    cls = str(int(box.cls[0]))
                    logging.debug("Class name -->", classNames.get(cls).get('name'))

                    # put box in cam
                    cv2.rectangle(img, (x1, y1), (x2, y2), classNames.get(cls).get('color'), 3)

                    # object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    thickness = 2
                    if show_confidence:
                        cv2.putText(img, f"{classNames.get(cls).get('name')}", org, font, fontScale, classNames.get(cls).get('color'), thickness)
                    else :
                        cv2.putText(img, f"{classNames.get(cls).get('name')} {confidence}", org, font, fontScale, classNames.get(cls).get('color'), thickness)
        return img


if __name__ == '__main__':
    model = YOLO(MODEL_PATCH)
    img = cv2.imread(MODEL_IMAGE_TEST)
    cv2.imshow('Result', detection(model,img,CLASS_NAMES, MODEL_CONFIDENCE, MODEL_CONFIDENCE_VISIBILITY))
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
