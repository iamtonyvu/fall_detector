from fall_detector.params import *

def fall_detection_time(detectClasses: dict, timeFall: int) -> int:
    if "0" in detectClasses:
        return timeFall + 1
    return 0
