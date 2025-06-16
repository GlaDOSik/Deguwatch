import threading
import time

import cv2
import numpy as np

class SharedCamera:
    def __init__(self, device_id):
        self.device_id = device_id
        self.frame = generate_static_frame()
        self.thread = None
        self.is_priority = False
        self.capture = None
        self.last_captured = 0

    def update(self):
        cap = cv2.VideoCapture(self.device_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
        ret, frame = cap.read()
        if ret:
            self.frame = frame
        cap.release()

    def set_priority(self):
        self.is_priority = True
        self.capture = cv2.VideoCapture(self.device_id)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
        self.thread = threading.Thread(target=self._update_internal, daemon=True)
        self.thread.start()

    def remove_priority(self):
        self.is_priority = False
        if self.thread is not None:
            self.thread.join()
        self.thread = None
        if self.capture is not None:
            self.capture.release()
        self.capture = None

    def _update_internal(self):
        while self.is_priority:
            ret, frame = self.capture.read()
            if ret:
                self.frame = frame
            time.sleep(1/15)

    def get_frame(self):
        return self.frame.copy() if self.frame is not None else None

def generate_static_frame(width=640, height=480):
    background_color = (0, 0, 255)  # BGR format
    return np.full((height, width, 3), background_color, dtype=np.uint8)
