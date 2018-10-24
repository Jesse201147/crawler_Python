import requests
import re


def get_html(url):
    # get page from url
    try:
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=30, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print(f'fail to get page from {url}')


def get_info(html):
    # collect info from the page
    pattern = re.compile(r' <dd>.*?board-index.*?">(\d+)</i>.*?'
                         r'title="(.*?)".*?data-src="(.*?)".*?'
                         r'class="star">(.*?)</p>.*?releasetime">(.*?)</p>', re.S)
    info = re.findall(pattern, html)
    return info


def save_info(info,offset):
    # save the information as 'movie.txt'
    with open('movie.txt', 'a')as f:
        for lines in info:
            lines = f'Ranking：{lines[0]}；title:{lines[1]};poster:{lines[2]} ;' \
                    f'actor:{lines[3].strip()[3:]};time:{lines[4][5:]}'
            f.writelines(lines + '\n')
        f.close()


def main(offset):
    # offset is the page number
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_html(url)
    info = get_info(html)
    save_info(info,offset)


if __name__=='__main__':
    # initialize a new file and run main
    with open ('movie.txt', 'w')as f:
        f.close()
    for i in range (10):
        main(i*10)
