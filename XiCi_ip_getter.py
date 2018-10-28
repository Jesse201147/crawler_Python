import requests
import pymongo
from lxml.html import etree
import time

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Hosts': 'hm.baidu.com',
    'Referer': 'http://www.xicidaili.com/nn',
    'Connection': 'keep-alive'
}
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ip"]
mycol = mydb["ip"]


def get_page(p):
    # 从西刺官网爬到国内高匿IP页面
    url = f'http://www.xicidaili.com/nn/{p+1}'
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        return r.text
    except:
        pass


def parse(page):
    # 从页面内解析出{ip': '', 'port': '', 'type': ''}并舍弃存活时间小于1天的IP 结果以列表形式返回
    ip_list = []
    ip = {}
    if page == None:
        return ''
    tree = etree.HTML(page)
    info = tree.cssselect('#ip_list tr')[1:]
    for i in info:
        p = i.cssselect('td')
        time = p[8].text.replace('分钟', '').replace('小时', '*60').replace('天', '*24*60')
        if eval(time) > 1 * 24 * 60:
            ip['ip'] = p[1].text
            ip['port'] = p[2].text
            ip['type'] = p[5].text
            ip_list.append(ip)
    return ip_list


def ip_check(ip):
    # 使用代理访问百度,检查IP是否可用,剔除其中不可用部分
    for i in ip:
        server = i['ip'] + ':' + i['port']
        proxies = {'http': 'http://' + server,
                   'https': 'https://' + server
                   }
        try:
            r = requests.get('https://www.baidu.com', proxies=proxies, timeout=1)
            if r.status_code != 200:
                i = {}
        except:
            i = {}
    return [i for i in ip if i != {}]


def main(num=30):
    # 持续抓取页面,直至抓取IP有效条数超过num,存入MongoDB
    stime = time.time()
    ip = []
    for i in range(99999):
        print(f'collecting page {i+1},time used:{time.time()-stime}sec')
        page = get_page(i)
        ip_onepage = parse(page)
        ip += ip_check(ip_onepage)
        time.sleep(1)
        if len(ip) > num:
            break
    mycol.insert_many(ip[:num])
    print(f'Ip collector finished!\ntime used :{time.time()-stime}sec')


if __name__ == '__main__':
    main()
