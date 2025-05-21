from zoneinfo import available_timezones

from flask import Blueprint, url_for, g

from component.available_cameras import AvailableCameras
from component.create_edit_camera_shot import CreateEditCameraShot
from component.dashboard import Dashboard
from dbe import camera_shot
from component.factory.dw_components import AVAILABLE_CAMERAS_ID
from vial.gui.component.common.root_component import Root
from vial.gui.component.component_factory import ComponentRegistry
from dbe.image import find_newest as find_newest_image

dashboard_blueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard")


DASHBOARD_ID = "dashboard"

@dashboard_blueprint.route("/", methods=["GET"])
def get_dashboard():
    transaction_session = getattr(g, "transaction_session", None)
    camera_shots = camera_shot.get_all(transaction_session)

    images = {}
    for shot in camera_shots:
        images[shot.id] = find_newest_image(transaction_session, shot.id)

    dashboard = Dashboard(DASHBOARD_ID)
    dashboard.set_camera_shots(camera_shots, images)

    root = (Root(None)
            .add_content(dashboard)
            .add_css(url_for("static", filename="style-util.css"))
            .add_css("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css")
            .add_js_url("https://cdn.tailwindcss.com")
            .add_js_url(url_for("static", filename="vial.js"))
            .add_js_url(url_for("static", filename="web-component-data.js"))
            .add_js_url(url_for("static", filename="deguwatch.js")))

    return root.render()

@dashboard_blueprint.route("/create", methods=["GET"])
def get_create_camera_shot():
    available_cameras_cmp = ComponentRegistry.create(AVAILABLE_CAMERAS_ID, None)

    create_camera_shot = CreateEditCameraShot("create-camera-shot")
    create_camera_shot.set_available_cameras_cmp(available_cameras_cmp)

    root = (Root(None)
            .add_content(create_camera_shot)
            .add_css(url_for("static", filename="style-util.css"))
            .add_css("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css")
            .add_js_url("https://cdn.tailwindcss.com")
            .add_js_url(url_for("static", filename="vial.js"))
            .add_js_url(url_for("static", filename="web-component-data.js"))
            .add_js_url(url_for("static", filename="deguwatch.js")))

    return root.render()


