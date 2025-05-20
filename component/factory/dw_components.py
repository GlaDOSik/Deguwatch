from component.available_cameras import AvailableCameras
from vial.gui.component.component_factory import ComponentRegistry
from vial.webcallback.web_callback import WebCallback
from service import webcam_service

AVAILABLE_CAMERAS_ID = "available-cameras"

@ComponentRegistry.register(AVAILABLE_CAMERAS_ID)
def create_available_cameras_cmp(callback: WebCallback):
    available_cameras = webcam_service.list_available_cameras()

    available_cameras_cmp = AvailableCameras("available-cameras")
    available_cameras_cmp.set_device_ids(available_cameras)

    return available_cameras_cmp