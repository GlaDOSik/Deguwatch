from datetime import datetime
from typing import List, Optional

import cv2

from dbe.camera_shot import CameraShot
from domain.shared_camera import SharedCamera


physical_cameras = {}

def initialize_cameras(max_test=10):
    for device_id in range(max_test):
        cap = cv2.VideoCapture(device_id)
        if cap.isOpened():
            # Try to get max resolution
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)

            ret, frame = cap.read()
            if ret:
                physical_cameras[device_id] = SharedCamera(cap)
                continue
        cap.release()

def get_frame(camera_shot: CameraShot):
    frame = physical_cameras.get(camera_shot.device_id).get_frame()
    cv2.putText(
        frame,
        camera_shot.name,
        (10, 30),  # Position (x, y)
        cv2.FONT_HERSHEY_SIMPLEX,  # Font
        1,  # Font scale
        (255, 255, 255),  # Color (white)
        2,  # Thickness
        cv2.LINE_AA  # Line type
    )
    if camera_shot.insert_timestamp is True:
        _insert_timestamp_to_frame(frame)
    return frame

def get_shared_camera(device_id: int) -> Optional[SharedCamera]:
    return physical_cameras.get(device_id)

def list_available_cameras() -> [int]:
    return physical_cameras.keys()

def _insert_timestamp_to_frame(frame):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(
        frame,
        timestamp,
        (10, 60),  # Position (x, y)
        cv2.FONT_HERSHEY_SIMPLEX,  # Font
        1,  # Font scale
        (255, 255, 255),  # Color (white)
        2,  # Thickness
        cv2.LINE_AA  # Line type
    )