import requests
from lxml.html import etree
import pymongo

#MongoDB数据库，新建DB与COL
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["weibo"]
mycol = mydb["weibo_hot"]


#爬取微博热搜５０条，存储为字典列表
url='https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6&display=0&retcode=6102'
r=requests.get(url)
tree=etree.HTML(r.text)
tag=tree.cssselect('tr>td>a')[1:]
num=tree.cssselect('tr>td>span')
a=[{"tag":tag[i].text,'num':num[i].text} for i in range(len(tag)) ]


#将爬取到的数据存入数据库
x=mycol.insert_many(a)


#调试过程与数据存储结果
if __name__=='__main__':
    print([tag.text for tag in tag])
    print(len([tag.text for tag in tag]))
    print([tag.text for tag in num])
    print(len([tag.text for tag in num]))
    print(a)
    print(x)
