import os
import time
import datetime
import csv
import urllib.request

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
IMAGE_DIR_PATH = os.path.join(ROOT_PATH, 'data', 'images', 'uncategorized')
SYUPPAN_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'syuppan.csv')


def load_novels_csv():
    novels = []

    if not os.path.exists(SYUPPAN_CSV_PATH):
        return novels

    with open(SYUPPAN_CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            novels.append(row)

    return novels


def download_image(url, book_id):
    org_file_name = os.path.basename(url)
    dest_file_name = '{}_{}'.format(book_id, org_file_name)
    dest_path = os.path.join(IMAGE_DIR_PATH, dest_file_name)

    if os.path.exists(dest_path):
        print(datetime.datetime.now().isoformat(), 'Skip:', org_file_name)
        return None

    else:
        print(datetime.datetime.now().isoformat(), 'New :', org_file_name)
        urllib.request.urlretrieve(url, dest_path)
        return dest_path


if __name__ == '__main__':
    for novel in load_novels_csv():
        result = download_image(novel[3], novel[0])

        if result:
            print(datetime.datetime.now().isoformat(), 'Sleep(3)')
            time.sleep(3)

