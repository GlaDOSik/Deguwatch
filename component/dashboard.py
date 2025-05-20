from typing import List

from dbe.camera_shot import CameraShot
from vial.gui.component.gui_component import GuiComponent


class Dashboard(GuiComponent):
    def __init__(self, component_id: str):
        super().__init__(component_id)

    def get_template_path(self) -> str:
        return "dashboard.html"

    def set_camera_shots(self, shots: List[CameraShot]):
        self.component_data["camera_shots"] = shots
