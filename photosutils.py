from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime


def get_exif_date(file_path):
    with Image.open(file_path) as img:
        exif_data = img._getexif()
        if not exif_data:
            raise ValueError('no EXIF data')
        
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'DateTimeOriginal':
                date_obj = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                return date_obj.strftime("%Y%m%d")

        raise ValueError('no DateTimeOriginal data')


def rename_by_date(file_path):
    file_path = os.path.expanduser(file_path)
    exif_date = get_exif_date(file_path)
    current_name = os.path.basename(file_path)

    if current_name.startswith(exif_date):
        print(f'{file_path} passed')
        return None 
    
    dir_name = os.path.dirname(file_path)
    base_name = os.path.splitext(current_name)[0]
    ext = os.path.splitext(current_name)[1]

    new_name = f'{exif_date}-{base_name}{ext}'
    new_path = os.path.join(dir_name, new_name)

    os.rename(file_path, new_path)
    print('done')
    return None