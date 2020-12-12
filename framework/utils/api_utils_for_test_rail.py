from .api_utils import APIUtils


class APIUtilsTestRail(APIUtils):
    HEADERS = {'Content-Type': 'application/json'}

    def add_attachment_to_result(self, result_id, file):
        files = {'attachment': open(file, 'rb')}
        response = self._post(path=f'index.php?/api/v2/add_attachment_to_result/{result_id}', files=files)
        files['attachment'].close()
        return response

    def add_results_to_test(self, test_id, status, comment=None, data=None):
        req = {'status_id': status, 'comment': comment}
        req.update(data) if data is not None else None
        response = self._post(path=f'index.php?/api/v2/add_result/{test_id}', json=req, headers=self.HEADERS)
        return response


class ResultStatusTestRail:
    PASSED = 1
    BLOCKED = 2
    RETEST = 4
    FAILED = 5
    PASSED_WITH_ISSUES = 6
