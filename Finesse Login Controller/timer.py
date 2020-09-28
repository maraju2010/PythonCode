import time
import logging

logging.getLogger(__name__)

class Timer(object):

    def __init__(self,IRT,counter,maxtimelimit):
        self.RT=10
        self.oldIRT = IRT
        self.IRT = self.oldIRT
        self.counter = counter
        self.maxlimit = maxtimelimit

    def _set_timer(self,oldvalue):
        if oldvalue > self.maxlimit:
            self.IRT = self.oldIRT
            return self.IRT
        self.IRT=oldvalue*self.counter
        return self.IRT

    def _get_timer(self):
        return self.IRT

    def reset_timer(self):
        self.IRT = self.oldIRT
        return self.IRT
