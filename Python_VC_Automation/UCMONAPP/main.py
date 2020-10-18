from requestapi import xml_api
import prop
import syslogclient
import xmlparser
import checkthreshold
import time
import datetime
import logging
import pika
import threading
import causecodeTable as CauseCodeMap
import command
import message
from functools import partial
from state import Abstract
import logging
import logging.handlers
from logging.config import fileConfig
from logging.handlers import RotatingFileHandler
# load the logging configuration
#logging.config.fileConfig('LoggerProperty.ini')
#logging.getLogger(__name__)

logfile = prop.filename
loglevel = prop.loglevel
count = prop.count
size = prop.logsize
logger = logging.getLogger(__name__)
logger.setLevel(loglevel)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              logfile, maxBytes=size, backupCount=count)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(lineno)d- %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


'''
    declare 3 Tables
    1) Poll Table : Stores endpoint IP and other details and uses it for polling each phone.
    2) Event Table: MQ service writes IP address into this table when there is call Start event observed on phone.
    3) Msg Queue Table : MQ service writes messages into this table when there is Call End event observed on phone.

'''

Poll_Table={}

Msg_Queue = {}

Event_Table = {}

class main(Abstract):
    def __init__(self):
        '''
            This Class runs in loop and invokes Event Mode or Poll Mode and calls other modules
            based on logic defined.
        '''
        logger.info("Initialize main instance")
        self.xmlparser = xmlparser.xmlparser(logger)
        self.checkTR = checkthreshold.checkthreshold(logger)
        self.syslogclient = syslogclient.syslog(logger)
        self.message = message.message(logger)
        self.callID = "0"
        self.lastcheck={}
        self.ActiveAlert={}
        self.VCActiveAlert = {}
        self._initialize_state()
        self.setlogging()
        self.__run()

    def _initialize_state(self):
        '''
            initialize the state for each phone to start polling.
        '''
        for k,v in prop.EndpointIP.items():
            ip=k.strip()
            Poll_Table[ip]=0
            self.lastcheck[ip]=datetime.datetime.now()
            self.ActiveAlert[ip]=[0,datetime.datetime.now()]
            self.VCActiveAlert[ip]=[0,"0",datetime.datetime.now()]

    def setlogging(self):
        '''
            logging level definition.
        '''
        if prop.logginglevel==0:
            LogLevel = "INFO"
        elif prop.logginglevel==1:
            LogLevel = "ERROR"
        elif prop.logginglevel==2:
            LogLevel = "CRITICAL"
        else:
            LogLevel = "DEBUG"
        if prop.enableTivoli==1:
            self.logger1 = self.syslogclient.createhandler(LoggerName="tivoli_logger",LoggerLevel=LogLevel,\
            LogFileName=prop.TivoliLogfilePath,Handler="tivoli_handler")
        if prop.enableFilebeat==1:
            self.logger2 = self.syslogclient.createhandler(LoggerName="filebeat_logger",LoggerLevel=LogLevel,\
            LogFileName=prop.FilebeatLogfilePath,Handler="filebeat_handler")
        else:
            pass

    def __run(self):
        try:
            '''
                invokes event or poll mode.
            '''
            logger.info("Entering main run loop ")
            while True:
                if Event_Table:
                    self._invoke_Eventmode()
                else:
                    self._invoke_Pollmode()
                time.sleep(2)
        except Exception as e:
            logger.info("caught exception %s" %  e)

    def _invoke_Eventmode(self):
        '''
        #0: Call Start Event
        #1: time lapse from last Check
        #2: Call End Event
        '''
        try:
            for k,v in Event_Table.items():
                self.ipaddr = k
                self.currtime = datetime.datetime.now()
                self.endpoint,self.priority,self.circle,self.credentialsgroup,\
                self.mailgrp,self.alertmark,self.vcalertmark = self._get_elements(self.ipaddr)
                self.callID = "0"
                #print("what is alert mark %d" % self.alertmark,self.ipaddr)
                if v==0:
                    srcflag="EM"
                    self.username,self.password = self._get_credentials(self.credentialsgroup)
                    if int(self.alertmark)==0:
                        res=self.__sendreq(self.ipaddr,self.username,self.password)
                        self._process_response(res,srcflag)
                elif v==1:
                    if self.lastcheck.get(self.ipaddr) < (self.currtime - datetime.timedelta(seconds=\
                    prop.lst_check_MQendpoint)):
                        Event_Table[self.ipaddr]=0
                elif v==2:
                    if prop.journallog=="DEBUG":
                        logger.debug("enter cause code analysis")
                    if Msg_Queue.get(self.ipaddr)!=None:
                        self._causecodecheck(Msg_Queue.get(self.ipaddr))
                        del Msg_Queue[self.ipaddr]
                        del Event_Table[self.ipaddr]
                        self.ActiveAlert[self.ipaddr]=[0,self.currtime]
                        self.VCActiveAlert[self.ipaddr]=[0,"0",datetime.datetime.now()]
                        #Poll_Table[self.ipaddr]==1
                else:
                    pass
        except Exception as e:
            logger.info("caught exception %s" % e)

    def _invoke_Pollmode(self):
        '''
        #0: Start Polling
        #1: time lapse from last Check
        #2: time lapse from last Check for failed endpoints
        '''
        try:
            for k,v in prop.EndpointIP.items():
                self.ipaddr=k
                self.currtime=datetime.datetime.now()
                self.endpoint,self.priority,self.circle,self.credentialsgroup,\
                self.mailgrp,self.alertmark,self.vcalertmark = self._get_elements(self.ipaddr)
                self.callID = "0"
                if Event_Table:
                    break
                elif Poll_Table[self.ipaddr]==0:
                    srcflag="PM"
                    self.username,self.password = self._get_credentials(self.credentialsgroup)
                    if int(self.alertmark)==0:
                        res = self.__sendreq(self.ipaddr,self.username,self.password)
                        self._process_response(res,srcflag)
                elif Poll_Table[self.ipaddr]==1:
                    if self.lastcheck.get(self.ipaddr) < (self.currtime - datetime.timedelta(seconds=\
                    prop.lst_check_endpoint)):
                        Poll_Table[self.ipaddr]=0
                elif Poll_Table[self.ipaddr]==2:
                    if self.lastcheck.get(self.ipaddr) < (self.currtime - datetime.timedelta(seconds=\
                    prop.lst_chk_failedendpoint)):
                        Poll_Table[self.ipaddr]=0
                else:
                    pass
        except Exception as e:
            logger.info("caught exception %s" % e)

    def _get_elements(self,v):
        '''
            set phone details such as endpoint name, priority tag, circle, credential grp, mail grp.
        '''
        try:
            value = prop.EndpointIP.get(v)
            if isinstance(value,list):
                NameofEndpoint = value[0] if (len(value)>1 or len(value)==1)   else "unknown"
                PriorityTag = value[1] if (len(value)>2 or len(value)==2) else "unknown"
                Circle = value[2] if (len(value)>3 or len(value)==3)  else "unknown"
                CredentialsGroup = value[3] if (len(value)>4 or len(value)==4) else "unknown"
                MailGroup = value[4] if (len(value)>5 or len(value)==5)  else "unknown"
                AlertMark = int(value[5]) if (len(value)>6 or len(value)==6)  else 1
                VCAlertMark = int(value[6]) if (len(value)>7 or len(value)==7)  else 1
                return NameofEndpoint,PriorityTag,Circle,CredentialsGroup,MailGroup,\
                AlertMark,VCAlertMark
            return "unknown","unknown","unknown","unknown","unknown",0,0
        except Exception as e:
            logger.info("caught exception %s" %  e)

    def _get_credentials(self,GRP):
        '''
            function to retrieve credentials of phone.
        '''
        credential= prop.VCredentials.get(GRP)
        if credential:
            return credential[0].strip(),credential[1].strip()
        return prop.Credentials.get("username"),prop.Credentials.get("password")


    def __sendreq(self,ipaddr,username,password):
        '''
            Sends request to phone and fetches response.
        '''
        try:
            logger.info("sending post request %s" % ipaddr)
            res = xml_api.getrequest(ipaddr,username,password)
            return res
        except Exception as e:
            logger.info("caught exception %s" %  e)

    def _process_response(self,res,srcflag):
        '''
            process the returned xml response from  phone.

        '''
        if res.response is not None:
            logger.info("received successful response")
            if srcflag=="EM":
                Event_Table[self.ipaddr]=1
                self.lastcheck[self.ipaddr]=self.currtime
            else:
                Poll_Table[self.ipaddr]=1
                self.lastcheck[self.ipaddr]=self.currtime
            xmllist = self.xmlparser.xmlparser(res.response)
            self._validate_response(xmllist,srcflag)
        else:
            if isinstance(res,Exception):
                if prop.journallog=="DEBUG":
                    print("%s : %s %s caught exception %s" % (datetime.datetime.now(),"main", "159",res))
                if srcflag=="EM":
                    Event_Table[self.ipaddr]=1
                    self.lastcheck[self.ipaddr]=self.currtime
                else:
                    Poll_Table[self.ipaddr] = 2
                    self.lastcheck[self.ipaddr] = self.currtime
            else:
                if prop.journallog=="DEBUG":
                    logger.info("caught exception %s" % res)
                if srcflag=="EM":
                    Event_Table[self.ipaddr]=1
                    self.lastcheck[self.ipaddr]=self.currtime
                else:
                    Poll_Table[self.ipaddr] = 1
                    self.lastcheck[self.ipaddr] = self.currtime

    def _validate_response(self,xmllist,srcflag):
        '''
            invoke appropriate function calls to tivoli or filebeat based on property setting.
        '''
        if isinstance(xmllist,dict):
            sysloglist = self.getTR(xmllist)
            if sysloglist:
                if prop.enableTivoli == 1:
                    self.send_Tivoli(sysloglist,srcflag)
                if prop.enableSDL == 1:
                    self.send_SDL(sysloglist,srcflag)
                if prop.enableVC == 1:
                    self.callID = xmllist.get("CALLID","0")
                    self._send_VC(sysloglist,srcflag)
            if len(xmllist)>0:
                if prop.enableFilebeat == 1 :
                    self.send_Filebeat(xmllist,srcflag)
        else:
            if prop.journallog=="DEBUG":
                logger.info("received response has empty content %s" % xmllist)
            if srcflag=="EM":
                Event_Table[self.ipaddr]=1
                self.lastcheck[self.ipaddr]=self.currtime
            else:
                Poll_Table[self.ipaddr] = 1
                self.lastcheck[self.ipaddr] = self.currtime


    def getTR(self,xmllist):
        '''
            Check if values returned from phone is beyond threshold.
        '''
        try:
            field=0
            sylist=[]
            for k,v in prop.ATTRIBUTES.items():
                param1,param2 = xmllist.get(v[0]),xmllist.get(v[1],"NULL")
                if prop.journallog=="DEBUG":
                    logger.debug("param1 %s param2 %s" % (param1,param2))
                    logger.debug("typeparam1 %s typeparam2 %s" % (type(param1),type(param2)))
                if param2 is "NULL":
                    if param1 is not None:
                        if int(param1)>0:
                            rl = self.checkTR.checkthreshold(param1,k)
                            if rl:
                                sylist.append(rl)
                        else:
                            pass
                else:
                    if param1 and param2:
                        if len(param1)>0 and len(param2)>0:
                            field=self.checkTR.calculateloss(param1,param2)
                            if prop.journallog=="DEBUG":
                                logger.info("calculate loss")
                            if field>0:
                                rl = self.checkTR.checkthreshold(field,k)
                                if rl:
                                    sylist.append(rl)
                            else:
                                pass
            return sylist
        except Exception as e:
            logger.info("caught exception %s" %  e)

    def send_Tivoli(self,sysloglist,srcflag):
        '''
            calls syslog function to send message to tivoli agent.
        '''
        if sysloglist:
            if self.alertmark==0:
                routing = self._counter
                if routing == 0:
                    if prop.journallog=="DEBUG":
                        logger.info("send to syslog for device %s" % self.endpoint)
                    self.syslogclient.sendalert(sysloglist,self.endpoint,self.logger1,self.ipaddr,self.priority,self.circle)
                else:
                    pass

    def send_Filebeat(self,xmllist,srcflag):
        '''
            call syslog function to send message to filebeat agent.
        '''
        try:
            if len(xmllist)>0:
                xmllist["ENDPOINT"]=self.endpoint
                xmllist["PRIORITY"]=self.priority
                xmllist["CIRCLE"]=self.circle
                xmllist["DateTime"]=self.currtime
                self.syslogclient.sendmsg(xmllist,self.logger2)
        except Exception as e:
            logger.info("caught exception %s" % e)

    def send_SDL(self,sysloglist,srcflag):
        ''' Direct integration with SDP MG URL '''
        if sysloglist:
            if self.alertmark==0:
                routing = self._counter
                if routing == 0:
                    if prop.journallog=="DEBUG":
                        logger.debug("send to SDL MG URL for device %s" % self.endpoint)
                    self.syslogclient.sendalert(sysloglist,self.endpoint,self.logger1,self.ipaddr,self.priority)
        else:
            pass

    def _send_VC(self,sysloglist,srcflag):
        if sysloglist:
            if self.vcalertmark==0:
                routing = self._VC_counter
                if routing == 0:
                    if prop.journallog=="DEBUG":
                        logger.debug("send to VC syslog for device %s" % self.endpoint)
                    message = self.message._filtermessage(sysloglist)
                        #print("what is final message %s" % message)
                    if message:
                        self._send_command(message)
                    else:
                        self._set_VCAlert(0)

    @property
    def _VC_counter(self):
        counterlist = self.VCActiveAlert.get(self.ipaddr)
        counter,vccallid,prevtimestamp = counterlist[0],counterlist[1],counterlist[2]
        if counter==0:
            counter +=1
            self._set_VCAlert(counter)
            return 0
        else:
            if self._VC_analyse_counter(prevtimestamp,vccallid):
                counter = 0
                self._set_VCAlert(counter)
                return 0
            else:
                counter +=1
                self._set_VCAlert(counter)
                return 1

    def _set_VCAlert(self,counter):
        self.VCActiveAlert[self.ipaddr] = [counter,self.callID,self.currtime]

    def _VC_analyse_counter(self,prevtimestamp,vccallid):
        if vccallid==self.callID:
            if int((self.currtime - prevtimestamp).total_seconds()) > int(prop.VCAlert_MaxTime):
                return True
            return False
        else:
            return True

    def _send_command(self,message):
        response = command.commands.postrequest(self.ipaddr,self.username,self.password,message)
        logger.info("from vcendpoint putxmlcommand %s" % response.status)

    @property
    def _counter(self):
        counterlist = self.ActiveAlert.get(self.ipaddr)
        counter,prevtimestamp = counterlist[0],counterlist[1]
        if counter>2:
            if self._analyse_counter(prevtimestamp):
                counter = 0
                self.ActiveAlert[self.ipaddr]=[counter,self.currtime]
                return 0
            else:
                return 1
        else:
            counter += 1
            self.ActiveAlert[self.ipaddr]=[counter,self.currtime]
            return 0

    def _analyse_counter(self,prevtimestamp):
        if int((self.currtime - prevtimestamp).total_seconds()) > int(prop.Alert_MaxTime):
             return True
        else:
            return False

    def _causecodecheck(self,msg):
        '''
            function to validate the disconnect message and check cause code and send to syslog.
        '''
        try:
            logger.info("entered causecode func")
            #srcdesc=msg[msg.find('descr')+6:msg.find(',CallType')]
            CauseType,CauseCode,dst,src,Cause,dt= self._parse_causecode(msg)
            srcdesc  = self._set_srcdesc()
            if prop.journallog=="DEBUG":
                logger.debug("CauseCode:%s and Cause:%s" % (CauseCode,Cause))
            if Cause:
                if Cause=="DISABLED":
                    pass
                else:
                    newmsg = "%s-%s %s: Call disconnected between src %s - %s and dest %s with causevalue %s desc %s \n" \
                    %(self.priority,self.circle,dt,src,srcdesc,dst,CauseCode,Cause)
                    if prop.enableFilebeat == 1 :
                        self.syslogclient.sendmsg(newmsg,self.logger2)
                    if prop.enableTivoli == 1:
                        self.syslogclient.sendmsg(newmsg,self.logger1)

            else:
                newmsg = "%s-%s %s: Call disconnected between src %s - %s and dest %s with causecode %s\n" \
                %(self.priority,self.circle,dt,src,srcdesc,dst,CauseCode)
                if prop.enableFilebeat == 1 :
                    self.syslogclient.sendmsg(newmsg,self.logger2)
                if prop.enableTivoli == 1:
                    self.syslogclient.sendmsg(newmsg,self.logger1)

        except Exception as e:
            logger.info("caught exception %s" %  e)

    def _parse_causecode(self,msg):
        try:
            CauseType=msg[msg.find('CauseType')+10:len(msg)]
            CauseCode=msg[msg.find('CauseCode')+10:msg.find(',CauseType')]
            dst=msg[msg.find('dst')+4:msg.find(',src')]
            src=msg[msg.find('src')+4:msg.find(',desc')]
            Cause = CauseCodeMap.getcode(int(CauseCode))
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return CauseType,CauseCode,dst,src,Cause,dt
        except Exception as e:
            logger.info("caught exception %s" %  e)

    def _set_srcdesc(self):
        if self.priority:
            srcdesc = self.endpoint
        else:
            srcdesc = self.endpoint
        return srcdesc


class MQService(object):
    def __init__(self):
        '''
            initialize MQService
        '''
        try:
            logger.info("Start UCMONAPP MQ Service")
            self.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost",5672))
            logger.info("MQ connection %s" % self.connection)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='UCMONQUEUE')
            logger.info("ucmon mq reciever on ")
            self.threadHB()
            self.channel.basic_consume(self._callback,
                                        queue='UCMONQUEUE')
            self.channel.start_consuming()

        except Exception as e:
            logger.info("caught exception %s" % e)

    def threadHB(self):
        '''
            Heart beat thread.
        '''
        try:
            t= threading.Thread(target=self._HB)
            t.daemon = True
            t.start()
        except Exception as e:
            logger.info("caught exception %s" %e)

    def ack_message(self,delivery_tag):
        """Note that `channel` must be the same pika channel instance via which
        the message being ACKed was retrieved (AMQP protocol constraint).
        """
        if self.channel.is_open:
            self.channel.basic_ack(delivery_tag)
        else:
            # Channel is already closed, so we can't ACK this message;
            # log and/or do something that makes sense for your app in this case.
            pass

    def _HB(self):
        self.connection.process_data_events()
        self.connection.sleep(30)

    def _callback(self,ch,method,properties,body):
        '''
            invokes callback when there is message in MQ queue.
        '''
        try:
          logger.info("mq message received %r" % body)
          header,content=str(body.decode("utf-8")).split(",",1)
          Ignore,EvType=header.split("Event=",1)
          ipaddr=content[content.find('src')+4:content.find(',descr')]
          #desc=msg[msg.find('descr')+6:msg.find(',CallType')]
          if EvType=="Success":
              if prop.journallog=="DEBUG":
                  logger.debug("Success State Set")
              Event_Table[ipaddr]=0
          else:
              if prop.journallog=="DEBUG":
                  logger.debug("Disconnect State Set")
              Event_Table[ipaddr]=2
              Msg_Queue[ipaddr] = content
          self.ack_message(method.delivery_tag)
        except Exception as e:
            logger.info("caught exception %s" %  e)

    def _close(self):
        '''
            closes the MQ session.
        '''
        self.connection.close()

if __name__ == "__main__":
    '''
        Main Function , it calls MQ in thread 1 and Main Class in Main thread.
    '''
    t1 = threading.Thread(target=MQService)
    t1.setDaemon(True)
    t1.start()
    #main function to start module
    main()
