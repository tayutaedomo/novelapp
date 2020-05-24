import os
import time
import datetime
import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SYUPPAN_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'syuppan.csv')
NOVELS_CSV_PATH = os.path.join(ROOT_PATH, 'data', 'novels.csv')


def load_syuppan_csv():
    books = []

    with open(SYUPPAN_CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            books.append(row)

    return books


def create_cache():
    cache = {}

    with open(NOVELS_CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            cache[row[0]] = row[1]  # { book_id: category, ... }

    return cache


def retrieve_ncode(driver, title):
    google_url = 'https://www.google.com/search?q=site:ncode.syosetu.com "{}"'.format(title)
    print(datetime.datetime.now().isoformat(), 'GET:', google_url)

    driver.get(google_url)

    matched_elem = None
    code = None

    link_list = driver.find_elements_by_css_selector('div#search a')

    if not link_list:
        return code

    for link_elem in link_list[:5]:
        href = link_elem.get_attribute('href')
        matched = re.match(r'^https:\/\/ncode\.syosetu\.com\/(.+)\/$', href)

        if matched:
            matched_elem = link_elem
            code = matched.group(1)
            break

    return code, matched_elem


def retrieve_novel_info(driver, ncode):
    info_top_url = 'https://ncode.syosetu.com/novelview/infotop/ncode/{}/"'.format(ncode)
    print(datetime.datetime.now().isoformat(), 'GET:', info_top_url)

    driver.get(info_top_url)

    novel_info = {
        'ncode': ncode,
        'success': False,
    }

    td_list = driver.find_elements_by_css_selector('table#noveltable1 td')

    def normalize_text(elem):
        if not elem:
            return None

        if not elem.text:
            return None

        return elem.text.replace('\n', ',').replace('\r\n', ',')

    if td_list:
        novel_info['overview'] = normalize_text(td_list[0])
        novel_info['author'] = normalize_text(td_list[1])
        novel_info['keywords'] = normalize_text(td_list[2])
        novel_info['category'] = normalize_text(td_list[3])

    td_list = driver.find_elements_by_css_selector('table#noveltable2 td')

    if td_list:
        novel_info['created_at'] = normalize_text(td_list[0])
        novel_info['updated_at'] = normalize_text(td_list[1])
        novel_info['comment_count'] = normalize_text(td_list[2])
        novel_info['review_count'] = normalize_text(td_list[3])
        novel_info['bookmark_count'] = normalize_text(td_list[4])
        novel_info['rating_total'] = normalize_text(td_list[5])
        novel_info['rating'] = normalize_text(td_list[6])
        novel_info['report'] = normalize_text(td_list[7])
        novel_info['public'] = normalize_text(td_list[8])
        novel_info['word_count'] = normalize_text(td_list[9])
        novel_info['time'] = datetime.datetime.now().isoformat()
        novel_info['success'] = True

    return novel_info


def append_novel_to_csv(book_id, category):
    csv_line = '"{}","{}"'.format(
        book_id,
        category,
    )

    with open(NOVELS_CSV_PATH, 'a') as f:
        f.write(csv_line + '\n')


if __name__ == '__main__':
    books = load_syuppan_csv()
    print(datetime.datetime.now().isoformat(), 'Count:', len(books))

    cache = create_cache()
    print(datetime.datetime.now().isoformat(), 'Count:', len(cache))

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    for i, book in enumerate(books):
        book_id = book[0]
        category = cache.get(book_id)

        if category:
            print(datetime.datetime.now().isoformat(), 'Skip:', book_id, category)

        else:
            ncode, elem = retrieve_ncode(driver, book[1])

            if not ncode:
                print('Not found ncode.', book)
                break

            novel = retrieve_novel_info(driver, ncode)

            category = novel['category']
            cache[str(book_id)] = category
            print(datetime.datetime.now().isoformat(), 'New :', book_id, category)

            append_novel_to_csv(book_id, category)

            if i < len(books) - 1:
                print(datetime.datetime.now().isoformat(), 'Sleep(3)')
                time.sleep(3)

