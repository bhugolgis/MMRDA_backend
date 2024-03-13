
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


def save_multiple_files(files, file_mapping, file_path , field):
    """
    The function saves multiple files to a specified file path and updates a file mapping dictionary
    with the file paths.
    
    """

    file_list = []
    for file in files:
        if file == False:
            print("file empty")
       
            # print("file is not empty")
            # print(type(file))
        tmp = os.path.join(settings.MEDIA_ROOT, file_path, file.name)
        # print(tmp , "temp")
        path = default_storage.save(tmp, ContentFile(file.read()))
        print(path)
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        file_list.append('/media/' + file_path + '/' + file.name)
        # print(file_list)
    file_mapping[field] = file_list