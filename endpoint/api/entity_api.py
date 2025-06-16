from uuid import uuid4

from flask import Blueprint, request, Response, g

from dbe.camera_shot import CameraShot
from service import task_service

entity_api = Blueprint("entity", __name__, url_prefix="/entity")

@entity_api.route("/camera-shot", methods=["POST"])
def create_camera_shot():
    transaction_session = getattr(g, "transaction_session", None)

    shot_name = request.json.get("shot-name")
    device_id = request.json.get("device-id")
    save_frequency = request.json.get("save-frequency")
    timestamp = request.json.get("put-timestamp")

    if shot_name is None or device_id is None:
        return Response(status=500)

    if save_frequency in ("", "0", None):
        save_frequency = None
    else:
        save_frequency = int(save_frequency) * 60

    camera_shot = CameraShot()
    camera_shot.id = uuid4()
    camera_shot.name = shot_name
    camera_shot.device_id = int(device_id)
    camera_shot.shot_frequency_sec = save_frequency
    camera_shot.insert_timestamp = timestamp

    task_service.create_task(camera_shot)

    transaction_session.add(camera_shot)
    return Response(status=200)