
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


def save_multiple_files(files, file_mapping, file_path , field):

    file_list = []
    for file in files:
        tmp = os.path.join(settings.MEDIA_ROOT, file_path, file.name)
        path = default_storage.save(tmp, ContentFile(file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        file_list.append('/media/' + file_path + '/' + file.name)
    file_mapping[field] = file_list