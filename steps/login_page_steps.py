from ..pages.login_page import LoginPage


class LoginPageSteps:

    @staticmethod
    def log_in(email, password):
        login_page = LoginPage()
        login_page.fill_email_field(email=email)
        login_page.fill_password_field(password=password)
        login_page.click_on_login_button()
