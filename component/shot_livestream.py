from dbe.camera_shot import CameraShot
from vial.gui.component.gui_component import GuiComponent


class ShotLivestream(GuiComponent):
    def __init__(self, component_id: str):
        super().__init__(component_id)

    def get_template_path(self) -> str:
        return "shot-livestream.html"

    def set_camera_shot(self, camera_shot: CameraShot):
        self.component_data["camera_shot"] = camera_shot