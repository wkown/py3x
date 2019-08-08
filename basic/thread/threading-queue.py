#!/usr/bin/python3
# -*- coding:utf-8 -*-

# 线程间通过队列同步数据

import queue
import threading
import time

exitFlag = 0

class MyThread(threading.Thread):
    def __init__(self, threadID, name, q, lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.queue = q
        self.lock = lock
    def run(self):
        print("开启线程:", self.name)
        process_data(self.name, self.queue, self.lock)
        print("退出线程：", self.name)

def process_data(threadName, q, lock):
    while not exitFlag:
        lock.acquire()
        if not q.empty():
            data = q.get()
        else:
            data = None
        lock.release()
        if data is not None:
            print("%s processing %s" % (threadName, data))
        time.sleep(1)



threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = queue.Queue(10)
threads = []

# 创建线程 消费者
threadID = 1
for tName in threadList:
    thread = MyThread(threadID, tName, workQueue, queueLock)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列 生产者
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

while not workQueue.empty():
    pass

exitFlag = 1

for t in threads:
    t.join()

print("退出主线程")
