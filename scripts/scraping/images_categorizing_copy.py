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

from scripts.utils.category import NarouCategory
from scripts.utils.category import NarouCategory2

NOVELS_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'novels.csv')
IMAGE_DIR_PATH = os.path.join(ROOT_PATH, 'data', 'images')
IMAGE_SRC_DIR_PATH = os.path.join(IMAGE_DIR_PATH, 'uncategorized')


def make_directories(dir_name, category_class):
    for category_id in category_class.categories_reversed.keys():
        dir_path = os.path.join(IMAGE_DIR_PATH, dir_name, str(category_id))
        os.makedirs(dir_path, exist_ok=True)


def load_novels_csv(category_class):
    novels = {}

    if not os.path.exists(NOVELS_CSV_PATH):
        return novels

    with open(NOVELS_CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            book_id = row[0]
            category_id = category_class.to_num(row[2])

            novels[book_id] = {
                'category_id': category_id,
            }

    return novels


def get_image_paths():
    return glob.glob('{}/*.jpg'.format(IMAGE_SRC_DIR_PATH))


def copy_image(src_path, dir_name, category_id):
    file_name = os.path.basename(src_path)
    dest_path = os.path.join(IMAGE_DIR_PATH, dir_name, category_id, file_name)

    if os.path.exists(dest_path):
        print(datetime.datetime.now().isoformat(), 'Skip:', category_id, file_name)
        return None

    else:
        print(datetime.datetime.now().isoformat(), 'New :', category_id, file_name)
        shutil.copy(src_path, dest_path)


if __name__ == '__main__':
    dir_name = 'categorized'
    category_class = NarouCategory

    if len(sys.argv) > 1 and sys.argv[1] == '2':
        dir_name = 'categorized-2'
        category_class = NarouCategory2

    make_directories(dir_name, category_class)

    novels = load_novels_csv(category_class)

    for image_path in get_image_paths():
        file_name = os.path.basename(image_path)
        book_id = re.sub(r'(_.*$)', '', file_name)
        novel = novels.get(book_id)

        if not novel:
            print(datetime.datetime.now().isoformat(), 'Not Found Novel', file_name)
            continue

        category_id = novel.get('category_id')

        if category_id is None:
            print(datetime.datetime.now().isoformat(), 'Unknown Category', file_name, novel)
            continue

        copy_image(image_path, dir_name, str(category_id))

