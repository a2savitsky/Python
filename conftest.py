import pytest
from .framework.browser import Browser
from .framework.utils.api_utils_for_test_rail import APIUtilsTestRail, ResultStatusTestRail
from .framework.utils.json_utils import JsonUtils

url = JsonUtils('config.json').get_data('testrail_url')
user = JsonUtils('credentials.json').get_data('user_testrail')
password = JsonUtils('credentials.json').get_data('password_testrail')
screenshot = JsonUtils('test_data.json').get_data('screenshot_name')
test_id = JsonUtils('test_data.json').get_data('test_testrail_id')
comment = JsonUtils('test_data.json').get_data('comment_to_testrail_result')
testrail = APIUtilsTestRail(url=url, user=user, password=password)


@pytest.fixture(autouse=True)
def browser():
    Browser.open_url()
    Browser.maximize()
    yield
    Browser.get_screenshot(screenshot)
    Browser.quit_browser()


def pytest_sessionfinish(exitstatus):
    status = ResultStatusTestRail.PASSED if exitstatus == 0 else ResultStatusTestRail.FAILED
    response = testrail.add_results_to_test(test_id=test_id, status=status, comment=comment)
    testrail.add_attachment_to_result(result_id=response['id'], file=screenshot)
