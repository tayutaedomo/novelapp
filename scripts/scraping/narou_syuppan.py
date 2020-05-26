import os
import time
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SYUPPAN_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'syuppan.csv')


def create_cache():
    cache = {}

    with open(SYUPPAN_CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            cache[row[0]] = True  # { book_id: category, ... }

    return cache


def retrieve_books(page):
    books = []

    list_url = 'https://syosetu.com/syuppan/list/?p={}'.format(page)
    print(datetime.datetime.now().isoformat(), 'GET:', list_url)

    driver.get(list_url)

    scroll_down(driver)

    item_elem_list = driver.find_elements_by_class_name('p-syuppan-list__item')

    now_str = datetime.datetime.now().isoformat()

    for item_elem in item_elem_list:
        book = {
            'title': '',
            'book_id': '',
            'book_url': '',
            'image_url': '',
            'downloaded': False,
        }

        try:
            title_elem = item_elem.find_element_by_class_name('p-syuppan-list__title')
            if title_elem:
                book['title'] = title_elem.text

            img_elem = item_elem.find_element_by_tag_name('img')
            if img_elem:
                book['image_url'] = img_elem.get_attribute('src')

            link_elem = item_elem.find_element_by_tag_name('a')
            if link_elem:
                book['book_url'] = link_elem.get_attribute('href')
                book['book_id'] = book['book_url'].replace(
                    'https://syosetu.com/syuppan/view/bookid/', '')
                book['book_id'] = book['book_id'].replace('/', '')

            book['time'] = now_str

            books.append(book)

        except Exception as e:
            print(datetime.datetime.now().isoformat(), e, book['book_id'], book['title'])

    return books


def scroll_down(driver):
    height = driver.execute_script("return document.body.scrollHeight")
    scroll_y = 150

    for x in range(scroll_y, height, scroll_y):
        driver.execute_script("window.scrollTo(0, "+str(x)+");")


def append_book_to_csv(book):
    csv_line = '"{}","{}","{}","{}", "{}"'.format(
        book['book_id'],
        book['title'],
        book['book_url'],
        book['image_url'],
        book['time'],
    )

    with open(SYUPPAN_CSV_PATH, 'a') as f:
        f.write(csv_line + '\n')


if __name__ == '__main__':
    cache = create_cache()
    print(datetime.datetime.now().isoformat(), 'Count:', len(cache))

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    page_count = 25

    for i in range(1, page_count + 1):
        for book in retrieve_books(i):
            book_id = book['book_id']

            if cache.get(book_id):
                print(datetime.datetime.now().isoformat(), 'Skip:', book_id)

            else:
                cache[book_id] = True
                print(datetime.datetime.now().isoformat(), 'New :', book_id, book['title'])

                append_book_to_csv(book)

        if i < page_count:
            print(datetime.datetime.now().isoformat(), 'Sleep(3)')
            time.sleep(3)

    # Capture
    file_path = os.path.join(ROOT_PATH, 'tmp', 'capture.png')
    driver.save_screenshot(file_path)

