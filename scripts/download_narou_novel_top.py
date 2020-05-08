import os
import requests

if __name__ == '__main__':
    ncode = 'n5378gc'
    url = 'https://ncode.syosetu.com/{}/'.format(ncode)
    print(url)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
    res = requests.get(url, headers=headers)
    #print(res.content)
    #print(res.text)

    data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    save_path = '{}/narou_novel_top_{}.html'.format(data_path, ncode)

    with open(save_path, 'wb') as f:
        f.write(res.content)

