import os
import sys
import datetime
import re
import csv
import glob
import shutil

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
ROOT_PATH = os.path.abspath(ROOT_PATH)

sys.path.append(ROOT_PATH)

from scripts.utils.narou_category import NarouCategory

NOVELS_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'novels.csv')
IMAGE_DIR_PATH = os.path.join(ROOT_PATH, 'data', 'images')


def make_directories():
    for category_id in NarouCategory.categories_reversed.keys():
        dir_path = os.path.join(IMAGE_DIR_PATH, 'categorized', str(category_id))
        os.makedirs(dir_path, exist_ok=True)


def load_novels_csv():
    novels = {}

    with open(NOVELS_CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            novels[row[0]] = NarouCategory.to_num(row[1])

    return novels


def get_image_paths():
    return glob.glob('{}/*.jpg'.format(IMAGE_DIR_PATH))


def copy_image(src_path, category_id):
    file_name = os.path.basename(src_path)
    dest_path = os.path.join(IMAGE_DIR_PATH, 'categorized', category_id, file_name)

    if os.path.exists(dest_path):
        print(datetime.datetime.now().isoformat(), 'Skip:', category_id, file_name)
        return None

    else:
        print(datetime.datetime.now().isoformat(), 'New :', category_id, file_name)
        shutil.copy(src_path, dest_path)


if __name__ == '__main__':
    make_directories()

    novels = load_novels_csv()

    for image_path in get_image_paths():
        file_name = os.path.basename(image_path)
        book_id = re.sub(r'(_.*$)', '', file_name)
        category_id = novels.get(book_id)

        if not category_id:
            print(datetime.datetime.now().isoformat(), 'Category is unknown', file_name)
            continue

        copy_image(image_path, str(category_id))

