"""
author: Cassiel
email: 2549171281@qq.com
time: 2020-7-14
env: Python3.6
socket and Process exercise
"""
'''
【1】 有人进入聊天室需要输入姓名，姓名不能重复
【2】 有人进入聊天室时，其他人会收到通知：xxx 进入了聊天室
【3】 一个人发消息，其他人会收到：xxx ： xxxxxxxxxxx
【4】 有人退出聊天室，则其他人也会收到通知:xxx退出了聊天室
【5】 扩展功能：服务器可以向所有用户发送公告:管理员消息： xxxxxxxxx
'''
from socket import *
from multiprocessing import Process

# 服务器使用地址   有特殊含义的大写
HOST = "0.0.0.0"
PORT = 8000
ADDR = (HOST, PORT)

# 存储用户 {name:address ...}
user = {}


# 处理进入聊天室
def do_login(sock, name, address):
    if name in user or "管理" in name:
        sock.sendto(b"FAIL", address)
        return
    else:
        sock.sendto(b"OK", address)
        # 通知其他人
        msg = "欢迎 %s 进入聊天室" % name
        for i in user:
            sock.sendto(msg.encode(), user[i])     #通知其他人
        # 存储用户
        user[name] = address



# 处理聊天
def do_chat(sock, name, content):
    msg = "%s : %s" % (name, content)
    for i in user:
        # 刨除本人
        if i != name:
            sock.sendto(msg.encode(), user[i])


# 处理退出
def do_exit(sock, name):
    del user[name]  # 移除此人    先删再发消息，可以少做一次排除本人的判断
    # 通知其他人
    msg = "%s 退出聊天室" % name
    for i in user:
        sock.sendto(msg.encode(), user[i])


# 子进程执行
def handle(sock):
    # 循环接收来自客户端请求
    while True:
        # 接收请求 (所有用户的所有请求)
        data, addr = sock.recvfrom(1024)
        tmp = data.decode().split(' ', 2)  # 对请求内容进行解析   “你好 世界”也不会报错。
#s = "你好 世界 啊啊啊  aaa"  # ['你好', '世界', '啊啊啊  aaa'],只以两个空格进行划分，而不是划分为两部分
#print(s.split(" ", 2))
        # 根据请求调用不同该函数处理
        if tmp[0] == 'L':
            # tmp ==> [L,name]
            do_login(sock, tmp[1], addr)  # 处理用户进入聊天具体事件
        elif tmp[0] == 'C':
            # tmp==>[C,name,xxxxxxx]
            do_chat(sock, tmp[1], tmp[2])
        elif tmp[0] == 'E':
            # tmp==>[E,name]
            do_exit(sock, tmp[1])


# 启动函数
def main():
    sock = socket(AF_INET, SOCK_DGRAM)  # UDP套接字
    sock.bind(ADDR)

    # 创建一个新的进程，用于分担功能
    p = Process(target=handle, args=(sock,))
    p.daemon = True
    p.start()
    # 父进程发送管理员消息
    while True:
        content = input("管理员消息：")
        # 服务端整个退出
        if content == "quit":
            break
        data = "C 管理员消息 " + content
        sock.sendto(data.encode(), ADDR)  # 父进程发送给子进程
#此处注意不能直接使用user字典进行遍历发送消息给所有客户端，因为父子进程的数据相互独立，
# user在子进程有值，但父进程字典依然为空

if __name__ == '__main__':
    main()
