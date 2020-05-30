import os
import time
import datetime
import csv
import urllib.request

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
IMAGE_DIR_PATH = os.path.join(ROOT_PATH, 'data', 'images', 'uncategorized')
SYUPPAN_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'syuppan.csv')


def load_books_csv():
    books = []

    if not os.path.exists(SYUPPAN_CSV_PATH):
        return books

    with open(SYUPPAN_CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            books.append(row)

    return books


def download_image(url, book_id):
    org_file_name = os.path.basename(url)
    dest_file_name = '{}_{}'.format(book_id, org_file_name)
    dest_path = os.path.join(IMAGE_DIR_PATH, dest_file_name)

    if os.path.exists(dest_path):
        print(datetime.datetime.now().isoformat(), 'Skip:', book_id, org_file_name)
        return None

    else:
        print(datetime.datetime.now().isoformat(), 'New :', book_id, org_file_name)
        urllib.request.urlretrieve(url, dest_path)
        return dest_path


if __name__ == '__main__':
    for book in load_books_csv():
        book_id = book[0]
        img_url = book[3]
        result = download_image(img_url, book[0])

        if result:
            print(datetime.datetime.now().isoformat(), 'Sleep(3)')
            time.sleep(3)

