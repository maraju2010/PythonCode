"""
work in progress not in use for now.

"""
import concurrent.futures
from CDRAnalyzer.monitor import worker
from CDRAnalyzer.logic import algo_1 as algo
import sys

def  thread_worker():
    w=worker.Worker()
    _p= worker._parser()
    f=w._start()
    for f in fl:
        _p._parse(fp=f,tb="cdr_main",db="cdr_portal")

def  thread_notifier():
    n=worker.Notifier()
    n.notify()

def thread_listener():
    l=worker.Listener()

def thread_algo():
    a=algo.auth_code_sn()
    a._analyse()

class Pool(object):

    def _start(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            try:
                a = executor.submit(thread_worker)
                b = executor.submit(thread_algo)
                #c = executor.submit(thread_listener)
            except:
                sys.exit()
