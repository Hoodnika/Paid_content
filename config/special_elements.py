from urllib.parse import urljoin


from django.core.files.storage import FileSystemStorage
import os

from config.settings import MEDIA_ROOT, MEDIA_URL

NULLABLE = {'blank': True, 'null': True}


class CustomStorage(FileSystemStorage):
    def get_valid_name(self, name):
        return name

    def save(self, name, content, **kwargs):
        return super()._save(name, content)

    location = os.path.join(MEDIA_ROOT, "content")
    base_url = urljoin(MEDIA_URL, "content/")


PRICE_MONTH = 410
PRICE_6_MONTH = 350
PRICE_YEAR = 320
