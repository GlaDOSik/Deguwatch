from dbe.image import Image
from vial.gui.component.gui_component import GuiComponent


class ImageView(GuiComponent):
    def __init__(self, component_id: str):
        super().__init__(component_id)

    def get_template_path(self) -> str:
        return "image-view.html"

    def set_images(self, prev_image: Image, current_image: Image, next_image: Image):
        self.component_data["prev_image"] = prev_image
        self.component_data["image"] = current_image
        self.component_data["next_image"] = next_image