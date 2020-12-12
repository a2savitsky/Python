import random
import string
from ..logger import logger


class StringUtils:

    @staticmethod
    def get_random_text(length):
        random_text = "".join([random.choice(string.ascii_letters) for i in range(length)])
        logger.info(f'Getting random text "{random_text}"')
        return random_text
