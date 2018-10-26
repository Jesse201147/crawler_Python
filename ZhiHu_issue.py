import requests
import re
import pymongo
from functools import reduce


def get_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.zhihu.com",
        "Upgrade-Insecure-Requests": "1",
    }
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print(f'fail to get page {url}')


def parse_first_page(page):
    # 从问题初始URL拿到回答的第一个URL
    pattern = re.compile(r'https://www.zhihu.com/api/v4/questions/46493260/answers\?.*?&quot;')
    url = pattern.findall(page)[0]
    return url


def parse_ans(page_ans):
    # 拿到回答中作者id,name,回答文本 存储格式{'name': '', 'id': '', 'content':''}
    # 返回 is_end 与 next 用于爬取下一页回答

    for i in page_ans['data']:
        ans = {}
        d = i['content']
        pattern = re.compile(r'<p>(.*?)</p>', re.S)
        content = pattern.findall(d)
        if len(content) != 0:
            t = [i for i in content if i not in ('<br>', '-', '')]
            try:
                content = reduce(lambda x, y: x + y, t)
            except:
                pass
            ans['name'] = i['author']['name']
            ans['id'] = i['author']['id']
            ans['content'] = content
            if ans:
                answers.append(ans)
    return page_ans['paging']['is_end'], page_ans['paging']['next']

def save_to_mongo(issue_num):
    # MongoDB数据库，ZhiHu'MeiTuan' 与COL 'issue:{issue_num}'
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["ZhiHu"]
    mycol = mydb[f"issue:{issue_num}"]

    save_status=mycol.insert_many(answers)
    return save_status


def main(issue_num=46493260):
    global true, false, answers
    true = True
    false = False
    answers = []
    is_end = False

    start_url = f'https://www.zhihu.com/question/{issue_num}'
    page = get_page(start_url)
    # 构建并爬取问题URL

    next = parse_first_page(page)
    # 解析issue页面,返回问题下第一个回答URL

    while not is_end:
        print(f"正在爬取第{len(answers)+1}个回答")
        # 打印文本进度条

        page_ans = eval(get_page(next))
        is_end, next = parse_ans(page_ans)
        if len(answers) >= 30:
            is_end = True
        # 在爬到30个回答 或者回答爬完了时循环终止
    save_status=save_to_mongo(issue_num)


if __name__ == '__main__':
    main()
    print(answers)
    print(len(answers))
