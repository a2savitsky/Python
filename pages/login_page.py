from selenium.webdriver.common.by import By
from ..framework.base_page import BasePage
from ..framework.elements.button import Button
from ..framework.elements.text_box import TextBox


class LoginPage(BasePage):
    LOGIN_PAGE_LOCATOR = (By.XPATH, '//div[@id="index_login"]')
    EMAIL_FIELD_LOCATOR = (By.XPATH, '//input[@id="index_email"]')
    PASSWD_FIELD_LOCATOR = (By.XPATH, '//input[@id="index_pass"]')
    LOGIN_BUTTON_LOCATOR = (By.XPATH, '//button[@id="index_login_button"]')

    def __init__(self):
        super().__init__(locator=self.LOGIN_PAGE_LOCATOR)

    def fill_email_field(self, email):
        TextBox(self.EMAIL_FIELD_LOCATOR, 'email_field').input_text_or_keys(email)

    def fill_password_field(self, password):
        TextBox(self.PASSWD_FIELD_LOCATOR, 'password_field').input_text_or_keys(password)

    def click_on_login_button(self):
        Button(self.LOGIN_BUTTON_LOCATOR, 'login_button').click()
