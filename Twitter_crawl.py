#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from selenium import webdriver
import time


email = '962080565@qq.com'
password = '1111111l'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}
proxies = {
    "http": "socks5://127.0.0.1:1080",
    "https": "socks5://127.0.0.1:1080"
}
session = requests.Session()


def login():
    # 使用selenium 登录返回cookies
    driver = webdriver.Firefox()
    driver.get("https://twitter.com/login")
    driver.find_element_by_css_selector('div.clearfix.field > input[name="session[username_or_email]"]').send_keys(
        email)
    driver.find_element_by_css_selector('div.clearfix.field > input[name="session[password]"]').send_keys(password)
    driver.find_element_by_css_selector('.EdgeButtom--medium').click()
    cookies = driver.get_cookies()
    driver.close()
    # cookies=[{'name': 'personalization_id', 'value': '"v1_jJOcwroHKQkTDDh2a73YCg=="', 'path': '/', 'domain': '.twitter.com', 'secure': False, 'httpOnly': False, 'expiry': 1603970312}, {'name': 'guest_id', 'value': 'v1%3A154089831274152553', 'path': '/', 'domain': '.twitter.com', 'secure': False, 'httpOnly': False, 'expiry': 1603970312}, {'name': 'ct0', 'value': 'fc9d4f11e4cdfc63fe49bd83ac2ced95', 'path': '/', 'domain': '.twitter.com', 'secure': True, 'httpOnly': False, 'expiry': 1540919912}, {'name': '_ga', 'value': 'GA1.2.1511951414.1540898320', 'path': '/', 'domain': '.twitter.com', 'secure': False, 'httpOnly': False, 'expiry': 1603970319}, {'name': '_gid', 'value': 'GA1.2.1397764081.1540898320', 'path': '/', 'domain': '.twitter.com', 'secure': False, 'httpOnly': False, 'expiry': 1540984719}, {'name': '_gat', 'value': '1', 'path': '/', 'domain': '.twitter.com', 'secure': False, 'httpOnly': False, 'expiry': 1540898379}, {'name': 'dnt', 'value': '1', 'path': '/', 'domain': '.twitter.com', 'secure': False, 'httpOnly': False, 'expiry': 1856258320}, {'name': 'ads_prefs', 'value': '"HBESAAA="', 'path': '/', 'domain': '.twitter.com', 'secure': False, 'httpOnly': False, 'expiry': 1856258320}, {'name': 'kdt', 'value': '6xoKZvDCHFSX36fv6TboSqTytpEICzAMXGaW4nX5', 'path': '/', 'domain': '.twitter.com', 'secure': True, 'httpOnly': True, 'expiry': 1588159120}, {'name': 'remember_checked_on', 'value': '1', 'path': '/', 'domain': '.twitter.com', 'secure': False, 'httpOnly': False, 'expiry': 1856258320}, {'name': '_twitter_sess', 'value': 'BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCdSssRmAToMY3NyZl9p%250AZCIlNjA2YzcwYWY1Y2YxNWYyMWJiN2Q1NzYxMzljMWQ4ZmY6B2lkIiUyMzY3%250AODI2NTBmZTY4Yzk0OGU0M2NhMmZiMjhkMTI5ZjoJdXNlcmwrCQAAVf%252B%252BrAEO--85a2fcc2357bbe6c241bb9adcef13432c2c8885c', 'path': '/', 'domain': '.twitter.com', 'secure': True, 'httpOnly': True}, {'name': 'twid', 'value': '"u=1009277727835226112"', 'path': '/', 'domain': '.twitter.com', 'secure': True, 'httpOnly': False, 'expiry': 1856258320}, {'name': 'auth_token', 'value': '5c6e11c5627968b33223c990a3c4e392f19f5318', 'path': '/', 'domain': '.twitter.com', 'secure': True, 'httpOnly': True, 'expiry': 1856258320}, {'name': 'csrf_same_site_set', 'value': '1', 'path': '/', 'domain': '.twitter.com', 'secure': True, 'httpOnly': True, 'expiry': 1572347920}, {'name': 'lang', 'value': 'en', 'path': '/', 'domain': 'twitter.com', 'secure': False, 'httpOnly': False}, {'name': 'csrf_same_site', 'value': '1', 'path': '/', 'domain': '.twitter.com', 'secure': True, 'httpOnly': True, 'expiry': 1572434320}]
    print(cookies)
    return cookies


def get_index_page(kw):
    url = f'https://twitter.com/search?q={kw}&src=typd'
    r = session.get('https://twitter.com/login', timeout=5, headers=headers, proxies=proxies)
    print(r)
    print(r.text)


def main(kw='Python'):
    session.cookies = login()
    index_page = get_index_page(kw)


if __name__ == '__main__':
    stime = time.time()
    main()
    print(f"time used : {time.time()-stime}")
