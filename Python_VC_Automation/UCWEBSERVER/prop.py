import json
import socket
import logging

ProjReq="""
#######################################################################################
#																					  #
#																					  #
#																					  #
#   Make API calls periodically to register feedback hooks on enddevices.	  						  #
#																					  #
#																					  #
#######################################################################################

"""
Credentials = {
    "username":"admin",
    "password":"admin"
}

EndpointIP = {
    "IP1":["192.168.0.1","Manoj Center"],

}


EndpointURL = "http://dummyip/getxml?location=/Status/MediaChannels"

#WebServerIP = socket.gethostbyname(socket.gethostname())
WebServerIP = "192.168.0.1"
Port = 8080

#log file properties
#example INFO= logging.INFO,DEBUG = logging.DEBUG
filename = '/var/log/webserverlog/webapp.log'
loglevel=logging.INFO
