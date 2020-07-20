from socket import *
from select import select
HOST="0.0.0.0"
PORT=12345
ADDR=(HOST,PORT)
tcp_socket=socket()
#设置为非阻塞
tcp_socket.setblocking(False)
tcp_socket.bind(ADDR)
tcp_socket.listen(5)
rlist=[tcp_socket]   #初始监控对象
wlist=[]
xlist=[]
#循环监控
while True:
    #对关注的IO进行监控
    rs,ws,xs=select(rlist,wlist,xlist)   #select阻塞监控
    #对返回值rs分情况讨论，监听套接字，客户端连接套接字
    for r in rs:
        if r is tcp_socket:
            connfd,addr=r.accept()
            connfd.setblocking(False)
            print("Connect from",addr)
            rlist.append(connfd)
        else:
            data=r.recv(1024)
#这里的r即connfd可以循环接收，是因为接收第一次以后又回到大循环，
# 而connfd处于被监控状态，只要有客户端发消息，就会响应，然后又可以执行
            if not data:   #客户端退出，服务端会收到空
                r.close()
                rlist.remove(r)
                continue   #继续执行循环，处理其他r
            print(data.decode())
            # r.send(b'ok')
            wlist.append(r)  #放入写列表

    for w in wlist:
        w.send(b'ok')  #发送消息
        wlist.remove(w)  #如果不移除会不断的写


