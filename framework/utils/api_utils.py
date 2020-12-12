import requests


class APIUtils:
    def __init__(self, url, user=None, password=None):
        self._user = user
        self._password = password
        self._url = url.format(user=self._user, password=self._password)

    def _post(self, path="", url=None, files=None, data=None, json=None, headers=None, exp_status_code=None):
        full_url = self._url + path if url is None else url
        response = requests.post(url=full_url, files=files, data=data, json=json, headers=headers)
        if exp_status_code is not None:
            self.__check_status_code(response, exp_status_code)
        return response.json()

    def _get(self, path="", params=None, headers=None, exp_status_code=None):
        response = requests.get(url=self._url + path, params=params, headers=headers)
        if exp_status_code is not None:
            self.__check_status_code(response, exp_status_code)
        return response.json()

    @staticmethod
    def __check_status_code(response, exp_status_code):
        assert response.status_code == exp_status_code, f'Status code is not {exp_status_code}'

    @staticmethod
    def download_file(url, file_name):
        r = requests.get(url=url)
        with open(file_name, 'wb') as f:
            f.write(r.content)
