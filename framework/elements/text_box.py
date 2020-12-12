from .base_elements import BaseElement


class TextBox(BaseElement):

    def input_text_or_keys(self, keys):
        self.find_element().send_keys(keys)

    def clear(self):
        self.find_element().clear()
