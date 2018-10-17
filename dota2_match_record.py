#!/usr/bin/python
import requests
import re
import time
import pymongo

#从STEAM官方API爬取ZSMJ最近25场比赛的战绩,因steam官方服务器链接较慢,若爬取失败请重试

def get_page(account_id):
    #使用account_id爬取该ID最新的100场比赛信息

    url='https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v001/'
    params = {'key': 'DBC7484E07E8358AC799DD0A1D3BBC17',
              'account_id': account_id,
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
              }
    try:
        r = requests.get(url,params=params,timeout=50)
        r.raise_for_status()

        r.encoding = r.apparent_encoding
        return r.text
    except:
        return print(f'cannot get info from {url}/\n please improve your network and try again')

def parse_matchid(page):
    #从100场比赛信息中提取matchid

    pattern=re.compile(r'"match_id":(\d+),')
    return re.findall(pattern,page)

def get_matchinfo(matchid):
    #使用100场matchid前25场的matchid 查询这25场比赛的详情

    matchinfo=[]
    url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/'
    count=0
    print('正在爬取比赛详情')
    for i in matchid:
        count+=1
        print('['+"-"*count+'=>'+"+"*(25-count)+']'+f'{4*(count-1)}'+'%')
        params = {'key': 'DBC7484E07E8358AC799DD0A1D3BBC17',
                  'match_id': i,
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                '(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
                  }
        try:
            r = requests.get(url, params=params, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            matchinfo.append(r.text.replace('\n', '').replace('\r', ''))
        except:
            pass
    return matchinfo

def parse_matchinfo(matchinfo):
    #在25场比赛详情中提取出 heroid KDA GPM XPM

    data=[]
    for i in matchinfo:
        players=eval(i).get('result','').get('players','')
        for j in players:
            if j.get('account_id','')==113705693:
                data.append({
                            'hero_id':j.get('hero_id',''),'kills':j.get('kills',''),'deaths':j.get('deaths',''),
                            'assists':j.get('assists',''),'GPM':j.get('gold_per_min',''),'XPM':j.get('xp_per_min','')
                            })
                break
    return data


def save_info(data):
    #将查得数据存入MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["dota2"]
    mycol = mydb["game_record"]
    x=mycol.insert_many(data)
    return x

    pass
def main ():
    global true, false,account_id
    true = True
    false = False
    account_id = 113705693
    print(f'开始爬取id={account_id}的比赛数据')
    page=get_page(account_id)
    if not page:
        return
    matchid=parse_matchid(page)[:25]
    print('已得到最新25场比赛ID')
    matchinfo=get_matchinfo(matchid)
    data=parse_matchinfo(matchinfo)
    x=save_info(data)
    if x:

        print('爬取成功已存入数据库')

if __name__=='__main__':
    starttime=time.time()
    main()
    usetime=time.time()-starttime
    print(f'-' * 100 + f'\n运行耗时{usetime}s')