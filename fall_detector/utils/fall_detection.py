from fall_detector.params import *

def fall_detection_time(detectClasses: dict, timeFall: int) -> int:
    """Increase value of successive fall detection

    Args:
        detectClasses (dict): labels predicted
        timeFall (int): Number of successive fall

    Returns:
        int: Number of successive fall
    """
    if "0" in detectClasses:
        return timeFall + 1
    return 0

def build_message(type: str, event: any) -> dict:
    """Build message for WebSockets response

    Args:
        type (str): Message type
        event (any): message

    Returns:
        dict: Message to send
    """
    return {
        "type": type,
        "event": event
    }
