# -*- coding:utf-8 -*-
import _thread
import time

def print_time(threadName, delay):
    count = 0
    while count < 50:
        time.sleep(delay)
        count += 1
        print("%s: %s" % (threadName, count))

if __name__ == "__main__":
    try:
        _thread.start_new_thread(print_time, ("thread-1", 0.05))
        _thread.start_new_thread(print_time, ("thread-2", 0.10))
    except:
        print("无法启动线程")

    while True:
        pass