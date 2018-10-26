# crawler_Python
这些是我在学习Python爬虫时的一部分练手项目:

ZhiHu_issue.py(爬取知乎issue:432035497 所有回答):/n
  1 GET 此问题下的网页源码
  2 从此问题的网页源码中解析第一个回答的URL
  3 从第一个回答URL中提取作者id,name,回答文本 存储格式{'name': '', 'id': '', 'content':''}
    并返回判断这是不是最后一个回答的状态参数 is_end 与 下一页URL 
  4 循环3 直至 在爬到指定数量回答 或 爬完所有回答
  5 保存数据到mongdb
 
 
