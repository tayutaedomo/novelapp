from selenium import webdriver

url = 'https://syosetu.com/syuppan/list/'

browser = webdriver.Chrome()
browser.get(url)

item_elem_list = browser.find_elements_by_class_name('p-syuppan-list__item')

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


browser.quit()

