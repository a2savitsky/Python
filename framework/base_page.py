from .elements.label import Label


class BasePage:
    def __init__(self, locator=None):
        self.locator = locator

    def is_page_open(self):
        elem = Label(self.locator)
        return elem.is_element_present()
