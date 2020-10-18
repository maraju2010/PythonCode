import json
import datetime
import logging

ProjReq="""
#######################################################################################
#																					  #
#																					  #
#																					  #
#   Make API calls periodically to Endpoint and get stats,the stats must be analysed  #
#   and based on threshold generate alert to stakeholders.	  						  #
#																					  #
#																					  #
#######################################################################################

"""


"""
######################################################################
#    Default credentials for cisco endpoints. It will be invoked for #
#    phones without any Grp or if no credential found under          #
#     credentials table.                                          #
######################################################################
"""
Credentials = {
    "username":"admin",
    "password":"Manoj_IL"
}


"""
######################################################################
#    V specific credentials.                                       #
#    Format "GRPName":["Username,"Password"]                         #
######################################################################
"""

VCredentials = {

    "GRP1":["admin","Manoj_IL"],
    "GRP2":["admin","Manoj_111"]
}



"""
######################################################################
#    MailGrp table                                                   #
#                                                                    #
######################################################################
"""

Default_MailID = (
    "XXXX@yahoo.com"
)

MailID = {
    "MG1":"XXX@yahoo.com",
    "MG2":"XXXX@gmail.com"
}


"""
#########################################################################################
#    Table to store endpoint details.                                                   #
#    Format "IP Address":"Name of Endpoint","PriorityTag","Circle","CredentialsGroup",  #
#    "MailGrp","AlertMark","VCAlertMark"                                                #
#    0:send alert                                                                       #
#    1: do not send alert                                                               #
#                                                                                       #
#########################################################################################
"""

EndpointIP = {

"192.168.0.1":["Manoj Raju","USR","APR","GRP1","MG1","0"],
}


"""
#########################################################################################
#    set threshold value for packetloss and jitter, jitter is in ms and                 #
#    packet loss is count of packets,will be used for percent calculation.              #
#                                                                                       #
#########################################################################################
"""

Threshold = {
    "AUDIOPACKETLOSS":30, #unit is percent
    "VIDEOPACKETLOSS":30,
    "DUOVIDEOPACKETLOSS":30,
    "AUDIOJITTER":50, #unit is ms
    "VIDEOJITTER":50,
    "DATAJITTER":50,
    "CURAUDIOPACKETLOSS":10, #unit is percent
    "CURVIDEOPACKETLOSS":10,
    "CURDUOVIDEOPACKETLOSS":10
}


"""
#########################################################################################
#    set attributes- do not change this setting.Each attribute is segmented as incoming #
#    outgoing with loss and jitter                                                      #
#    attributetype:['losspacket','totalpacets']                                         #
#########################################################################################
"""

ATTRIBUTES = {
    #0:["INCOMINGAUDIOLOSS":["INCOMINGAUDIOPACKETS"],
    #1:["INCOMINGVIDEOLOSS":["INCOMINGVIDEOPACKETS"],
    #2:["INCOMINGDATALOSS":["INCOMINGDATAPACKETS"],
    #3:["OUTGOINGAUDIOLOSS":["OUTGOINGAUDIOPACKETS"],
    #4:["OUTGOINGVIDEOLOSS":["OUTGOINGAUDIOPACKETS"],
    #5:["OUTGOINGDATALOSS":["OUTGOINGDATAPACKETS"],
    6:["INCOMINGAUDIOJITTER","NULL"],
    7:["INCOMINGVIDEOJITTER","NULL"],
    8:["INCOMINGDATAJITTER","NULL"],
    9:["OUTGOINGAUDIOJITTER","NULL"],
    10:["OUTGOINGVIDEOJITTER","NULL"],
    11:["OUTGOINGDATAJITTER","NULL"],
    12:["INCOMINGAUDIOLASTINTERVALLOST","INCOMINGAUDIOLASTINTERVALRECEIVED"],
    13:["INCOMINGVIDEOLASTINTERVALLOST","INCOMINGVIDEOLASTINTERVALRECEIVED"],
    14:["INCOMINGDATALASTINTERVALLOST","INCOMINGDATALASTINTERVALRECEIVED"],
    15:["OUTGOINGAUDIOLASTINTERVALLOST","OUTGOINGAUDIOLASTINTERVALRECEIVED"],
    16:["OUTGOINGVIDEOLASTINTERVALLOST","OUTGOINGVIDEOLASTINTERVALRECEIVED"],
    17:["OUTGOINGDATALASTINTERVALLOST","OUTGOINGDATALASTINTERVALRECEIVED"]
    
}

"""
###################################################################################
#       set Type of attributes in call                                            #
#                                                                                 #
###################################################################################
"""

ATTRIBUTESTYPE = {
    0:"INAUDIO",
    1:"INVIDEO",
    2:"INDATA",
    3:"OUTAUDIO",
    4:"OUTVIDEO",
    5:"OUTDATA",
    6:"INAUDIOJITTER",
    7:"INVIDEOJITTER",
    8:"INDATAJITTER",
    9:"OUTAUDIOJITTER",
    10:"OUTVIDEOJITTER",
    11:"OUTDATAJITTER",
    12:"CURINAUDIO",
    13:"CURINVIDEO",
    14:"CURINDATA",
    15:"CUROUTAUDIO",
    16:"CUROUTVIDEO",
    17:"CUROUTDATA"
}


"""
###################################################################################
#      endpoint url, dummip to be replaced with actual ip while sending request  #
#                                                                                 #
###################################################################################
"""

EndpointURL = "http://dummyip/getxml?location=/Status/MediaChannels"

"""
###################################################################################
#     lst_check_MQ endpoint parameter will check the timelapse to poll in            #
#     Event Mode that have ActiveCalls.                                           #
#                                                                                 #
###################################################################################
"""

lst_check_MQendpoint = 20


"""
###################################################################################
#     lst_check_endpoint parameter will check the timelapse to poll working       #
#     devices in Poll Mode.                                                       #
#                                                                                 #
###################################################################################
"""

lst_check_endpoint = 40


"""
###################################################################################
#     lst_check_failedendpoint parameter will check the timelapse to poll failed  #
#     devices in Poll Mode.                                                       #
#                                                                                 #
###################################################################################
"""

lst_chk_failedendpoint = 600

"""
###################################################################################
#     Alert_MaxTime parameter will check the timelapse to send alerts again.      #
#                                                                                 #
###################################################################################
"""

Alert_MaxTime = 300

"""
###################################################################################
#     VCAlert_MaxTime parameter will determine the timelapse to send VCalerts .   #
#                                                                                 #
###################################################################################
"""

VCAlert_MaxTime = 900


"""
###################################################################################
#     to enable Tivoli logging set 1, either tivoli 0: disable, 1: enable.        #
#                                                                                 #
###################################################################################
"""
enableTivoli = 1
TivoliLogfilePath = "/var/log/tivolilog/ucmessages.out"
#TivoliLogfilePath = "ucmessages.out"

"""
###################################################################################
#    to enable file beat logging set 1, 0: disable, 1: enable.                    #
#                                                                                 #
###################################################################################
"""

enableFilebeat=0
FilebeatLogfilePath = "/var/log/filebeatmessages.out"


"""
###################################################################################
#    to enable SDL logging set 1: 0: disable, 1: enable.                          #
#                                                                                 #
###################################################################################
"""
enableSDL = 0

"""
###################################################################################
#    to enable VC alert logging set 1: 0: disable, 1: enable.                          #
#                                                                                 #
###################################################################################
"""

enableVC = 1

"""
###################################################################################
#    logging level                                                                #
#                                                                                 #
###################################################################################
"""

logginglevel = 0  # e.g 0:warning,1:error,2:critical,3:debug
debugpath = "ucmessages.out"

"""
###################################################################################
#    Not in use.                                                                  #
#                                                                                 #
###################################################################################
"""

Syslog = {
    "IP":"192.168.0.2",
    "PORT":514
}


"""
#####################################################################################
#    disable cause codes alert table.                                              #
#    format #causecode : FLAG( 0 for send alert,1 for do not send alert)           #                                                   #
######################################################################################
"""

disablecausecodes = {
    0:1,
    16:1
}

"""
#####################################################################################
#    Enable  Logging to Linux Journal Files                                         #
#    format #Level : INFO or DEBU                                                   #
######################################################################################
"""

journallog = "DEBUG"

#log file properties
#example INFO= logging.INFO,DEBUG = logging.DEBUG
filename = '/var/log/ucmonapplog/ucmonapp.log'
loglevel=logging.DEBUG
logsize = 50000
count = 10
