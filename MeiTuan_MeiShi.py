import requests
import re
import pymongo

# MongoDB数据库，新建DB'MeiTuan' 与COL 'MeiShi'
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["MeiTuan"]
mycol = mydb["MeiShi"]

# 爬取源码中存在true ,false 会使程序报错,故提前赋值
true = True
false = False

# 爬取美团美食信息前3页并使用正则进行解析
data = []
kv = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://gz.meituan.com/'
}
for i in range(3):
    url = f'https://gz.meituan.com/meishi/pn{i+1}/'
    r = requests.get(url, params=kv, timeout=30)
    pattern = re.compile(r'"poiLists":(.*?),"comHeader"')
    info = eval(re.findall(pattern, r.text)[0]).get('poiInfos')
    data += info

# 将美食信息存入MongoDB
x = mycol.insert_many(data)

if __name__ == '__main__':
    print(x)
    print(len(data))
