from datetime import datetime
from uuid import uuid4, UUID

import cv2
from apscheduler.schedulers.background import BackgroundScheduler

from database import DBSession
from dbe.camera_shot import find_by_id as find_camera_shot_by_id
from dbe.image import Image
from dw_configuration import IMAGE_PATH
from service import webcam_service
from vial.config import app_config


class SaveShotTask:
    def __init__(self, frequency_sec: int, camera_shot_id: UUID):
        self.frequency_sec: int = frequency_sec
        self.scheduler = BackgroundScheduler()
        self.camera_shot_id: UUID = camera_shot_id

    def tick(self):
        transaction_session = DBSession()

        camera_shot = find_camera_shot_by_id(transaction_session, self.camera_shot_id)
        if camera_shot is None:
            return

        image = Image()
        image.id = uuid4()
        image.camera_shot_id = camera_shot.id
        image.timestamp = datetime.now()
        transaction_session.add(image)

        frame = webcam_service.get_frame(camera_shot)
        image_path = app_config.get(IMAGE_PATH)
        cv2.imwrite(image_path + "/" + str(image.id) + ".jpg", frame)

        transaction_session.commit()
        transaction_session.close()

    def start(self):
        self.scheduler.add_job(self.tick, "interval", seconds=self.frequency_sec)
        self.scheduler.start()
