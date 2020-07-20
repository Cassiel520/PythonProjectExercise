"""
chat client
发送请求，得到结果
"""
from socket import *
from multiprocessing import Process
import sys
#124.70.156.125   服务器公网
# ADDR = ("124.70.156.125", 8000)
# 服务端地址
ADDR = ("127.0.0.1", 8000)

# 请求进入聊天室 OK FAIL
def login(sock):
    while True:
        name = input("Name:")
        msg = "L " + name  # 根据通信协议整理发送信息
        sock.sendto(msg.encode(), ADDR)  # 发送请求
        result, addr = sock.recvfrom(128)  # 等待回复
        if result.decode() == 'OK':
            print("您已进入聊天室")
            return name
        else:
            print("你的名字太受欢迎了，换一个吧")

# 接收消息
def recv_msg(sock):
    while True:
        data, addr = sock.recvfrom(2048)
        print("\n" + data.decode() + "\n我：", end="")


# 发送消息
def send_msg(sock, name):
    while True:
        try:
            msg = input("我:")
        except KeyboardInterrupt:  #捕获这种异常以后,客户端不会退出，执行完下面的msg才退出
            msg = "exit"
        if msg == 'exit':
            data = "E " + name
            sock.sendto(data.encode(), ADDR)
            sys.exit("您已退出聊天室")
        data = "C %s %s" % (name, msg)
        sock.sendto(data.encode(), ADDR)


def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    # sock.bind(('0.0.0.0',55555))
    # 远程连接，udp客户端最好绑定地址，因为客户端长时间不发消息，地址将会变化，会出现丢包等情况
    name = login(sock)  # 进入聊天室

    # 为聊天创建子进程
    p = Process(target=recv_msg, args=(sock,))
    p.daemon = True  # 父进程退出子进程也退出
    p.start()
    send_msg(sock, name)


if __name__ == '__main__':
    main()
