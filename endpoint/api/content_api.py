import time
from uuid import UUID

import cv2
from flask import Blueprint, Response, g, send_file

from database import DBSession
from dw_configuration import IMAGE_PATH
from service import webcam_service
from dbe.camera_shot import find_by_id as find_camera_shot_by_id
from vial.config import app_config


content_api = Blueprint("content", __name__, url_prefix="/content")

@content_api.route("/image/<image_id>", methods=["GET"])
def camera_shot_image(image_id: str):
    return send_file(app_config.get(IMAGE_PATH) + "/" + image_id + ".jpg", mimetype='image/jpeg')


@content_api.route("/preview/camera/<camera_id>", methods=["GET"])
def camera_preview(camera_id):
    transaction_session = getattr(g, "transaction_session", None)

    camera_shot = find_camera_shot_by_id(transaction_session, camera_id)
    image = webcam_service.get_frame(camera_shot)
    if image is None:
        return Response(status=404)

    _, buffer = cv2.imencode(".jpg", image)
    return Response(buffer.tobytes(), mimetype="image/jpeg")

@content_api.route("/preview/device/<device_id>", methods=["GET"])
def device_preview(device_id):
    shared_camera = webcam_service.get_shared_camera(int(device_id))
    image = shared_camera.get_frame()
    if image is None:
        return Response(status=404)

    _, buffer = cv2.imencode(".jpg", image)
    return Response(buffer.tobytes(), mimetype="image/jpeg")

@content_api.route('/shot-livestream/<params>')
def livestream(params: str):
    split_params = params.split("$")
    return Response(gen_frames(split_params[0], int(split_params[1])),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames(camera_shot_id: str, target_fps: int):
    transaction_session = DBSession()

    camera_shot = find_camera_shot_by_id(transaction_session, camera_shot_id)
    transaction_session.close()
    while True:
        frame = webcam_service.get_frame(camera_shot)
        if frame is None:
            break
        else:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()

            # Yield as a multipart response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(1/target_fps)