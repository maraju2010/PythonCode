import xml.etree.ElementTree as ET
import datetime
import prop

class xmlparser(object):

    def __init__(self,logger):
        ### create instance of object
        self.logging = logger

    def  getdevice(self,snapshotxmlPath):
        ###############################################################################
        #########################   func to parse remote device ID  ##################
        ###############################################################################
        try:
            inputDataXML = ET.fromstring(snapshotxmlPath)
            bodies = inputDataXML.findall(".//Call")
            for param in bodies:
                #rdevice=param.find(".//RemoteNumber").text
                tempdevice=param.find(".//RemoteNumber").text
                if "@" in tempdevice:
                    rdevice,ch=tempdevice.split("@")
                else:
                    rdevice=tempdevice
            return rdevice
        except Exception as e:
            self.logging.info("caught exception %s" %  e)

    def  xmlparser(self,snapshot):

        ###############################################################################
        #########################   func to parse xml message  ##################
        ###############################################################################
        try:
            root = ET.fromstring(snapshot)
            #root=tree.Element.getroot()
            bodies=root.findall(".//Call")
            xmldict=[]
            i=0
            for call in bodies:
                cl=call.attrib
                callID=cl["item"]
                d={}
                for channel in call:
                    channelno=channel.attrib
                    channelID=channelno["item"]
                    leg=channel.find(".//Direction").text
                    Type=channel.find(".//Type").text

                    if Type=="Video":
                        i=i+1
                        if (i==1 or i==2):
                            channeltag=leg + Type  + "channelid"
                            d[channeltag]=channelID
                        else:
                            pass
                    else:
                        channeltag=leg + Type + "channelid"
                        d[channeltag]=channelID

                    for child in channel:
                        if child.tag=="Netstat" or child.tag=="Audio" or \
                        child.tag=="Video" or child.tag=="Data":
                            if Type=="Video":
                                if (i==1 or i==2):
                                    for sub in child:
                                        finaltag=leg+ Type  + sub.tag
                                        d[finaltag]=sub.text
                            else:
                                for sub in child:
                                    finaltag=leg+ Type  + sub.tag
                                    d[finaltag]=sub.text

                        elif child.tag.strip(" ") == "\n":
                            pass
                        else:
                            finaltag=leg + Type + child.tag
                            d[finaltag]=child.text

                d["callID"]=callID
                xmldict.append(d)

            return self.settoCapitalize(xmldict)
        except Exception as e:
            self.logging.info("caught exception %s" % e)

    def settoCapitalize(self,xmldict):
            try:
                capxmldict = {k.upper(): v for k,v in xmldict[0].iteritems()}
                if prop.journallog=="DEBUG":
                    self.logging.debug("xml dict %s" % capxmldict)
                return capxmldict
            except Exception as e:
                self.logging.info("caught exception %s" %  e)
