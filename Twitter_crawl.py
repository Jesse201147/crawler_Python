#!/usr/bin/python
import requests
import time
import re
from selenium import webdriver

email = '962080565@qq.com'
password = '1111111l'
mykey = '/ogcS2b43dNG5NS0'
true = True
false = False
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'authority': 'twitter.com',
    'referer': f'https://twitter.com{mykey}'
}

proxies = {
    "http": "socks5://127.0.0.1:1080",
    "https": "socks5://127.0.0.1:1080"
}
session = requests.Session()
session.headers = headers
session.proxies=proxies

def login():
    # 使用selenium 登录返回cookies
    jar = requests.cookies.RequestsCookieJar()
    driver = webdriver.Firefox()
    driver.get("https://twitter.com/login")
    driver.find_element_by_css_selector('div.clearfix.field > input[name="session[username_or_email]"]').send_keys(
        email)
    driver.find_element_by_css_selector('div.clearfix.field > input[name="session[password]"]').send_keys(password)
    driver.find_element_by_css_selector('.EdgeButtom--medium').click()
    cookies = driver.get_cookies()
    driver.close()
    for i in cookies:
        jar.set(i['name'], i['value'], path=i['path'], domain=i['domain'], secure=i['secure'])
    session.cookies = jar
    return jar


def get_first_p(kw):
    # 获取搜索页面源码，解析并返回其中的position
    try:
        r = session.get('https://twitter.com/search?vertical=default&q=%E4%BB%8A%E5%A4%A9&l=zh&src=typd')
        r.raise_for_status()
        pattern = re.compile(r'data-max-position="(.*?)"', re.S)
        position = pattern.findall(r.text)
        return position
    except:
        print('fail to get first position')


def get_news(position, kw):
    # 使用position 获取对应的页面源码
    url = f'https://twitter.com/i/search/timeline?vertical=news&q={kw}&l=en&src=typd&composed_count=0&include_available_' \
          f'features=1&include_entities=1&include_new_items_bar=true&interval=30000&latent_count=0&min_position={position}'
    try:
        r = session.get(url)
        r.raise_for_status()
        return r.text
    except:
        print(f'fail to get position {position}')


def parse_text(text):
    # 从position对应的页面源码中解析用户key
    html = eval(text)['items_html']
    position = eval(text)['max_position']
    pattern = re.compile(
        r' class=\"account-group js-account-group js-action-profile js-user-profile-link js-nav\" href=\"\\(.*?)"')
    user = pattern.findall(html)
    return user, position


def get_user_info(user_keys):
    # 使用用户key从用户主页获取用户信息
    users = []
    for i in user_keys:
        user_info = {}
        user_info['user_key'] = i
        url = 'https://twitter.com' + i
        r = session.get(url)

        pattern_name = re.compile(r' class="ProfileHeaderCard-nameLink u-textInheritColor js-nav">(.*?)<')
        name = pattern_name.findall(r.text)
        user_info['name'] = name[0] if name else ''

        pattern_description = re.compile(r'<p class="ProfileHeaderCard-bio u-dir" dir="ltr">(.*?)<')
        description = pattern_description.findall(r.text)
        user_info['description'] = description[0] if description else ''

        pattern_location = re.compile(r' <span class="ProfileHeaderCard-locationText u-dir" dir="ltr">(.*?)<')
        location = pattern_location.findall(r.text)
        user_info['location'] = location[0] if location else ''

        pattern_join_date = re.compile(
            r' <span class="ProfileHeaderCard-joinDateText js-tooltip u-dir" dir="ltr" title="11:22 AM - 29 Oct 2018">Joined(.*?)</span>')
        join_date = pattern_join_date.findall(r.text)
        user_info['join_date'] = join_date[0] if join_date else ''
        users.append(user_info)
    return users


def main(kw='今天', num=10):
    # kw : 要搜索的内容 num ：要搜索的用户数量
    user_keys = []
    login()
    print(session.cookies)
    position = get_first_p(kw)
    while True:
        user, position = parse_text(get_news(position, kw))
        user_keys += user
        user_keys = list(set(user_keys))
        if len(user_keys) >= num:
            break
    user_info = get_user_info(user_keys)
    return user_info[:num]


if __name__ == '__main__':
    stime = time.time()
    user_info = main()
    print(user_info)
    print(len(user_info))
    print(f"time used : {time.time()-stime}")
