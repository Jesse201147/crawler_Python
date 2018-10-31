# 这些是我在学习Python爬虫时的一部分练手项目:
  
Twitter_crawl.py(登录Twitter,搜索抓取搜索到相关内容的作者详细信息):   
   
  1 使用selenium 登录Twitter 获取cookies   
  2 使用cookies获取搜索页面,从中解析出搜索到twitter的position参数  
  3 使用position得到搜索结果,从中解析出twitter作者的key,与下一个posion  
  4 循环3 直至爬到想要的数量    
  5 使用作者的key 爬取作者主页,从中解析作者详细信息  
  
  
ZhiHu_issue.py(爬取知乎issue:432035497 所有回答):  
  
  1 GET 此问题下的网页源码  
  2 从此问题的网页源码中解析第一个回答的URL  
  3 从第一个回答URL中提取作者id,name,回答文本 存储格式{'name': '', 'id': '', 'content':''}  
    并返回判断这是不是最后一个回答的状态参数 is_end 与 下一页URL   
  4 循环3 直至 在爬到指定数量回答 或 爬完所有回答  
  5 保存数据到MongoDB 
 
 XiCi.py(从西刺代理抓取300个可用且存活时间超过24h的 IP):  
    
  1 从西刺代理爬取国内高匿IP第一页,  
  2 解析ip信息,存储存活时间超过24小时的IP 存储格式{ip': '', 'port': '', 'type': ''}  
  3 判断第一页中IP是否可用(使用代理访问百度),去除不可用IP  
  4 重复123 直至IP总数超过爬取数量,存储至MongoDB  
   
 dota2_match_record.py(从STEAM官方API爬取ZSMJ最近25场比赛的战绩):    
    
  1 使用ZSMJ的DOTA2_id 从官方API抓取并解析出最近25场比赛的match_id  
  2 使用match_id从官方AIP查询比赛详情,解析出 heroid KDA GPM XPM   
  3 将比赛数据存入MongoDB  
   
