from typing import Optional

from database import DBSession
from dbe.camera_shot import CameraShot
from domain.save_shot_task import SaveShotTask
from dbe.camera_shot import get_all as get_all_camera_shots

tasks = {}

def create_task(camera_shot: CameraShot):
    if camera_shot.shot_frequency_sec is None:
        return
    task = SaveShotTask(camera_shot.shot_frequency_sec, camera_shot.id)
    task.start()
    tasks[str(camera_shot.id)] = task

def initialize_tasks():
    transaction_session = DBSession()
    shots = get_all_camera_shots(transaction_session)
    for shot in shots:
        create_task(shot)
    transaction_session.close()
