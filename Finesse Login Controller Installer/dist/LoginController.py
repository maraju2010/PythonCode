from restapi import finesseapi
from autologin import Browser
from xmlparser import xmlparser
from htmlparser import jshtml
from backoff import backoffalgorithm
from postclient import postclient
import property
import time
import sys
import timer
import datetime
import os
import logging
import logging.handlers
from logging.config import fileConfig
import configparser
import socket

browsersession = ""

# load the logging configuration
logging.config.fileConfig('LoggerProperty.ini')
logging.getLogger(__name__)

class MainApp(object):
    global browsersession

    def __init__(self):
        #initialize logincontroller app
        try:
            self.loggedOn = 0
            self.attempt = property.attempt
            self.counter = 0
            self.disablepwd=0
            self.session = Browser()
            self.xmlparse = xmlparser()
            self.jshtml = jshtml()
            self.rest = finesseapi()
            self.configobject = self.read_config()
            self.oldRTT,logincounter,maxtimelimit = self._read_timerA(self.configobject)
            self.t = timer.Timer(self.oldRTT,logincounter,maxtimelimit)
            self.pc = postclient()
            self.boff = backoffalgorithm()
            self.username = None
            #self.password = self._read_password(self.configobject)
            self.password = ""
            self.extension = None
            self.forced = False
            browsersession = self.session
            self.looptimer = 1
            self.init_wait=5
            self.LastTried = 0
            self.waittimer = self.boff._get_waittimer()
            self.Finesse_Primary_Server,self.Finesse_Secondary_Server = self._read_url(self.configobject)
            self.Location = self._read_location(self.configobject)
            finphost,finshost = self._set_host(self.Finesse_Primary_Server,self.Finesse_Secondary_Server)
            self.phost,self.shost = self._set_host_to_ip(finphost,finshost)
            self.CICM_Instance,self.PG = self.Config_set_instance(self.configobject)
            self.EventCode = 0
            self.EventTimeStamp = datetime.datetime.now()
            self.DeltaDuration = 0
            self.AgentName=""
            self.DateTime = datetime.datetime.now()
            self.FinesseUsed = ""
            self.Outage = 0
            self.OutageTime = 0
            self.currtime = datetime.datetime.now()
            self.EventQueue = []
            self.sendevent = 0
            self.webservercounter = 0
            self.errortimestamp = 0
            self.url = self._read_webserver(self.configobject)

        except Exception as e:
            logging.debug("Initialize of Main Application Failed: %s " % e)
            self._close()
            sys.exit(1)

    def _run(self):
        #loop call
        try:
            while True:
                if self.loggedOn==0:
                    #load url with no autologin
                    self._Load_url()
                elif self.loggedOn==1:
                    #load url and autologin
                    self._Login_user()
                elif self.loggedOn==2:
                    self._Verify_source()
                else:
                    #to be used for future reference
                    pass
                time.sleep(self.looptimer)

        except Exception as e:
            logging.error("Error Occured %s" %e)
            self._close()
            sys.exit(1)

    def _Login(self,username=None,password=None,extension=None):
        #function to invoke login
        try:
            if self.LastTried==0:
                if self.Finesse_Primary_Server:
                    self.FinesseUsed = self.phost
                    self.session.run(self.Finesse_Primary_Server)
                    if username:
                        self.session.login(username,password,extension)
                elif self.Finesse_Secondary_Server:
                    self.FinesseUsed = self.shost
                    self.session.run(self.Finesse_Secondary_Server)
                    if username:
                        self.session.login(username,password,extension)
                else:
                    logging.debug("Login to Finesse failed... no url configured")
            else:
                if self.Finesse_Secondary_Server:
                    self.FinesseUsed = self.shost
                    self.session.run(self.Finesse_Secondary_Server)
                    if username:
                        self.session.login(username,password,extension)
        except Exception as e:
                logging.debug("Login to Finesse failed: %s " % e)

    def validate(self,msg):
       #function to validate javascript return page
       try:
            if msg=="FORCEDLOGOUT":
                self._FORCEDLOGOUT()

            if msg=="ERR_INTERNET_DISCONNECTED":
                self._ERR_INTERNET_DISCONNECTED()

            if msg=="ERR_CONNECTION_ABORTED":
                self._ERR_CONNECTION_ABORTED()

            if msg=="ERR_NAME_NOT_RESOLVED":
                self._ERR_NAME_NOT_RESOLVED()

            if msg=="NEWLOGINPAGE":
               self._NEWLOGINPAGE()

            if msg=="REFRESHLOGINPAGE":
                self._REFRESHLOGINPAGE()

            if msg=="LOOPLOGINPAGE":
                self._LOOPLOGINPAGE()

            if msg=="LOGGEDIN":
                self._LOGGEDIN()

            if msg=="ALREADYLOGGEDIN" and self.username is None:
                self._ALREADYLOGGEDIN()

            if msg=="ALREADYLOGGEDIN" and self.username is not None:
                self._EVENTCHECK()

            if msg=="AFTERFORCED":
                self._AFTERFORCED()

            if msg=="PAGENOTLOADED":
                self._PAGENOTLOADED()

            if msg=="LOGINATTEMPTFAILED":
                self._LOGINATTEMPTFAILED()

       except Exception as e:
            logging.debug("failed validation page response %s" %e)

    def checkitems(self):
        #function to html page
        try:
            html = self.session.checkelement()
            if html=="NoSuchWindowException":
                logging.debug("failed browser unreachable")
                self._close()
                sys.exit(1)
            else:
                return html
        except Exception as e:
            logging.debug("failed checking session element %s" %e)

    def _Load_url(self):
        self._Login()
        self.loggedOn=2

    def _Login_user(self):
        self._Login(self.username,self.password,self.extension)
        self.loggedOn=2

    def _Verify_source(self):
        htmlpage = self.checkitems()
        parsedmsg = self.jshtml.parse_html(htmlpage)
        self.validate(parsedmsg)

    def _FORCEDLOGOUT(self):
        if self.username:
            self.loggedOn=1
        self.forced = True
        self.EventTimeStamp = datetime.datetime.now()
        self.EventCode = 2
        self.DeltaDuration = 0
        self.Outage = 1
        self.OutageTime = self.EventTimeStamp
        self.currtime = self.EventTimeStamp
        self.AgentName = self.get_AgentName()
        self.sendevent = 0
        self._setEventQueue()

    def _ERR_INTERNET_DISCONNECTED(self):
        if self.counter<self.attempt:
            self.loggedOn=0
            self.counter = self.counter+1
        else:
            self._close()
            logging.debug("Exceeded attempts: please check network connectivity and try again")
            sys.exit(1)

    def _ERR_CONNECTION_ABORTED(self):
        if self.counter<self.attempt:
            self.loggedOn=0
            self.counter = self.counter+1
        else:
            self._close()
            logging.debug("Exceeded attempts: please check network connectivity and try again")
            sys.exit(1)

    def _ERR_NAME_NOT_RESOLVED(self):
        if self.counter<self.attempt:
            self.loggedOn=0
            self.counter = self.counter+1
        else:
            self._close()
            logging.debug("Exceeded attempts: please check network connectivity and try again")
            sys.exit(1)

    def _NEWLOGINPAGE(self):
        self.loggedOn=2

    def _REFRESHLOGINPAGE(self):
        #REFRESH is invoked immediately after forced logout or manual logout
        if self.forced==True:
            self.loggedOn=1
        else:
            #print("seems user has manually logged out... exiting the app")
            self._close()
            sys.exit(1)

    def _LOOPLOGINPAGE(self):
        #LOOP LOGIN is invoked immediately after forced logout and post first time failure
        self.oldRTT = self.t._set_timer(self.oldRTT)
        time.sleep(self.oldRTT)
        self.loggedOn=1
        self._EVENTCHECK()

    def _LOGGEDIN(self):
        #LOGGED IN is invoked after user successfully logs in
        user_text = self.session.get_credentials()
        self.set_credentials(user_text)
        self.loggedOn=2
        self.EventTimeStamp = datetime.datetime.now()
        self.EventCode = 1
        self.DeltaDuration = 0
        self.currtime = self.EventTimeStamp
        self.sendevent = 0
        self.AgentName = self.get_AgentName()
        self._setEventQueue()
        if self.forced==True:
            self.forced=False

    def _ALREADYLOGGEDIN(self):
        #Already LOGGED IN is invoked after user successfully logs in and username
        # is not cached at first login
        user_text = self.session.get_credentials()
        self.set_credentials(user_text)
        self.loggedOn=2
        if self.forced==True:
            self.forced= False
        if self.oldRTT>10:
            self.oldRTT = self.t.reset_timer()

    def _PAGENOTLOADED(self):
        #PAGE not loaded to be invoked if url does not connect
        if self.counter<self.attempt:
            self.loggedOn=0
            if self.LastTried==0:
                self.LastTried=1
            else:
                self.LastTried=0
            self.counter = self.counter+1
        else:
            self._close()
            logging.debug("Exceeded attempts: please check network connectivity and try again")
            sys.exit(1)

    def _AFTERFORCED(self):
        #After forced  is invoked after user successfully logs in post forced logout
       user_text = self.session.get_credentials()
       self.set_credentials(user_text)
       self.loggedOn=2
       self.EventTimeStamp = datetime.datetime.now()
       self.EventCode = 3
       self.DeltaDuration = int((self.EventTimeStamp - self.OutageTime).total_seconds()) if self.Outage==1 else 0
       self.Outage = 0
       self.OutageTime = 0
       self.currtime = self.EventTimeStamp
       self.AgentName = self.get_AgentName()
       self.sendevent = 0
       self._setEventQueue()
       if self.forced==True:
           self.forced= False
       if self.oldRTT>10:
           self.oldRTT = self.t.reset_timer()

    def _LOGINATTEMPTFAILED(self):
        #print("called logging attempt failed func")
        self.session.reattempt()
        self.loggedOn=2

    def _EVENTCHECK(self):
        #eventcheck is called to send events to webserver
        if self.sendevent == 0:
            if int((datetime.datetime.now() - self.currtime).total_seconds()) > self.waittimer:
                    self._FIREEVENT()

    def _FIREEVENT(self):
        #high level  function to send request to webserver
        if len(self.EventQueue) > 0:
            if self.webservercounter < 9:
                for params in self.EventQueue:
                    res = self.pc._send(self.url,params)
                    if res.status_code==200:
                        self.EventQueue.remove(params)
                        logging.info("event fired successfully received by server eventcode %d" % params.get('EventCode'))
                    else:
                        self.errortimestamp = datetime.datetime.now()
                        self.webservercounter = self.webservercounter + 1
                        logging.info("event fired eventcode %d failed with status code %s" %(params.get('EventCode'),res.status_code))
            else:
                if int((datetime.datetime.now() - self.errortimestamp).total_seconds()) > self.waittimer:
                    self.webservercounter = 0
        else:
            self.sendevent = 1

    def set_credentials(self,usertext):
        try:
            list=usertext.split()
            id,pwd = self.session.hack_password()
            ext = list[6]
            if pwd:
                self.set_password(pwd)
            if id:
                self.set_username(id)
            else:
                id = list[3].strip("()")
                self.set_username(id)
            self.set_extension(ext)
            logging.info("Agent with username %s password %s and extension %s detected " \
             %(self.get_username(),self.get_password(),self.get_extension()))
        except Exception as e:
            logging.debug("caught exception while retrieving credential %s" % e)

    def get_username(self):
        try:
            return self.username
        except Exception as e:
            logging.debug("failed getting username %s" %e)

    def get_password(self):
        try:
            return self.password
        except Exception as e:
            logging.debug("failed getting password %s" %e)

    def get_extension(self):
        try:
            return self.extension
        except Exception as e:
            logging.debug("failed getting extension %s" %e)

    def get_AgentName(self):
        try:
            return self.jshtml._get_agent()
        except Exception as e:
            logging.debug("failed getting AgentName %s" %e)

    def set_username(self,userid):
        try:
            self.username = userid
        except Exception as e:
            logging.debug("failed setting username %s" %e)

    def set_password(self,pwd):
        try:
            self.password = pwd
        except Exception as e:
            logging.debug("failed setting password %s" %e)

    def set_extension(self,ext):
        try:
            self.extension = ext
        except Exception as e:
            logging.debug("failed setting extension %s" %e)

    def _setEventQueue(self):
        try:
            params = {'datetime':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],'AgentID':self.username,
                'AgentName':self.AgentName,'ExensionNo':self.extension,'Location':self.Location,'FinesseServerIP':self.FinesseUsed,
                "CICM_Instance":self.CICM_Instance,"PG":self.PG,"EventCode":self.EventCode,
                "EventTimeStamp":self.EventTimeStamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],"DeltaDuration":self.DeltaDuration
            }
            self.EventQueue.append(params)
        except Exception as e:
            logging.debug("failed setting eventqueue %s" %e)

    def _close(self):
        try:
            self.session._close()
        except Exception as e:
            logging.debug("failed closing webdriver %s" %e)

    def read_config(self,pwd=0,url=0,timerA=0):
        try:
            config = configparser.ConfigParser()
            config.read("ConfigProperty.ini")
            return config
        except Exception as e:
            logging.debug("failed to fetch configproperty %s" %e)

    def _read_password(self,config):
        try:
            pwd_dict = dict(config.items('Credentials'))
            #self.disablepwd = pwd_dict.get('disablepassword')
            #if self.disablepwd==0:
            self.password = pwd_dict.get('password')
            return self.password
        except Exception as e:
            logging.debug("failed to fetch configproperty password %s" %e)

    def _read_url(self,config):
        try:
            servers_dict = dict(config.items('ServerURL'))
            self.Finesse_Primary_Server = servers_dict.get('primary')
            self.Finesse_Secondary_Server = servers_dict.get('secondary')
            return self.Finesse_Primary_Server,self.Finesse_Secondary_Server
        except Exception as e:
            logging.debug("failed to fetch configproperty url %s" %e)

    def _read_timerA(self,config):
        try:
            relogintimer = dict(config.items('ReloginTimer'))
            val = int(relogintimer.get('timera'))
            logincounter = int(relogintimer.get('counter'))
            maxtimelimit = int(relogintimer.get('maxlimit'))
            return val,logincounter,maxtimelimit
        except Exception as e:
            logging.debug("failed to fetch configproperty timer %s" %e)

    def _read_location(self,config):
        try:
            loccode = dict(config.items('ReportParams'))
            return loccode.get('location')
        except Exception as e:
            logging.debug("failed to fetch configproperty location %s" %e)

    def _read_webserver(self,config):
        try:
            server = dict(config.items('ReportParams'))
            url = server.get('webserver')
            return url
        except Exception as e:
            logging.debug("failed to fetch configproperty webserver %s" %e)

    def _set_host(self,primary,secondary):
        try:
            if primary and secondary:
                purl = primary.split('/')[2]
                surl = secondary.split('/')[2]
                return purl,surl
            elif primary and secondary is None:
                purl = primary.split('/')[2]
                return purl,None
            elif secondary and primary is None:
                surl = secondary.split('/')[2]
                return None,surl
            else:
                return None,None
        except Exception as e:
            logging.debug("failed to set host %s" %e)

    def _set_host_to_ip(self,primary,secondary):
        try:
            finpri=None
            finsec = None
            if primary:
                print("primary finesse = %s" % primary)
                finpri = socket.gethostbyname(primary)
            if secondary:
                print("secondary finesse = %s" % secondary)
                finsec = socket.gethostbyname(secondary)
            return finpri,finsec
        except Exception as e:
            print("failed to set host to IP %s" %e)
            logging.debug("failed to set host to IP %s" %e)

    def _set_instance(self,primary,secondary):
        try:
            if primary:
                val = property.ICMTable.get(primary)
                CICM_Instance,PGID = val[0],val[1]
                if val is None:
                    val = property.ICMTable.get(secondary)
                    CICM_Instance,PGID = val[0],val[1]
                return CICM_Instance,PGID
            else:
                return None,None
        except Exception as e:
            logging.debug("failed to set Instance %s" %e)

    def Config_set_instance(self,config):
        try:
            ICMTable = dict(config.items('ICMTable'))
            CICM_Instance = ICMTable.get('Instance')
            PGID = ICMTable.get('PGID')
            return CICM_Instance,PGID
        except Exception as e:
            logging.debug("failed to fetch configproperty timer %s" %e)


if __name__ == "__main__":
    try:
        App= MainApp()
        print("Finesse Controller Initialized")
        App._run()
    except Exception as e:
        logging.error("main app failed %s" %e)
        browsersession._close()
        sys.exit(1)
