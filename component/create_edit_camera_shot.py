from vial.gui.component.gui_component import GuiComponent


class CreateEditCameraShot(GuiComponent):
    def __init__(self, component_id: str):
        super().__init__(component_id)

    def get_template_path(self) -> str:
        return "create-edit-camera-shot.html"

    def set_available_cameras_cmp(self, component: GuiComponent):
        self._add_child(0, component)