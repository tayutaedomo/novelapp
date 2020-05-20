import os
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
IMAGE_DIR_PATH = os.path.join(ROOT_PATH, 'data', 'images')
CSV_PATH = os.path.join(ROOT_PATH, 'data', 'syuppan.csv')


def download_image(url, book_id):
    org_file_name = os.path.basename(url)
    dest_file_name = '{}_{}'.format(book_id, org_file_name)
    dest_path = os.path.join(IMAGE_DIR_PATH, dest_file_name)
    print(dest_path, os.path.exists(dest_path))

    if os.path.exists(dest_path):
        return False    # Skip if already exits
    else:
        urllib.request.urlretrieve(url, dest_path)
        return True


def append_book_to_csv(book):
    csv_line = '"{}","{}","{}","{}"'.format(
        book['book_id'],
        book['title'],
        book['book_url'],
        book['image_url']
    )

    with open(CSV_PATH, 'a') as f:
        f.write(csv_line + '\n')


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    site_url = 'https://syosetu.com/syuppan/list/'
    driver.get(site_url)

    book_list = []

    item_elem_list = driver.find_elements_by_class_name('p-syuppan-list__item')

    for item_elem in item_elem_list[:2]:
        book = {
            'title': '',
            'book_id': '',
            'book_url': '',
            'image_url': '',
            'downloaded': False,
        }

        title_elem = item_elem.find_element_by_class_name('p-syuppan-list__title')
        if title_elem:
            book['title'] = title_elem.text

        img_elem = item_elem.find_element_by_tag_name('img')
        if img_elem:
            book['image_url'] = img_elem.get_attribute('src')

        link_elem = item_elem.find_element_by_tag_name('a')
        if link_elem:
            book['book_url'] = link_elem.get_attribute('href')
            book['book_id'] = book['book_url'].replace('https://syosetu.com/syuppan/view/bookid/', '')
            book['book_id'] = book['book_id'].replace('/', '')

        # Image Download
        book['downloaded'] = download_image(book['image_url'], book['book_id'])

        book_list.append(book)

        append_book_to_csv(book)

        print(book)

    # Capture
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'capture.png')
    driver.save_screenshot(file_path)

