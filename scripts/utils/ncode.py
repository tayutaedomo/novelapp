import datetime
import re


class SyosetuSearch:
    @classmethod
    def get_ncode(cls, driver, title):
        #base_url = 'https://yomou.syosetu.com/search.php?word={}&notword=&genre=&type=&mintime=&maxtime=&minlen=&maxlen=&min_globalpoint=&max_globalpoint=&minlastup=&maxlastup=&minfirstup=&maxfirstup=&order=new'
        base_url = 'https://yomou.syosetu.com/search.php?word={}order=new'
        url = base_url.format(title)

        print(datetime.datetime.now().isoformat(), 'GET:', url)

        driver.get(url)

        matched_elem = None
        code = None
        link = driver.find_element_by_link_text('小説情報')
        pass


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
            return code, None

        for link_elem in link_list[:5]:
            href = link_elem.get_attribute('href')
            matched = re.match(r'^https:\/\/ncode\.syosetu\.com\/(.+)\/$', href)

            if matched:
                matched_elem = link_elem
                code = matched.group(1)
                break

        return code, matched_elem

