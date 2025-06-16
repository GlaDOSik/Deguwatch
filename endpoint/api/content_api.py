import time

import cv2
from flask import Blueprint, Response, g, send_file, request

from database import DBSession
from dw_configuration import IMAGE_PATH
from service.webcam_service import webcam_service
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

    _, buffer = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_OPTIMIZE), 1])
    return Response(buffer.tobytes(), mimetype="image/jpeg")

@content_api.route("/preview/device/<device_id>", methods=["GET"])
def device_preview(device_id):
    shared_camera = webcam_service.get_shared_camera(int(device_id))
    image = shared_camera.get_frame()
    if image is None:
        return Response(status=404)

    _, buffer = cv2.imencode(".jpg", image)
    return Response(buffer.tobytes(), mimetype="image/jpeg")

@content_api.route("/shot-livestream/<camera_shot_id>")
def livestream(camera_shot_id):
    priority = 0 if request.args.get("p") is None else int(request.args.get("p"))
    width = None if request.args.get("x") is None else int(request.args.get("x"))

    return Response(gen_frames(camera_shot_id, priority, width),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

def gen_frames(camera_shot_id: str, priority, width: int):
    transaction_session = DBSession()

    camera_shot = find_camera_shot_by_id(transaction_session, camera_shot_id)
    transaction_session.close()
    if priority == 1:
        webcam_service.set_priority_device(camera_shot)
    while True:
        if priority == 1:
            webcam_service.set_last_priority_captured(camera_shot)
        frame = webcam_service.get_frame(camera_shot)
        if frame is None:
            break
        else:
            # Encode frame as JPEG
            if width is not None:
                h, w = frame.shape[:2]
                aspect_ratio = h / w
                new_height = int(width * aspect_ratio)
                frame = cv2.resize(frame, (width, new_height))

            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()

            # Yield as a multipart response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(1/15 if priority == 1 else 1.0)