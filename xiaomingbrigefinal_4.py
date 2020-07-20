'''
小明家必须要过一座桥。小明过桥最快要１秒，小明的弟弟最快要３秒，
小明的爸爸最快要６秒，小明的妈妈最快要８秒，小明的爷爷最快要１２秒。
每次此桥最多可过两人，而过桥的速度依过桥最慢者而定。
过桥时候是黑夜，所以必须有手电筒，小明家只有一个手电筒，
而且手电筒的电池只剩30秒就将耗尽。小明一家该如何过桥，请写出详细过程。
'''
#思路1快的人多走几次
# 思路2 慢的人尽量少走，让第二快的人回来
#让最快的人和第二快的人往返

#1.小明和弟弟先走 3 小明回来 1
#2.妈妈和爷爷走12 弟弟回来3
#3.小明和爸爸走6 小明回来1
#4.小明和弟弟走3

#随机找人从a岸到b岸去，统计每次的时间，直到有一次时间小于30为止
import random
while True:
    # a岸
    a = [1, 3, 6, 8, 12]
    # b岸
    b = []
    # 总时间
    total_time = 0
    # 流程
    step = []

    while True:
        # 随机获取两个a中的元素
        x = random.sample(a, 2)   #结果为列表
        # 将元素放入b中
        b.extend(x)
        # 从a中删除元素
        a.remove(x[0])
        a.remove(x[1])
        step.append(x)  # 将随机组合添加到列表
        step.append(max(x))  # 将随机组合的过河时间也添加到列表
        if not a:
            break

        # 从b中随机找一个到a
        # y = random.sample(b, 1)
        #从b中找最快的人回来
        y=min(b)
        a.append(y)
        b.remove(y)
        step.append(y)  # 记录 返回的时间
        step.append('||')

    # print(step)
    for i in step:
        if type(i) == int:
            total_time += i
    if total_time <= 30:
        break
print(total_time)
print(step)
#[[3, 1], 3, 1, '||', [12, 8], 12, 3, '||', [3, 1], 3, 1, '||', [6, 1], 6]