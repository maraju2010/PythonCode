"""
work in progress not in use for now.

"""
from CDRAnalyzer.MQ import base as MQBASE
from CDRAnalyzer.settings import global_conf as conf

class publisher(MQBASE.MQ_Service):

    def __init__(self):
        self.host = conf.HOST
        self.port = conf.PORT
        self.queue = conf.Queue[0]
        super(publisher,self).__init__(self.host,self.port)
        #add this class initializers
        self._connect(self.queue)

    def _send_message(self,msg):
        self._pub(msg)

class consumer(MQBASE.MQ_Service):

    def  __init__(self):
        self.host = conf.HOST
        self.port = conf.PORT
        self.queue = conf.Queue[0]
        super(consumer,self).__init__(self.host,self.port)
        self._connect(self.queue)

    def _recv_message(self):
        self._sub(callback)

    def callback(self,ch, method, properties, body):
        #override
        pass
