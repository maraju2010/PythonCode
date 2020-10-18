import os
import time
from datetime import datetime
import asyncio
from CDRAnalyzer.settings import global_conf as conf
from CDRAnalyzer.MQ import service
from CDRAnalyzer.loader import csvtodb as csv
from CDRAnalyzer.util.exceptions import ImproperlyConfigured
from CDRAnalyzer.util.file import filepath

class Worker(object):

    def __init__(self):
        self.dir = conf.MON_PATH
        self.flag = 0
        self.f = filepath()
        if len(conf.cache) > 0:
            self.before_path = conf.cache
        else:
            self.before_path = os.listdir(self.dir)

    async def _start(self):
        try:
            while (self.flag==0):
                after_path = os.listdir(self.dir)
                file_list = [f for f in after_path if f not in self.before_path]
                yield file_list
                self.before_path = after_path
                #time.sleep(5)
                print("in worker reached here @%s" % str(datetime.now()))
                await asyncio.sleep(20)
        except:
            self.f.write_file(self.before_path)


    def _stop(self):
        self.flag == 1

    @property
    def setattr(self):
        pass

    def write_to_cache(self):
        self.f.write_file(self.before_path)

class Notifier(object):

    def __init__(self):
        self.pub = service.publisher()

    def notify(self,fp):
        self.pub._send_message(fp)

class Listener(object):

    def __init__(self):
        self.sub = service.consumer()

    def receive(self):
        self.sub._recv_message()

class _parser(object):
    def __init__(self):
        self.s = csv.to_db()

    def _parse(self,fp=None,tb=None,db=None):
        #read from file and load to db
        if fp:
            self.tb = tb
            self.db = db
            for f in fp:
                #print ("This _parser %s" % f)
                self.s.read_fp(fp=str(f),tb=self.tb,db=self.db)
