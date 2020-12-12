from hamcrest import assert_that, equal_to
import allure
from ..framework.utils.strings import StringUtils
from ..framework.utils.json_utils import JsonUtils
from ..framework.utils.image_utils import ImageUtils
from ..pages.login_page import LoginPage
from ..pages.my_page import MyPage
from ..pages.left_side_bar import LeftSideBar
from ..steps.login_page_steps import LoginPageSteps
from ..vk_utils.vk_api_utils import VkApiUtils, VkTypeObject


class TestVkPosting:
    EMAIL = JsonUtils('credentials.json').get_data('email')
    PASSWORD = JsonUtils('credentials.json').get_data('password')
    USER_VK_ID = JsonUtils('test_data.json').get_data('user_vk_id')
    TOKEN = JsonUtils('credentials.json').get_data('token')
    VERSION = JsonUtils('test_data.json').get_data('vk_api_version')
    IMAGE_TO_UPLOAD = JsonUtils('test_data.json').get_data('image_to_upload')
    IMAGE_TO_DOWNLOAD = JsonUtils('test_data.json').get_data('image_to_download')
    LENGTH_RANDOM_STRING = 100
    vk_api = VkApiUtils(token=TOKEN, version=VERSION)
    login_page = LoginPage()
    my_page = MyPage()
    left_side_bar = LeftSideBar()

    def test_vk_posting(self):

        with allure.step('Go to login page'):
            assert_that(self.login_page.is_page_open(), equal_to(True), 'Login page is not open')

        with allure.step('Authorization'):
            LoginPageSteps.log_in(email=self.EMAIL, password=self.PASSWORD)
            assert_that(self.left_side_bar.is_page_open(), equal_to(True), 'Side bar is not open')

        with allure.step('Go to "My page"'):
            self.left_side_bar.click_on_my_page()
            assert_that(self.my_page.is_page_open(), equal_to(True), '"My page" is not open')

        with allure.step('Make post by API'):
            message_orig = StringUtils.get_random_text(self.LENGTH_RANDOM_STRING)
            post_id = self.vk_api.make_post_on_wall(message_orig)

        with allure.step('Verify that post was added by UI'):
            assert_that(self.my_page.get_text_from_post(post_id=post_id), equal_to(message_orig), 'Texts do not match')
            assert_that(self.my_page.get_author_id(item_id=post_id), equal_to(self.USER_VK_ID), 'Users do not match')

        with allure.step('Edit post and upload photo by API'):
            message_change = StringUtils.get_random_text(self.LENGTH_RANDOM_STRING)
            photo_id = self.vk_api.upload_image_to_post(image=self.IMAGE_TO_UPLOAD, message=message_change, post_id=post_id)

        with allure.step('Verify that post was edited and photo is present by UI'):
            self.my_page.download_image(item_id=post_id, photo_id=photo_id, image_name=self.IMAGE_TO_DOWNLOAD)
            assert_that(self.my_page.get_text_from_post(post_id=post_id), equal_to(message_change), 'Texts do not match')
            assert_that(ImageUtils.is_two_images_equal(self.IMAGE_TO_UPLOAD, self.IMAGE_TO_DOWNLOAD), equal_to(True),
                        'Images do not match')

        with allure.step('Add comment to the post by API'):
            comment = StringUtils.get_random_text(self.LENGTH_RANDOM_STRING)
            comment_id = self.vk_api.make_comment_to_post(message=comment, post_id=post_id)

        with allure.step('Verify that comment was added by UI'):
            self.my_page.open_comment_area(post_id=post_id)
            assert_that(self.my_page.get_text_from_comment(post_id=post_id, comment_id=comment_id), equal_to(comment),
                        'Texts do not match')
            assert_that(self.my_page.get_author_id(item_id=comment_id), equal_to(self.USER_VK_ID), 'Users do not match')

        with allure.step('Put like to the comment by UI'):
            self.my_page.click_on_like_button(item_id=comment_id)

        with allure.step('Verify that like is present by API'):
            assert_that(self.vk_api.is_like_present_from(VkTypeObject.COMMENT, item_id=comment_id, owner_id=self.USER_VK_ID),
                        equal_to(True), 'Like is not present')

        with allure.step('Delete the post by API'):
            self.vk_api.delete_post_from_wall(post_id=post_id)

        with allure.step('Verify that post was deleted by UI'):
            assert_that(self.my_page.is_post_on_wall_deleted(post_id=post_id), equal_to(True), 'Post is not deleted')
