# -*- coding: utf-8 -*-
import threading
from time import ctime, sleep
from random import randint
from Queue import Queue
import requests


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def getResult(self):
        return self.res


    def run(self):
        print 'starting', self.name, 'at:', ctime()
        self.res = apply(self.func, self.args)
        print self.name, 'finished at:', ctime()




def writer(queue, loops):

    #for i in range(loops):
    for i in loops:
        #writerQ(queue)
        print 'producing object for Q...'
        queue.put(i)
        print "size now", queue.qsize
        #sleep(0.1)

def reader(queue, queued):
    while True:
        val = queue.get()
        response = requests.get(val)
        print 'consumed object from Q ... size now', val, queue.qsize()
        r = response.content
        queued.put(r)

    queue.task_done()
    print "我完成了！"
    queued.task_done()
    print "完成了！！"


def main():
    links = ['http://newjwgl.ncsxy.com/Content/Reporters/Keibao/ViewKebiao.aspx?kbtype=xh&xq=20162&usercode=%s' %i for i in range(15601101, 15601141)]
    q = Queue()
    qd = Queue()

    writer(q, links)

    threads = []


    for i in range(10):
        t = MyThread(reader, (q, qd), reader.__name__)
        threads.append(t)

    for i in range(10):
        threads[i].setDaemon(True)
        threads[i].start()

    for i in range(10):
        threads[i].join()

    print "all DONE"
    while True:
        if qd.empty():
            break
        a = qd.get()
        print a

if __name__ == '__main__':
    main()
