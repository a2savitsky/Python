from ..framework.utils.api_utils import APIUtils
from ..framework.utils.json_utils import JsonUtils


class VkApiUtils(APIUtils):
    URL = JsonUtils('config.json').get_data('vk_api_url')

    def __init__(self, token, version):
        super().__init__(url=self.URL)
        self._token = '&access_token=' + str(token)
        self._version = '?v=' + version

    def make_post_on_wall(self, message, user_id=None):
        data = {'message': message, 'owner_id': user_id}
        return self._post(path='wall.post' + self._version + self._token, data=data)['response']['post_id']

    def upload_image_to_post(self, image, post_id, message=None):
        server = self._post(path='photos.getWallUploadServer' + self._version + self._token)['response']['upload_url']
        file = {'photo': open(image, 'rb')}
        upload = self._post(url=server, files=file)
        file['photo'].close()
        response = self._post(path='photos.saveWallPhoto' + self._version + self._token, data=upload)
        photo_id = str(response['response'][0]['id'])
        owner_id = str(response['response'][0]['owner_id'])
        data = {'message': message, 'post_id': post_id, 'attachments': 'photo' + owner_id + '_' + photo_id}
        self._post(path='wall.edit' + self._version + self._token, data=data)
        return photo_id

    def make_comment_to_post(self, message, post_id):
        data = {'message': message, 'post_id': post_id}
        return self._post(path='wall.createComment' + self._version + self._token, data=data)['response']['comment_id']

    def is_like_present_from(self, type_of_object, owner_id, item_id):
        data = {'type': type_of_object, 'owner_id': owner_id, 'item_id': item_id}
        response = self._get(path='likes.isLiked' + self._version + self._token, params=data)
        return True if response['response']['liked'] == 1 else False

    def delete_post_from_wall(self, post_id):
        data = {'post_id': post_id}
        return self._post(path='wall.delete' + self._version + self._token, data=data)


class VkTypeObject:
    POST = 'post'
    COMMENT = 'comment'
    PHOTO = 'photo'
    AUDIO = 'audio'
    VIDEO = 'video'
    NOTE = 'note'
    PHOTO_COMMENT = 'photo_comment'
    VIDEO_COMMENT = 'video_comment'
    TOPIC_COMMENT = 'topic_comment'
