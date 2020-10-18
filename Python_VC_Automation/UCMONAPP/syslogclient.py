import logging
import logging.handlers
import prop
import datetime
import logging


'''
    class to create syslog handler and send messages to tivoli or filebeat agent.
'''

class syslog(object):
    def __init__(self,logger):
        #initialise emtpy syslog object
        self.logging = logger

    def createhandler(self,LoggerName=None,LoggerLevel=None,LogFileName=None,Handler=None):
        """This class creates syslog handler"""
        try:
            if LoggerName:
                my_logger = logging.getLogger(LoggerName)
                level = self.__getlevel(LoggerLevel)
                my_logger.setLevel(level)
                Handler = logging.FileHandler(LogFileName)
                Handler.setLevel(level)
                my_logger.addHandler(Handler)
                return my_logger
            else:
                 pass
        except Exception as e:
            self.logging.info("caught exception %s" %  e)

    def __getlevel(self,LoggerLevel):
        """
        Level	Numeric value
        CRITICAL	50
        ERROR	40
        WARNING	30
        INFO	20
        DEBUG	10
        NOTSET	0
        """
        LogLevel = self.__capitalize(LoggerLevel)
        if LogLevel=="INFO":
            return logging.INFO
        if LogLevel=="DEBUG":
            return logging.debug
        if LogLevel=="WARNING":
            return logging.warn
        if LogLevel=="ERROR":
            return logging.error
        if LogLevel=="CRITICAL":
            return logging.critical
        else:
            return None

    def __capitalize(self,word):
        return word.upper()

    def sendalert(self,msglist,desc,logger,ipaddr,priority,circle):
        #function will loop the list and generate alerts
        d={}
        if prop.journallog=="DEBUG":
            self.logging.debug("send syslog message to tivoli %s" % msglist)
        for row,val in enumerate(msglist):
            d=msglist[row][0]
            if prop.journallog=="DEBUG":
                self.logging.debug("filtered msg dict %s" % d)
            for key,val in d.items():
                if "JITTER" in key:
                    logger.info("%s-%s %s: %s of %1.2f ms observed for attribute %s at endpoint:%s-%s" \
                    %(priority,circle,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"JITTER",val,key,desc,ipaddr))
                else:
                    logger.info("%s-%s %s: Packet %s Percent of %1.2f  observed for attribute %s at endpoint:%s-%s" \
                    %(priority,circle,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"LOSS",val,key,desc,ipaddr))
                self.logging.info(" message sent to tivoli")

    def sendmsg(self,msg,logger):
        if prop.journallog=="DEBUG":
            self.logging.debug("send message to third party app %s" % msg)
        if logger:
            logger.info(msg)
