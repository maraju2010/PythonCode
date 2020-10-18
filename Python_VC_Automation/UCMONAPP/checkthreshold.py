from __future__ import division
import prop
import syslogclient
import datetime
import logging

'''
    class to check if values returned from phone are greater than threshold defined in property file.

'''
class checkthreshold(object):

    def __init__(self,logger):
        self.logging = logger

    def calculateloss(self,arg1,arg2):
        '''
            function to check packet loss.
        '''
        try:
            if int(arg1)==0:
                    losspercent=0
            else:
                if int(arg1)<=int(arg2):
                    losspercent=int(arg1)/int(arg2)*100
                else:
                    losspercent=0
            return losspercent
        except Exception as e:
            self.logging.info(e)

    def checkthreshold(self,arg1,type):
        '''
            Initialize sysloglist and validate the threshold check, if value is greater than threshold
            then write to sysloglist e.g [(INAUDIO:10)]
        '''
        if prop.journallog=="DEBUG":
            self.logging.debug("check threshold with arg1 and type")
        sysloglist = []
        arg1 = int(arg1)
        if prop.ATTRIBUTESTYPE.get(type)=="INAUDIO" or prop.ATTRIBUTESTYPE.get(type)=="OUTAUDIO":
            if arg1 > prop.Threshold.get("AUDIOPACKETLOSS",5):
                    sysloglist.append({prop.ATTRIBUTESTYPE.get(type):arg1})
        elif prop.ATTRIBUTESTYPE.get(type)=="INVIDEO" or prop.ATTRIBUTESTYPE.get(type)=="OUTVIDEO":
            if arg1 > prop.Threshold.get("VIDEOPACKETLOSS",5):
                    sysloglist.append({prop.ATTRIBUTESTYPE.get(type):arg1})
        elif prop.ATTRIBUTESTYPE.get(type)=="INDATA" or prop.ATTRIBUTESTYPE.get(type)=="OUTDATA":
            if arg1 > prop.Threshold.get("DUOVIDEOPACKETLOSS",5):
                    sysloglist.append({prop.ATTRIBUTESTYPE.get(type):arg1})
        elif prop.ATTRIBUTESTYPE.get(type)=="INAUDIOJITTER" or prop.ATTRIBUTESTYPE.get(type)=="OUTAUDIOJITTER":
            if  arg1 > prop.Threshold.get("AUDIOJITTER",5):
                    sysloglist.append({prop.ATTRIBUTESTYPE.get(type):arg1})
        elif  prop.ATTRIBUTESTYPE.get(type)=="INVIDEOJITTER" or prop.ATTRIBUTESTYPE.get(type)=="OUTVIDEOJITTER":
            if arg1 > prop.Threshold.get("VIDEOJITTER",5):
                    sysloglist.append({prop.ATTRIBUTESTYPE.get(type):arg1})
        elif prop.ATTRIBUTESTYPE.get(type)=="INDATAJITTER" or prop.ATTRIBUTESTYPE.get(type)=="OUTDATAJITTER":
            if arg1 > prop.Threshold.get("DATAJITTER",5):
                    sysloglist.append({prop.ATTRIBUTESTYPE.get(type):arg1})
        elif prop.ATTRIBUTESTYPE.get(type)=="CURINAUDIO" or prop.ATTRIBUTESTYPE.get(type)=="CUROUTAUDIO":
            if arg1 > prop.Threshold.get("CURAUDIOPACKETLOSS",5):
                    sysloglist.append({prop.ATTRIBUTESTYPE.get(type):arg1})
        elif prop.ATTRIBUTESTYPE.get(type)=="CURINVIDEO" or prop.ATTRIBUTESTYPE.get(type)=="CUROUTVIDEO":
            if arg1 > prop.Threshold.get("CURVIDEOPACKETLOSS",5):
                    sysloglist.append({prop.ATTRIBUTESTYPE.get(type):arg1})
        elif prop.ATTRIBUTESTYPE.get(type)=="CURINDATA" or prop.ATTRIBUTESTYPE.get(type)=="CUROUTDATA":
                if arg1 > prop.Threshold.get("CURDUOVIDEOPACKETLOSS",5):
                        sysloglist.append({prop.ATTRIBUTESTYPE.get(type):arg1})
        else:
            pass
        return sysloglist
