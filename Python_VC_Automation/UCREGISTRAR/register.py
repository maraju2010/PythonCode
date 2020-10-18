import requests
import time
import datetime
#from axl1 import axl
from xml.etree.ElementTree import Element, SubElement, Comment,ElementTree
from xml.etree import ElementTree as ST
from xml.dom import minidom
import register_prop as _prop
import sys
import pika
import threading
import logging
import logging.handlers
from logging.config import fileConfig
from logging.handlers import RotatingFileHandler
# load the logging configuration
#logging.config.fileConfig('LoggerProperty.ini')
#logging.getLogger(__name__)

logfile = _prop.filename
loglevel = _prop.loglevel
count = _prop.count
size = _prop.logsize
logger = logging.getLogger(__name__)
logger.setLevel(loglevel)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              logfile, maxBytes=size, backupCount=count)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(lineno)d- %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

callqueue={}

class register(object):

    def __init__(self,res):
        self.response=res.text
        self.status=res.status_code

    @classmethod
    def postrequest(cls,ipaddr,username,password,reqtype):

        codec_username=username
        codec_password=password
        codec_ip=ipaddr
        headers={"content-type":"text/xml"}
        body=register.convertdatatoxml(reqtype)
        if _prop.journallog=="DEBUG":
            logger.info("post request body %s" % body)
        #from xml.etree.ElementTree import ElementTree as ET
        session=requests.Session()
        session.trust_env=False
        try:
            res=session.post("http://" + ipaddr + "/putxml",
            headers=headers,auth=(username,password),data=body,timeout=2)
            res.close()
            return cls(res)
        except Exception as e:
            logger.info("caught exception %s" %  e)

    @staticmethod
    def convertdatatoxml(reqtype=None):
        root=Element("Command")
        child=SubElement(root,"HttpFeedback")
        child1=SubElement(child,'Register',{"command":"True"})
        child2=SubElement(child1,"FeedbackSlot")
        child2.text="2"
        child3=SubElement(child1,"ServerUrl")
        child3.text="http://" + _prop.ServerIP + ":" + "8080"
        child4=SubElement(child1,"Expression",{"item":"2"})
        child4.text="/Event/CallSuccessful"
        child5=SubElement(child1,"Expression",{"item":"3"})
        child5.text="/Event/CallDisconnect"
        xmldata=register.prettify(root)
        return xmldata

    @staticmethod
    def prettify(elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ST.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

class MQService(object):
    def __init__(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost",5672))
            logger.info("mq connection %s" % self.connection)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='UCREGQUEUE')
            logger.info("register mq reciever on")
            self.channel.basic_consume(self._callback,
                                    queue='UCREGQUEUE',
                                    no_ack=True)
            self.channel.start_consuming()
        except Exception as e:
            logger.info("caught exception %s" %  e)

    def _callback(self,ch,method,properties,body):
        logger.info("register mq reciever on %r" % body)
        ipaddr,state=str(body.decode("utf-8")).split("=")
        callqueue[ipaddr]=state

    def _close(self):
        self.connection.close()

class init_main(object):
    #TODO
    def __init__(self):
        #TODO
        #use arrays
        self.register_db = {}
        self.init_list()
        self._start()

    def init_list(self):
        #states
        #0 not subscribed
        #1 subscribed completed for  newcall
        #2 subscribe required for  disconnect
        #3 subscribe completed for disconnect
        for k,v in _prop.EndpointIP.items():
            IP = k.strip()
            self.register_db[IP]=0

    def _start(self):
        logger.info(self.register_db)
        while True:
            for k,v in _prop.EndpointIP.items():
                try:
                    IP = k.strip()
                    NameofEndpoint,PriorityTag,Circle,CredentialsGroup=self._get_elements(v)
                    if self.register_db.get(k)==0:
                        try:
                            username,password = self._get_credentials(CredentialsGroup)
                            s=register.postrequest(IP,username,password,"RegisterConnect")
                            if _prop.journallog=="DEBUG":
                                logger.info("response received %s" %s.response)
                        except Exception as e:
                            logger.info("caught exception %s" %  e)
                    elif callqueue.get(IP)==2:
                        #received from MQ
                        self.register_db[IP]=0
                    else:
                        pass
                except Exception as e:
                    logger.info(" caught exception %s" % e)
            time.sleep(1800)

    def _get_elements(self,v):
        try:
            NameofEndpoint = v[0] if (len(v)>1 or len(v)==1)  else None
            if len(v)>2:
                PriorityTag = v[1] if (len(v)>2 or len(v)==2)  else None
                Circle = v[2] if (len(v)>3 or len(v)==3)  else None
                CredentialsGroup = v[3] if (len(v)>4 or len(v)==4)  else None
                return NameofEndpoint,PriorityTag,Circle,CredentialsGroup
            return NameofEndpoint,"unknown","unknown","unknown"
        except Exception as e:
            logger.info("caught exception %s" % e)

    def _get_credentials(self,GRP):
         credential= _prop.VCredentials.get(GRP)
         if credential:
             return credential[0].strip(),credential[1].strip()
         return _prop.Credentials.get("username"),_prop.Credentials.get("password")

if __name__=="__main__":
    t1 = threading.Thread(target=MQService)
    t1.setDaemon(True)
    t1.start()
    init_main()
