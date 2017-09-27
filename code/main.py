# -*- coding: utf-8 -*-
import threading
from . import monitor

ori_url = 'http://stuex.nju.edu.cn/a/tztg/'
front = 'http://stuex.nju.edu.cn'

_an_hour = 1*60*60

def f_timer():
    global timer
    monitor.crawl(front=front,url=ori_url)
    timer = threading.Timer(_an_hour, f_timer)
    timer.start()


if __name__ == '__main__':
    timer = threading.Timer(0, f_timer)
    timer.start()
