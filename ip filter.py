import requests
from multiprocessing import Pool
import os


# 将从http://www.gatherproxy.com/ 获取的txt格式 ip 筛选可用ip


def get_ip(file):
    with open(file, 'r') as f:
        while True:
            lines = data = f.read().splitlines()
            return lines


def ip_check(server):
    # 使用代理访问百度,检查IP是否可用,
    print(f'process {os.getpid()} is running for {server}')

    proxies = {'http': 'http://' + server,
               'https': 'https://' + server
               }
    try:
        r = requests.get('https://www.baidu.com', proxies=proxies, timeout=3)
        r.raise_for_status()
        print(f'process {os.getpid()} checked {server} is ok ')
        return server
    except:
        print(f'process {os.getpid()} checked {server} is  nok ')

if __name__ == '__main__':
    file = 'ip.txt'
    ip_list = get_ip(file)
    p = Pool()
    ip = p.map(ip_check, ip_list[:300])
    p.close()
    p.join()
    ip = [i for i in ip if i]
    with open('ip_checked.txt', 'w+') as f:
        f.write('\n'.join(ip))
