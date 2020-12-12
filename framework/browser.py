from .singleton_driver import SingleDriver
from .utils.json_utils import JsonUtils
from .logger import logger


class Browser:
    URL = JsonUtils('config.json').get_data('link')
    IMPLICITLY_WAIT = JsonUtils('config.json').get_data('implicitly_wait')

    @staticmethod
    def get_browser():
        browser = SingleDriver().get_driver()
        return browser

    @staticmethod
    def open_url(url=None):
        if url is None:
            url = Browser.URL
        logger.info('Try to get driver')
        browser = Browser.get_browser()
        logger.info(f'Try to open url "{url}"')
        browser.get(url)
        browser.implicitly_wait(Browser.IMPLICITLY_WAIT)

    @staticmethod
    def get_current_url():
        browser = Browser.get_browser()
        return browser.current_url

    @staticmethod
    def get_cookies():
        browser = Browser.get_browser()
        logger.info('Getting cookies')
        return browser.get_cookies()

    @staticmethod
    def get_screenshot(name):
        browser = Browser.get_browser()
        browser.get_screenshot_as_file(name)

    @staticmethod
    def get_cookie(name):
        browser = Browser.get_browser()
        logger.info(f'Getting cookie named as "{name}"')
        return browser.get_cookie(name)

    @staticmethod
    def add_cookie(cookie):
        browser = Browser.get_browser()
        logger.info('Adding cookies')
        browser.add_cookie(cookie)

    @staticmethod
    def change_cookie(name_cookie_to_change, new_value):
        browser = Browser.get_browser()
        logger.info(f'Changing cookies "{name_cookie_to_change}" to new value "{new_value}"')
        cookie_to_change = browser.get_cookie(name_cookie_to_change)
        cookie_to_change['value'] = new_value
        browser.add_cookie(cookie_to_change)

    @staticmethod
    def delete_cookie(name):
        browser = Browser.get_browser()
        logger.info(f'Deleting cookie named as "{name}"')
        browser.delete_cookie(name)

    @staticmethod
    def delete_all_cookies():
        browser = Browser.get_browser()
        logger.info('Deleting all cookies')
        browser.delete_all_cookies()

    @staticmethod
    def maximize():
        browser = SingleDriver().get_driver()
        logger.info('Maximize window')
        browser.maximize_window()

    @staticmethod
    def refresh():
        browser = SingleDriver().get_driver()
        logger.info('Refresh window')
        browser.refresh()

    @staticmethod
    def quit_browser():
        driver = SingleDriver()
        browser = driver.get_driver()
        browser.quit()
        driver.del_driver()

    @staticmethod
    def switch_to_top():
        browser = SingleDriver().get_driver()
        logger.info('Switching to default frame')
        browser.switch_to.default_content()

    @staticmethod
    def switch_to_frame(element):
        browser = SingleDriver().get_driver()
        logger.info('Switching to IFrame')
        browser.switch_to.frame(element.find_element())

    @staticmethod
    def go_to_other_tab():
        browser = SingleDriver().get_driver()
        if len(browser.window_handles[1]) > 1:
            logger.info('Switching to other tab')
            browser.switch_to.window(browser.window_handles[1])

    @staticmethod
    def go_to_main_tab():
        browser = SingleDriver().get_driver()
        logger.info('Switching to main tab')
        browser.switch_to.window(browser.window_handles[0])

    @staticmethod
    def confirm_alert():
        logger.info('Switching to alert and confirm')
        Browser.get_browser().switch_to.alert.accept()

    @staticmethod
    def dismiss_alert():
        logger.info('Switching to alert and dismiss')
        Browser.get_browser().switch_to.alert.dismiss()

    @staticmethod
    def get_text_from_alert():
        logger.info('Getting text from alert')
        return Browser.get_browser().switch_to.alert.text

    @staticmethod
    def input_text_into_alert(text):
        logger.info(f'Prompting "{text}" into alert')
        Browser.get_browser().switch_to.alert.send_keys(text)
