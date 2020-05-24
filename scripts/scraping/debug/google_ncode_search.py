
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    title = '悪役令嬢ですが攻略対象の様子が異常すぎる'
    #title = '元公爵令嬢の就職3～料理人になろうと履歴書を提出しましたが、ゴブリンにダメだしされました～'
    #google_url = 'https://www.google.com/search?q=site:ncode.syosetu.com/novelview/infotop "{}"'.format(title)
    google_url = 'https://www.google.com/search?q=site:ncode.syosetu.com "{}"'.format(title)
    driver.get(google_url)

    # Get first item
    link_elem = driver.find_element_by_css_selector('div#search a')
    print(link_elem.get_attribute('href'))
    print(link_elem.text)
    print('\n')

    # Find from top 5 items
    matched_elem = None
    code = None
    link_list = driver.find_elements_by_css_selector('div#search a')
    for link_elem in link_list[:5]:
        href = link_elem.get_attribute('href')
        print(href)
        print(link_elem.text)
        print('\n')

        matched = re.match(r'^https:\/\/ncode\.syosetu\.com\/(.+)\/$', href)
        if matched:
            matched_elem = link_elem
            code = matched.group(1)
            break

    if matched_elem:
        print(code, matched_elem.text)

    # Capture
    file_path = os.path.join(ROOT_PATH, 'tmp', 'capture.png')
    driver.save_screenshot(file_path)

