from flask import Blueprint, url_for, g

from component.image_view import ImageView
from component.shot_livestream import ShotLivestream
from vial.gui.component.common.root_component import Root
from dbe import camera_shot
from dbe.image import find_by_id as find_image_by_id

shot_blueprint = Blueprint("shot", __name__, url_prefix="/shot")

SHOT_LIVESTREAM_ID = "shot-livestream"
IMAGE_VIEW_ID = "image-view"


@shot_blueprint.route("/<camera_shot_id>", methods=["GET"])
def get_shot_livestream(camera_shot_id: str):
    transaction_session = getattr(g, "transaction_session", None)

    camera_shot_entity = camera_shot.find_by_id(transaction_session, camera_shot_id)

    shot_livestream = ShotLivestream(SHOT_LIVESTREAM_ID)
    shot_livestream.set_camera_shot(camera_shot_entity)

    root = (Root(None)
            .add_content(shot_livestream)
            .add_css(url_for("static", filename="style-util.css"))
            .add_css("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css")
            .add_js_url("https://cdn.tailwindcss.com")
            .add_js_url(url_for("static", filename="vial.js"))
            .add_js_url(url_for("static", filename="web-component-data.js"))
            .add_js_url(url_for("static", filename="deguwatch.js")))

    return root.render()

@shot_blueprint.route("/image/<image_id>", methods=["GET"])
def get_shot_image(image_id):
    transaction_session = getattr(g, "transaction_session", None)

    image = find_image_by_id(transaction_session, image_id)

    image_view = ImageView(IMAGE_VIEW_ID)
    image_view.set_image(image)

    root = (Root(None)
            .add_content(image_view)
            .add_css(url_for("static", filename="style-util.css"))
            .add_css("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css")
            .add_js_url("https://cdn.tailwindcss.com")
            .add_js_url(url_for("static", filename="vial.js"))
            .add_js_url(url_for("static", filename="web-component-data.js"))
            .add_js_url(url_for("static", filename="deguwatch.js")))

    return root.render()