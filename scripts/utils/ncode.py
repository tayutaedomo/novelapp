import datetime
import re


class SyosetuSearch:
    @classmethod
    def get_ncode(cls, driver, title):
        base_url = 'https://yomou.syosetu.com/search.php?word={}&order=new'
        url = base_url.format(title)

        print(datetime.datetime.now().isoformat(), 'GET:', url)

        driver.get(url)

        code = None
        matched_elem = None

        try:
            link_elem = driver.find_element_by_link_text('小説情報')
            href = link_elem.get_attribute('href')
            matched = re.match(r'^https:\/\/ncode\.syosetu\.com\/(.+)\/$', href)

            if matched:
                matched_elem = link_elem
                code = matched.group(1)

        except Exception as e:
            print(datetime.datetime.now().isoformat(), e)

        return code, matched_elem


class GoogleSearch:
    @classmethod
    def get_ncode(cls, driver, title):
        url = 'https://www.google.com/search?q=site:ncode.syosetu.com {}'.format(title)
        print(datetime.datetime.now().isoformat(), 'GET:', url)

        driver.get(url)

        matched_elem = None
        code = None

        link_list = driver.find_elements_by_css_selector('div#search a')

        if not link_list:
            return code, matched_elem

        for link_elem in link_list[:5]:
            href = link_elem.get_attribute('href')
            matched = re.match(r'^https:\/\/ncode\.syosetu\.com\/(.+)\/$', href)

            if matched:
                matched_elem = link_elem
                code = matched.group(1)
                break

        return code, matched_elem

