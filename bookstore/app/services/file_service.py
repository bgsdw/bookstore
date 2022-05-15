import base64
from django.core.files.base import ContentFile


class FileService:
    @classmethod
    def base64_to_file(self, data, filename):
        _, _img_str = data.split(';base64,')
        return ContentFile(base64.b64decode(_img_str), filename)