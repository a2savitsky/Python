from selenium.webdriver.common.by import By
from ..framework.base_page import BasePage
from ..framework.elements.button import Button


class LeftSideBar(BasePage):
    SIDE_BAR_LOCATOR = (By.XPATH, '//div[@id="side_bar"]')
    MY_PAGE_BUTTON_LOCATOR = (By.XPATH, '//li[@id="l_pr"]')

    def __init__(self):
        super().__init__(locator=self.SIDE_BAR_LOCATOR)

    def click_on_my_page(self):
        Button(self.MY_PAGE_BUTTON_LOCATOR, 'my_page_button').click()
