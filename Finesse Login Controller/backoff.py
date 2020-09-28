import random
import logging

logging.getLogger(__name__)

class backoffalgorithm(object):
    def  __init__(self):
        self.counterA = random.randint(0,2**6)
        self.counterB = random.randint(0,5)
        #self.counterA = 1
        #self.counterB = 1
        self.advance_timer = self.counterA + self.counterB

    def _get_waittimer(self):
        return 2.5*self.advance_timer
