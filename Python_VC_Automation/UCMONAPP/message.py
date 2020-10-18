import prop
import datetime
import time
import logging

class message(object):
    def __init__(self,logger):
        self.logging = logger

    def _filtermessage(self,msglist):
        #function will loop the list and generate alerts
        d={}
        buffer=[]
        if prop.journallog=="DEBUG":
            self.logging.info("send syslog message to vc endpoint %s" % msglist)
        for row,val in enumerate(msglist):
            d=msglist[row][0]
            self.logging.info("check d %s" % d)
            if prop.journallog=="DEBUG":
                self.logging.debug("filtered msg dict %s" % d)
            for key,val in d.items():
                if "JITTER" in key:
                    pass
                else:
                    if "CURIN" in key:
                        if buffer.count(key)>0:
                            pass
                        else:
                            buffer.append(key[5:])
                    if "CUROUT" in key:
                        if buffer.count(key)>0:
                            pass
                        else:
                            buffer.append(key[6:])
        return self._analyze(buffer)

    def _analyze(self,buffer):
        if len(buffer)>0:
            #return "High PKTLOSS observed for following connections\n" + '\n'.join('{}: {}'.format(*k) for k in enumerate(buffer))
            return "Alert: User may experience audio video quality issue due to external factors."
        return None
        #else:
        #    return "High PKTLOSS observed for following connections\n" + '\n'.join('{}: {}'.format(*k) for k in enumerate(v))
