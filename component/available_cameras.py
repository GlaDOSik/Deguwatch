from vial.gui.component.gui_component import GuiComponent


class AvailableCameras(GuiComponent):
    def __init__(self, component_id: str):
        super().__init__(component_id)

    def get_template_path(self) -> str:
        return "available-cameras.html"

    def set_device_ids(self, device_ids: [int]):
        self.component_data["device_ids"] = device_ids