from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from ..framework.base_page import BasePage
from ..framework.elements.label import Label
from ..framework.elements.link import Link
from ..framework.elements.button import Button
from ..framework.utils.api_utils import APIUtils
from ..framework.utils.regex_utils import RegexUtils


class MyPage(BasePage):
    AUTHOR_ID_REGEX = r'\d+'
    MY_PAGE_LOCATOR = (By.XPATH, '//div[@id="page_info_wrap"]')
    MORE_ACT_IMAGE_LINK_LOCATOR = (By.XPATH, '//a[@class="pv_actions_more"]')
    DOWNLOAD_IMAGE_LINK_LOCATOR = (By.XPATH, '//a[@id="pv_more_act_download"]')
    CLOSE_LAYER_IMAGE_LOCATOR = (By.XPATH, '//div[@id="layer"]//div[@class="pv_close_btn"]')
    POST_WALL_LOCATOR_FORMAT = '//div[contains(@id, "post") and contains(@id, "{post_id}")]'
    POST_WALL_TEXT_LOCATOR_FORMAT = '//div[contains(@id, "post") and contains(@id, "{post_id}")]//div[contains(@class,'\
                                    ' "wall_post_text")]'
    AUTHOR_LINK_LOCATOR_FORMAT = '//div[contains(@id, "{item_id}")]//a[@class="author"]'
    COMMENT_WALL_TEXT_LOCATOR_FORMAT = '//div[contains(@id, "post") and contains(@id, "{post_id}")]//div[contains(@id,'\
                                       ' "{comment_id}")]//div[@class="wall_reply_text"]'
    LIKE_BUTTON_LOCATOR_FORMAT = '//div[contains(@id, "{item_id}")]//div[@class="like_button_icon"]'
    IMAGE_WALL_LOCATOR_FORMAT = '//div[contains(@id, "{item_id}")]//a[contains(@data-photo-id, "{photo_id}")]'
    OPEN_COMMENT_BUTTON_LOCATOR_FORMAT = '//div[contains(@id, "post") and contains(@id, "{post_id}")]//' \
                                         'a[contains(@class, "replies_next")]'

    def __init__(self):
        super().__init__(locator=self.MY_PAGE_LOCATOR)

    def open_comment_area(self, post_id):
        Button((By.XPATH, self.OPEN_COMMENT_BUTTON_LOCATOR_FORMAT.format(post_id=post_id))).click()

    def get_text_from_post(self, post_id):
        return Label((By.XPATH, self.POST_WALL_TEXT_LOCATOR_FORMAT.format(post_id=post_id))).get_text()

    def get_text_from_comment(self, post_id, comment_id):
        return Label(
            (By.XPATH, self.COMMENT_WALL_TEXT_LOCATOR_FORMAT.format(post_id=post_id, comment_id=comment_id))).get_text()

    def get_author_id(self, item_id):
        url = Link((By.XPATH, self.AUTHOR_LINK_LOCATOR_FORMAT.format(item_id=item_id))).get_attribute('href')
        return RegexUtils.get_part_string_by_regex(string=url, regex=self.AUTHOR_ID_REGEX)[0]

    def click_on_like_button(self, item_id):
        Button((By.XPATH, self.LIKE_BUTTON_LOCATOR_FORMAT.format(item_id=item_id))).click_by_javascript()

    def download_image(self, item_id, photo_id, image_name):
        Link((By.XPATH, self.IMAGE_WALL_LOCATOR_FORMAT.format(item_id=item_id, photo_id=photo_id))).click()
        Link(self.MORE_ACT_IMAGE_LINK_LOCATOR).click()
        url = Link(self.DOWNLOAD_IMAGE_LINK_LOCATOR).get_attribute('href')
        APIUtils.download_file(url=url, file_name=image_name)
        Button(self.CLOSE_LAYER_IMAGE_LOCATOR).click()

    def is_post_on_wall_deleted(self, post_id):
        post = Label((By.XPATH, self.POST_WALL_LOCATOR_FORMAT.format(post_id=post_id)))
        post.find_element_with_expected_condition(EC.invisibility_of_element_located)
        return not post.is_element_displayed()
