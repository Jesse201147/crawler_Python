#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/5 13:41
# @Author  : Jesse.T
import requests
from bs4 import BeautifulSoup



def get_Html(url):
    try:
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=30, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''


def get_info(HTML, info):
    soup = BeautifulSoup(HTML, 'html.parser')
    for li in soup.find('div', 'job-list').descendants:
        if li.name == 'li':
            tap_div = li('div', "job-title")
            job = tap_div[0].string
            # 职位
            tap_span = li('span', 'red')
            salary = tap_span[0].string
            # 工资
            request = li('p')
            year = request[0].contents[2]
            # 工作经验需求
            edu = request[0].contents[4]
            # 教育背景需求
            company = request[1].contents[0]
            # 公司类型
            tap_a = li('a')
            company_name = tap_a[1].string
            # 公司名称
            info.append([job, salary, year, edu, company, company_name])


def save_info(info):
    with open('work.txt', 'wt')as f:
        tplt = '{0:{6}<20}{1:<5}{2:{6}<5}{3:{6}<5}{4:{6}<5}{5:{6}<5}'
        f.write(tplt.format('职位', '月薪', '工作年限', '学历', '公司类型', '公司名称', chr(12288)) + '\n')
        for i in info:
            line = tplt.format(i[0], i[1], i[2], i[3], i[4], i[5], chr(12288))
            f.write(line + '\n')


def main():
    u = 'https://search.bilibili.com/all?keyword='
    k= input('请输入您要搜索的关键词（多个关键词以逗号隔开):')
    keyword = '%20'.join(k.split(','))
    o='o'
    order_list={'a':'totalrank','b':'click','c':'pubdate','d':'dm','e':'stow'}
    while not o in ('a','b', 'c','d', 'A', 'B', 'C', 'D'):
        o=input('请输入搜索结果排序方式:\n依综合排序请输入\'a\'\n依点击量排序请输入\'b\'\n依发布时间排序请输入\'c\'\n依收藏量排序请输入\'d\'\n')
    else:
        o=o.lower()
        order=order_list.get(o)
    num='a'
    while not isinstance(num,int):
        num=eval(input('请输入下载视频数量:'))
        p=num//20+1
    info = []
    for i in range(1, p + 1):
        print('正在爬取第{:d}页...'.format(i))
        url = u + keyword + '&from_source=banner_search&order=' + order + '&duration=0&tids_1=0&page=' + str(i)
        HTML = get_Html(url)
        get_info(HTML, info)

    save_info(info)
    print('爬取完成，结果请见程序根目录work.txt, 感谢使用！')


main()