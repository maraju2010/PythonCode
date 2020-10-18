import json
import socket
import datetime
import logging

ProjReq="""
#######################################################################################
#																					  #
#																					  #
#																					  #
#   Make API calls periodically to Endpoint.	  						  #
#																					  #
#																					  #
#######################################################################################

"""

Credentials = {
    "username":"admin",
    "password":"Manoj_IL"
}

VCredentials = {
    #Format "GRPName":["Username,"Password"]
    "GRP1":["admin","Manoj_IL"],
    "GRP2":["admin","Manoj_111"]
}


EndpointIP = {
    #Format "IP Address":["Name of Endpoint","PriorityTag","Circle","CredentialsGroup","MAILGRP","ALERT"]

"192.168.0.1":["Manoj Raju","USR","APR","GRP1","MG1","0"],
}

#ServerIP = socket.gethostbyname(socket.gethostname())
ServerIP = "192.168.0.2"

journallog="DEBUG"

#log file properties
#example INFO= logging.INFO,DEBUG = logging.DEBUG
filename = '/var/log/registerapplog/registerapp.log'
loglevel=logging.INFO
logsize = 50000
count = 10
