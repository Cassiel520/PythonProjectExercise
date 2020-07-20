'''
练习1： 一个线程打印1--52 另一个线程打印A--Z
两个线程一起启动，要求打印的结果
12A34B56C.....5152Z

提示: 使用同步互斥方法控制线程执行
程序中不一定只有一个锁
'''
from threading import Thread,Lock
lock1=Lock()
lock2=Lock()
def print_num():
    # 每次打印两个数字
    for i in range(1,53,2):
        lock1.acquire()
        print(i)
        print(i+1,)
        lock2.release()
def print_char():
    for i in range(65,91):
        lock2.acquire()
        print(chr(i))
        lock1.release()
t=Thread(target=print_num)
t.start()
#为了先打印数字，重复加锁会阻塞，此时只有print_num()才会执行，再次循环时，是二次加锁，
# 只能等待print_char帮忙解锁，而刚好print_num()已经解锁lock2，所以可以打印一个字母……
lock2.acquire()
print_char()