import os
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

IMAGE_DIR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'images')


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


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    site_url = 'https://syosetu.com/syuppan/list/'
    driver.get(site_url)

    book_list = []

    item_elem_list = driver.find_elements_by_class_name('p-syuppan-list__item')

    for item_elem in item_elem_list[:1]:
        book_info = {
            'title': '',
            'book_id': '',
            'book_url': '',
            'image_url': '',
            'downloaded': False,
        }

        title_elem = item_elem.find_element_by_class_name('p-syuppan-list__title')
        if title_elem:
            book_info['title'] = title_elem.text

        img_elem = item_elem.find_element_by_tag_name('img')
        if img_elem:
            book_info['image_url'] = img_elem.get_attribute('src')

        link_elem = item_elem.find_element_by_tag_name('a')
        if link_elem:
            book_info['book_url'] = link_elem.get_attribute('href')
            book_info['book_id'] = book_info['book_url'].replace('https://syosetu.com/syuppan/view/bookid/', '')
            book_info['book_id'] = book_info['book_id'].replace('/', '')

        # Image Download
        book_info['downloaded'] = download_image(book_info['image_url'], book_info['book_id'])

        print(book_info)

        book_list.append(book_info)

    # Capture
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'capture.png')
    driver.save_screenshot(file_path)

