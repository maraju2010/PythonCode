import requests
import logging

logging.getLogger(__name__)

class postclient(object):

    def __init__(self):
        pass

    def _send(self,url,params):
        try:
            #params = "&".join("%s=%s" % (k,v) for k,v in payload.items())
            session=requests.Session()
            session.trust_env=False
            res=session.get(url,params=params,timeout=2)
            return res
        except Exception as e:
            logging.debug("failed sending http request %s" %e)

if __name__ == "__main__":
    r = postclient()
    r._send('http://172.30.39.152:8080/CTIAgentEvent/CTIAgentEventService.asmx/InsertAgentEvent',{'cisco':'cisco'})
