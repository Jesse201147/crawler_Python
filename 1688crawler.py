#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jesse.Tang

from selenium import webdriver
from lxml.html import etree
import pymongo
import time

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["1688商品信息"]
mycol = mydb["智能手环"]
driver = webdriver.Firefox()


def open_page():
    # selenium 模拟打开搜索页面，如果弹出新用户窗口将其关闭
    url = f'https://s.1688.com/selloffer/offer_search.htm?keywords=%D6%C7%C4%DC%CA%D6%BB%B7&beginPage=1'
    driver.get(url)
    try:
        driver.find_element_by_css_selector('em.s-overlay-close-l').click()
    except:
        pass


def get_page_source():
    # 将页面滑动至底端，休眠3s等所有商品信息加载完成后点击下一页按钮 （休眠时间视网速情况设定）
    driver.execute_script('window.scrollTo(0, 99999)')
    time.sleep(3)
    page = driver.page_source
    try:
        driver.find_element_by_css_selector('a.fui-next').click()
        return page
    except:
        print('no next page')


def parse(page):
    info = []
    tree = etree.HTML(page)
    items = tree.cssselect('ul#sm-offer-list>li')
    # 将页面中的商品详情标签 <li> 取出

    css_dict = {
        'title': ('.imgofferresult-mainBlock>.sm-offer-photo>a', 'title'),
        'url': ('.imgofferresult-mainBlock>.sm-offer-photo>a', 'href'),
        'img': ('.imgofferresult-mainBlock>.sm-offer-photo>a>img[src^=https]', 'src'),
        'price': ('.imgofferresult-mainBlock>div>span[class*=price]', 'title'),
        'tradeBt': ('.imgofferresult-mainBlock>div>span[class*=tradeBt]', 'title'),
        'company_name': ('.imgofferresult-mainBlock>div[class*=companyinfo]>a[data-spm=of2]', 'title'),
        'company_url': ('.imgofferresult-mainBlock>div[class*=companyinfo]>a[data-spm=of2]', 'href')
    }
    # 将 <li> 标签中商品信息对应的cssselector与信息存储位置以字典形式整合

    for i in items:
        item_info = {}
        for j in css_dict.keys():
            try:
                item_info[j] = i.cssselect(css_dict[j][0])[0].get(css_dict[j][1])
            except:
                item_info[j] = ''
        if item_info['title'] and item_info['url']:
            info.append(item_info)
    # 对 items 中每一个<li>标签 遍历 css_dict 中的cssselector获得此标签中商品信息，若信息有效，存入列表info

    return info


def main(page=6):
    info = []
    open_page()
    for i in range(page):
        info += parse(get_page_source())
    mycol.insert_many(info)
    return info


if __name__ == '__main__':
    info = main()
    print(len(info))
    c = 0
    for i in info:
        c += 1
        print(c)
        for j in i.keys():
            print(f'{j}=>{i[j]}')
