# 这些是我在学习Python爬虫时的一部分练手项目:
    
 **Twitter_crawl.py(登录Twitter,搜索抓取搜索到相关内容的作者详细信息):**   
   
  1 使用selenium 登录Twitter 获取cookies   
  2 使用cookies获取搜索页面,从中解析出搜索到twitter的position参数  
  3 使用position得到搜索结果,从中解析出twitter作者的key,与下一个posion  
  4 循环3 直至爬到想要的数量    
  5 使用作者的key 爬取作者主页,从中解析作者详细信息  
  
  
 **ZhiHu_issue.py(爬取知乎issue:432035497 所有回答):**  
  
  1 GET 此问题下的网页源码  
  2 从此问题的网页源码中解析第一个回答的URL  
  3 从第一个回答URL中提取作者id,name,回答文本 存储格式{'name': '', 'id': '', 'content':''}  
    并返回判断这是不是最后一个回答的状态参数 is_end 与 下一页URL   
  4 循环3 直至 在爬到指定数量回答 或 爬完所有回答  
  5 保存数据到MongoDB 
  
   
   **1688crawler.py（使用 selenium 从 阿里巴巴 爬取商品信息 存入MongoDB):**  
    
  1 从使用selenium打开1688页面获取源码 
  2 使用 CSS选择器 从源码中解析商品信息
  3 判断商品信息是否有效，将有效信息存储   
  4 使用selenium进行翻页
  5 重复2 3 直至爬取完成
 
   **ip_filter.py(将从http://www.gatherproxy.com/ 获取的txt格式ip筛选可用ip并保存):**  
    
  1 从http://www.gatherproxy.com/ 下载txt格式IP文件  
  2 从文件读取IP  
  3 使用读取的IP 作代理访问百度 验证IP是否有效   
  4 验证过程使用多线程 multiprocessing 进行提速
  5 将验证完成的IP保存
   
  **XiCi.py(从西刺代理抓取300个可用且存活时间超过24h的 IP):**  
    
  1 从西刺代理爬取国内高匿IP第一页,  
  2 解析ip信息,存储存活时间超过24小时的IP 存储格式{ip': '', 'port': '', 'type': ''}  
  3 判断第一页中IP是否可用(使用代理访问百度),去除不可用IP  
  4 重复123 直至IP总数超过爬取数量,存储至MongoDB  
   
  **dota2_match_record.py(从STEAM官方API爬取ZSMJ最近25场比赛的战绩):**    
    
  1 使用ZSMJ的DOTA2_id 从官方API抓取并解析出最近25场比赛的match_id  
  2 使用match_id从官方AIP查询比赛详情,解析出 heroid KDA GPM XPM   
  3 将比赛数据存入MongoDB  
   
