from ultralytics import YOLO
import cv2
import math
from fall_detector.params import *

def detection(model: YOLO, img: cv2.typing.MatLike, classNames: dict, confidence_indice: int = 50, show_confidence: bool = False):
    """Predict classNames from image with YOLO model and return image with boxes and class detected

    Args:
        model (YOLO): Yolo model
        img (cv2.typing.MatLike): Image for prediction
        classNames (dict): Labels to predict
        confidence_indice (int, optional): Confidence level to predict. Defaults to 50.
        show_confidence (bool, optional): Defaults to False.

    Returns:
        img (cv2.typing.MatLike): Image predicted with boxes
        detections (dict): Labels predicted
    """
    results = model.predict(img, classes=MODEL_CLASSES, verbose=MODEL_VERBOSE)
    return prediction_result(img, results, classNames, confidence_indice, show_confidence)

def prediction_result(img: cv2.typing.MatLike, results: list, classNames: dict, confidence_indice: int = 50, show_confidence: bool = False):
    """return image with boxes and class detected

    Args:
        img (cv2.typing.MatLike): Image for drawing boxes
        results (list): Result of predoction
        classNames (dict): Labels to predict
        confidence_indice (int, optional): Confidence level to predict. Defaults to 50.
        show_confidence (bool, optional): Defaults to False.

    Returns:
        img (cv2.typing.MatLike): Image predicted with boxes
        detections (dict): Labels predicted
    """
    detections = {}
    for r in results:
        boxes = r.boxes

        for box in boxes:
            confidence = math.ceil((box.conf[0]*100))/100
            if confidence >= confidence_indice/100:
                cls = str(int(box.cls[0]))
                detections[cls] = classNames.get(cls)
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

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
        return img, detections


if __name__ == '__main__':
    """
    Test prediction
    """
    model = YOLO(MODEL_PATCH)
    img = cv2.imread(MODEL_IMAGE_TEST)
    cv2.imshow('Result', detection(model,img,CLASS_NAMES, MODEL_CONFIDENCE, MODEL_CONFIDENCE_VISIBILITY))
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
