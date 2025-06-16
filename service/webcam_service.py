import threading
import time
from datetime import datetime
from typing import List, Optional

import cv2

from dbe.camera_shot import CameraShot
from domain.shared_camera import SharedCamera
from domain.shared_camera import generate_static_frame

class WebcamService:
    def __init__(self):
        self.static_frame = generate_static_frame()
        self.physical_cameras = {}
        self.thread = threading.Thread(target=self.update_frames, daemon=True)
        self.priority_device = None

    def set_priority_device(self, camera_shot: CameraShot):
        self.priority_device = camera_shot.device_id

    def set_last_priority_captured(self, camera_shot: CameraShot):
        shared_camera = self.physical_cameras.get(camera_shot.device_id)
        shared_camera.last_captured = int(time.time())

    def update_frames(self):
        while True:
            if self.priority_device is not None:
                priority_cam = self.physical_cameras.get(self.priority_device)
                if not priority_cam.is_priority:
                    for shared_camera in self.physical_cameras.values():
                        shared_camera.remove_priority()
                    priority_cam.set_priority()
                elif int(time.time()) - priority_cam.last_captured > 2:
                    self.priority_device = None
            else:
                for shared_camera in self.physical_cameras.values():
                    if shared_camera.is_priority:
                        shared_camera.remove_priority()
                    shared_camera.update()
            time.sleep(5.0)

    def start_updates(self):
        self.thread.start()

    def initialize_cameras(self, max_test=10):
        for device_id in range(max_test):
            cap = cv2.VideoCapture(device_id)
            if cap.isOpened():
                # Try to get max resolution
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)

                ret, frame = cap.read()
                if ret:
                    self.physical_cameras[device_id] = SharedCamera(device_id)
                    continue
            cap.release()

    def get_frame(self, camera_shot: CameraShot):
        shared_camera = self.physical_cameras.get(camera_shot.device_id)
        frame = None
        if shared_camera is None:
            frame = self.static_frame
        else:
            frame = shared_camera.get_frame()
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
        if camera_shot.insert_timestamp is True and shared_camera is not None:
            self._insert_timestamp_to_frame(frame)
        return frame

    def get_shared_camera(self, device_id: int) -> Optional[SharedCamera]:
        return self.physical_cameras.get(device_id)

    def list_available_cameras(self) -> [int]:
        return self.physical_cameras.keys()

    def _insert_timestamp_to_frame(self, frame):
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

webcam_service = WebcamService()