from dbe.image import Image
from vial.gui.component.gui_component import GuiComponent


class ImageView(GuiComponent):
    def __init__(self, component_id: str):
        super().__init__(component_id)

    def get_template_path(self) -> str:
        return "image-view.html"

    def set_image(self, image: Image):
        self.component_data["image"] = image
