import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    url = 'https://syosetu.com/syuppan/list/'
    driver.get(url)

    item_elem_list = driver.find_elements_by_class_name('p-syuppan-list__item')

    for item_elem in item_elem_list[:1]:
        title_elem = item_elem.find_element_by_class_name('p-syuppan-list__title')
        if title_elem:
            print(title_elem.text)  # TODO

        img_elem = item_elem.find_element_by_tag_name('img')
        if img_elem:
            print(img_elem.get_attribute('src'))    # TODO

        link_elem = item_elem.find_element_by_tag_name('a')
        if link_elem:
            print(link_elem.get_attribute('href'))  # TODO

    # Capture
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'capture.png')
    driver.save_screenshot(file_path)

