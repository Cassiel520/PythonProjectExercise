'''
web 服务程序实现
1.主要功能
【1】 接收客户端（浏览器）请求
【2】 解析客户端发送的请求
【3】 根据请求组织数据内容
【4】 将数据内容形成http响应格式返回给浏览器
2.特点 ：
【1】 采用IO并发，可以满足多个客户端同时发起请求情况
【2】 通过类接口形式进行功能封装
【3】 做基本的请求解析，根据具体请求返回具体内容，同时处理客户端的非网页请求行为
'''
from socket import *
from select import *
import re
class WebServer:
    def __init__(self, host='0.0.0.0', port=8888, html=''):
        self.host = host
        self.port = port
        self.html = html
        self.create_socket()
        self.bind()
        # 做IO多路复用并发模型准备
        self.__rlist = []
        self.__wlist = []
        self.__xlist = []

    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def bind(self):
        self.address = ((self.host, self.port))
        self.sock.bind(self.address)

    def start(self):
        self.sock.listen(5)
        self.__rlist.append(self.sock)
        print("Listen the port %d"%self.port)
        while True:
            rs, ws, xs = select(self.__rlist, self.__wlist, self.__xlist)
            for r in rs:
                if r is self.sock:
                    connfd, addr = r.accept()
                    connfd.setblocking(False)
                    # connfd不能变成属性，相当于类中的全局变量，所有都可以用
                    self.__rlist.append(connfd)
                else:
                    try:
                       self.handle(r)  #处理有些特殊字符不能转换为字节串的异常
                    except:
                        self.__rlist.remove(r)
                        r.close()

    def handle(self, connfd):
        data = connfd.recv(4096 * 10)
        pattern = "[A-Z]+\s+(?P<info>/\S*)"
        request = re.match(pattern, data.decode())
# match对象 或None,不能直接用group(),因为none没有group()方法
        if request:
            info = request.group('info')  # 提取请求内容
            print("请求内容:", info)
            self.request(connfd, info)
        else:
            self.__rlist.remove(connfd)
            connfd.close()

    #1 根据请求组织响应内容，发送给浏览器
    def request(self,connfd, name):
        if name == '/':
            name = self.html + "/index.html"
        else:
            name = self.html + name
        try:
            f = open(name, "rb")  # 有可能有图片
        except:
            #出现异常执行的代码块
            html = 'HTTP/1.1 404 Not Found\r\n'
            html += 'content-Type:text/html\r\n'
            html +='\r\n'
            html+='<h1>Sorry....</h1>'
            html=html.encode()

        else:
            #请求的文件存在
            data = f.read()
            html = 'HTTP/1.1 200 ok\r\n'
            html += 'content-Type:text/html\r\n'
            html += 'content-Length:%d\r\n' % len(data)
            html += '\r\n'
            html = html.encode() + data
            # 不能将f.read转换成字符串相加，因为可能是图片，不是所有字符串都能转换成字符串
        finally:
            #肯定会执行的语句
            connfd.send(html)




if __name__ == '__main__':
    httpd = WebServer(host="0.0.0.0", port=12233, html='./static')
    httpd.start()