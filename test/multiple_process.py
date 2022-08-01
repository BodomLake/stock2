import threading
from threading import Thread, Lock
import time

n = 100  # 共 100 张电影票


def task():
    global n
    mutex.acquire()  # 上锁
    temp = n  # 赋值给临时变量
    time.sleep(0.2)  # 睡眠 0.2 秒
    n = temp - 1  # 数量减 1
    print("购买成功，剩余 %d 张电影票" % n, "购买者是：%s", threading.current_thread().name)
    mutex.release()  # 释放锁


if __name__ == '__main__':
    mutex = Lock()
    list = []
    for i in range(10):
        th = Thread(target=task, name=('thread-' + str(i)))
        list.append(th)
        th.start()
    for th in list:
        th.join()
