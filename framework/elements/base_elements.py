from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from ..utils.json_utils import JsonUtils
from ..logger import logger
from ..browser import Browser

data = JsonUtils('config.json')
explicitly_wait = data.get_data('explicitly_wait')


class BaseElement:
    def __init__(self, locator=None, name=None):
        self.locator = locator
        self.name = name
        self.browser = Browser.get_browser()
        self.wait = WebDriverWait(self.browser, explicitly_wait)

    def find_element_with_expected_condition(self, expected_condition, element=None, time=15):
        logger.info(f'Finding element named as "{self.name}" with expected condition as "{expected_condition}"')
        return WebDriverWait(self.browser, time).until(expected_condition(element or self.locator))

    def find_element(self):
        logger.info(f'Finding element named as "{self.name}"')
        return self.wait.until(EC.presence_of_element_located(self.locator))

    def find_elements(self):
        logger.info(f'Finding elements named as "{self.name}"')
        return self.wait.until(EC.presence_of_all_elements_located(self.locator))

    def get_text(self):
        logger.info(f'Getting text from element named as "{self.name}"')
        return self.find_element().text

    def find_parent_or_child(self, locator):
        logger.info(f'Finding element named as "{self.name}"')
        return self.browser.find_element(*locator)

    def click(self):
        logger.info(f'Click on element named as "{self.name}"')
        self.find_element().click()

    def click_by_javascript(self):
        logger.info(f'Click on element named as "{self.name}"')
        self.browser.execute_script("arguments[0].click();", self.find_element())

    def get_attribute(self, name):
        logger.info(f'Getting attribute from element named as "{self.name}"')
        return self.find_element().get_attribute(name)

    def is_element_present(self):
        logger.info(f'Checking that element named as "{self.name}" is present')
        try:
            self.find_element()
        except TimeoutException:
            logger.info(f'Element named as "{self.name}" is NOT present')
            return False
        logger.info(f'Element named as "{self.name}" is present')
        return True

    def is_element_displayed(self):
        return self.browser.find_element(*self.locator).is_displayed()
