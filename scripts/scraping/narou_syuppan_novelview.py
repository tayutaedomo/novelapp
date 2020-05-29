import os
import sys
import time
import datetime
import csv
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
ROOT_PATH = os.path.abspath(ROOT_PATH)

sys.path.append(ROOT_PATH)

from scripts.utils.ncode import GoogleSearch
from scripts.utils.ncode import SyosetuSearch


SYUPPAN_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'syuppan.csv')
NOVELS_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'novels.csv')


def load_syuppan_csv():
    books = []

    if not os.path.exists(SYUPPAN_CSV_PATH):
        return books

    with open(SYUPPAN_CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            books.append(row)

    return books


def create_cache():
    cache = {}

    if not os.path.exists(NOVELS_CSV_PATH):
        return cache

    with open(NOVELS_CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            cache[row[0]] = row[1]  # { book_id, result(0|1), category, ... }

    return cache


def get_ncode(driver, title):
    #return GoogleSearch.get_ncode(driver, title)
    return SyosetuSearch.get_ncode(driver, title)


def get_novel_info(driver, ncode):
    novel = {
        'result': 0,
        'ncode': ncode,
        'title': '',
        'overview': '',
        'author': '',
        'keywords': '',
        'category': '',
        'created_at': '',
        'updated_at': '',
        'comment_count': '',
        'review_count': '',
        'bookmark_count': '',
        'rating_total': '',
        'rating': '',
        'report': '',
        'public': '',
        'word_count': '',
        'time': '',
    }

    if not ncode:
        return novel

    info_top_url = 'https://ncode.syosetu.com/novelview/infotop/ncode/{}/'.format(ncode)
    print(datetime.datetime.now().isoformat(), 'GET:', info_top_url)

    driver.get(info_top_url)

    def strip_text(elem):
        if not elem:
            return None

        if not elem.text:
            return None

        text = elem.text.replace('\n', ',').replace('\r\n', ',')
        text.lstrip().rstrip()
        return text

    try:
        h1_elem = driver.find_element_by_css_selector('h1')
        novel['title'] = h1_elem.text

        td_list = driver.find_elements_by_css_selector('table#noveltable1 td')

        if td_list:
            novel['overview'] = strip_text(td_list[0])
            novel['author'] = strip_text(td_list[1])
            novel['keywords'] = strip_text(td_list[2])
            novel['category'] = strip_text(td_list[3])

        td_list = driver.find_elements_by_css_selector('table#noveltable2 td')

        if td_list:
            novel['created_at'] = strip_text(td_list[0])
            novel['updated_at'] = strip_text(td_list[1])
            novel['comment_count'] = strip_text(td_list[2])
            novel['review_count'] = strip_text(td_list[3])
            novel['bookmark_count'] = strip_text(td_list[4])
            novel['rating_total'] = strip_text(td_list[5])
            novel['rating'] = strip_text(td_list[6])
            novel['report'] = strip_text(td_list[7])
            novel['public'] = strip_text(td_list[8])
            novel['word_count'] = strip_text(td_list[9])
            novel['time'] = datetime.datetime.now().isoformat()

            novel['result'] = 1

    except Exception as e:
        print(datetime.datetime.now().isoformat(), e)

    return novel


def append_novel_to_csv(book_id, novel):
    csv_line = '"{}","{}","{}","{}","{}"'.format(
        book_id,
        novel.get('result'),
        novel.get('category'),
        novel.get('title'),
        novel.get('keywords'),
    )

    with open(NOVELS_CSV_PATH, 'a') as f:
        f.write(csv_line + '\n')


if __name__ == '__main__':
    books = load_syuppan_csv()
    print(datetime.datetime.now().isoformat(), 'Book Count:', len(books))

    cache = create_cache()
    print(datetime.datetime.now().isoformat(), 'Cache Count:', len(cache))

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    limit = 500

    for i, book in enumerate(books):
        if limit == 0:
            print(datetime.datetime.now().isoformat(), 'Stop scraping as over limit')
            break

        book_id = book[0]

        if cache.get(book_id):
            print(datetime.datetime.now().isoformat(), 'Skip:', book_id)

        else:
            limit -= 1

            ncode, elem = get_ncode(driver, book[1])

            if not ncode:
                print(datetime.datetime.now().isoformat(), 'Not found:', book)

            novel = get_novel_info(driver, ncode)

            if novel['result'] == 1:
                cache[str(book_id)] = novel['result']

            print(datetime.datetime.now().isoformat(),
                  'New :', book_id, novel['result'], novel['category'])

            append_novel_to_csv(book_id, novel)

            if i < len(books) - 1:
                print(datetime.datetime.now().isoformat(), 'Sleep(3)')
                time.sleep(3)

