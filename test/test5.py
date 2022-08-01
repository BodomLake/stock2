# 对于io操作，多线程和多进程性能差别不大

import time
import threading
import multiprocessing

print(multiprocessing.cpu_count())

def get_detail_html(url):
    print('我获取详情内容了')
    time.sleep(2)
    print('我获取内容完了')


def get_detail_url(url):
    print('我获取url了')
    time.sleep(2)
    print('我获取url完了')


if __name__ == '__main__':
    thread1 = threading.Thread(target=get_detail_html, args=('',))
    thread2 = threading.Thread(target=get_detail_url, args=('',))
    start_time = time.time()
    # thread1.start()
    # thread2.start()
    # 时间非常小，是运行代码的时间差，而不是2秒
    # 这样运行一共有三个线程，主线程和其他两个子线程（thread1，thread2），而且是并行的，子线程启动后，主线程仍然往下运行，因此时间不是2秒
    # 守护线程（主线程退出，子线程就会kill掉）
    print('last time:{}'.format(time.time() - start_time))

