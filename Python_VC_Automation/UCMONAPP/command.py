import requests
import time
import datetime
#from axl1 import axl
import prop
from xml.etree.ElementTree import Element, SubElement, Comment,ElementTree
from xml.etree import ElementTree as ST
from xml.dom import minidom

class commands(object):

    def __init__(self,res):
        self.response=res.text
        self.status=res.status_code

    @classmethod
    def postrequest(cls,ipaddr,username,password,message):

        codec_username=username
        codec_password=password
        codec_ip=ipaddr
        headers={"content-type":"text/xml"}
        body=commands.convertdatatoxml(message)
        #from xml.etree.ElementTree import ElementTree as ET
        session=requests.Session()
        session.trust_env=False
        try:
            res=session.post("http://" + ipaddr + "/putxml",
            headers=headers,auth=(username,password),data=body,timeout=2)
            res.close()
            return cls(res)
        except Exception as e:
            return e

    @staticmethod
    def convertdatatoxml(message):
        root=Element("Command")
        child1=SubElement(root,"UserInterface")
        child2=SubElement(child1,"Message")
        child3=SubElement(child2,"Alert")
        child4=SubElement(child3,"Display",{"command":"True"})
        #child5=SubElement(child4,"Title")
        #child5.text="Alert from UCMON Tool"
        child6=SubElement(child4,"Text")
        child6.text=message
        child7=SubElement(child4,"Duration")
        child7.text="30"
        xmldata=commands.prettify(root)
        return xmldata

    @staticmethod
    def prettify(elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ST.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

if __name__ == "__main__":
        a= commands.postrequest("192.168.0.1","admin","Manoj_IL","This is a test")
        if a:
            print(a.response)
