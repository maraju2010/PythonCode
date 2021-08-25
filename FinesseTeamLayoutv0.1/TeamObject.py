import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.etree.ElementTree import Element,SubElement,Comment, tostring,ElementTree,XMLParser
from xml.sax.saxutils import escape,unescape
import os

class TeamObject(object):

    def __init__(self,finessePub,Id,Layout,TeamConfig=[]):
        #Team(Team,self.Tmp[Team],response.text)
        self.Id = Id
        self.Name=self.setName(TeamConfig[0])
        self.URI=self.setURI(TeamConfig[1])
        self.cuicSub = self.getFinesseSub(finessePub)
        count=0
        for i in TeamConfig:
            if count==0:
                self.Name = i
                count = count +1
            if count==1:
                self.URI = i
        self.Layout,self.systemlayout = self.__build(Layout)


    def __build(self,xmlstring):

        buffer = []
        AddTeamMessage = True
        RemoveChatMessage = False
        RemoveMakeCall = False
        RemoveIdentity = False

        chat="<url>/desktop/scripts/js/chat.component.js</url>"

        """ clean up xml string """
        cleanxml=self.xmlesc(xmlstring)

        """ Write to an output file"""
        #file_name = self.output_to_file(cleanxml)

        """ building xml body"""

        root =  ET.fromstring(cleanxml,parser=None)
        defaultvalue = root.find('useDefault').text
        finesselayout = root.find('.//{http://www.cisco.com/vtg/finesse}finesseLayout')
        ET.register_namespace('', "http://www.cisco.com/vtg/finesse")
        rightcol = finesselayout.find('.//{http://www.cisco.com/vtg/finesse}rightAlignedColumns')
        url = finesselayout.findall('.//{http://www.cisco.com/vtg/finesse}url')

        for i in url:
            if "teammessage.component.js" in i.text:
                AddTeamMessage = False
            if "chat.component.js" in i.text:
                RemoveChatMessage = True
            if "makenewcall.component.js" in i.text:
                RemoveMakeCall = True
            if "identity-component.js" in i.text:
                RemoveIdentity = True

        if RemoveChatMessage:
            rightsidecol = finesselayout.find(".//{http://www.cisco.com/vtg/finesse}rightAlignedColumns")
            headercolumn = rightsidecol.findall(".//{http://www.cisco.com/vtg/finesse}headercolumn")
            for headercol1 in headercolumn:
                component = headercol1.find('.//{http://www.cisco.com/vtg/finesse}component')
                url = component.find('.//{http://www.cisco.com/vtg/finesse}url')
                if "chat.component.js" in url.text:
                    headercol1.remove(component)
                    rightsidecol.remove(headercol1)

        if RemoveMakeCall:
            rightsidecol = finesselayout.find(".//{http://www.cisco.com/vtg/finesse}rightAlignedColumns")
            headercolumn = rightsidecol.findall(".//{http://www.cisco.com/vtg/finesse}headercolumn")
            for headercol1 in headercolumn:
                component = headercol1.find('.//{http://www.cisco.com/vtg/finesse}component')
                url = component.find('.//{http://www.cisco.com/vtg/finesse}url')
                if "makenewcall.component.js" in url.text:
                   headercol1.remove(component)
                   rightsidecol.remove(headercol1)

        if RemoveIdentity:
            rightsidecol = finesselayout.find(".//{http://www.cisco.com/vtg/finesse}rightAlignedColumns")
            headercolumn = rightsidecol.findall(".//{http://www.cisco.com/vtg/finesse}headercolumn")
            for headercol1 in headercolumn:
                component = headercol1.find('.//{http://www.cisco.com/vtg/finesse}component')
                url = component.find('.//{http://www.cisco.com/vtg/finesse}url')
                if "identity-component.js" in url.text:
                   headercol1.remove(component)
                   rightsidecol.remove(headercol1)


        if AddTeamMessage:
            #headercol = rightcol[0].insert(0,"headercolumn")
            headercol = SubElement(rightcol,"headercolumn")
            headercol.set("width","50px")
            component = SubElement(headercol,"component")
            component.set("id","broadcastmessagepopover")
            url = SubElement(component,"url")
            url.text="/desktop/scripts/js/teammessage.component.js"
            #ET.indent(headercol)

        """ work around to maitain the same order of xml elements"""
        if RemoveMakeCall:
            headercol = SubElement(rightcol,"headercolumn")
            headercol.set("width","50px")
            component = SubElement(headercol,"component")
            component.set("id","make-new-call-component")
            url = SubElement(component,"url")
            url.text="/desktop/scripts/js/makenewcall.component.js"
            #ET.indent(headercol)


        if RemoveIdentity:
            headercol = SubElement(rightcol,"headercolumn")
            headercol.set("width","72px")
            component = SubElement(headercol,"component")
            component.set("id","identity-component")
            url = SubElement(component,"url")
            url.text="/desktop/scripts/js/identity-component.js"
            #ET.indent(headercol)
            #self.pretty_xml(headercol,'\t','\n')


        gadgets = finesselayout.findall('.//{http://www.cisco.com/vtg/finesse}gadget')
        for gadget in gadgets:
            if "LiveDataGadget.jsp" in  gadget.text:
                gadget.set("alternateHosts",self.cuicSub)
            if "HistoricalGadget.jsp" in gadget.text:
                gadget.set("alternateHosts",self.cuicSub)
            if "QueueStatistics.jsp" in gadget.text:
                gadget.set("alternateHosts",self.cuicSub)


        ET.indent(finesselayout)
        newstring = tostring(finesselayout, encoding="unicode")
        #print(newstring)
        newroot = Element("TeamLayoutConfig")
        useDefault = SubElement(newroot,"useDefault")
        useDefault.text = defaultvalue
        layoutxml = SubElement(newroot,"layoutxml")
        layoutxml.text = newstring
        return(tostring(newroot, encoding="unicode"),defaultvalue)
        ## using lxml

    # the missing part:
    def parse_xml_with_remarks(self,filepath):
        ctb = CommentedTreeBuilder()
        xp = ET.XMLParser(target=ctb)
        tree = ET.parse(filepath, parser=xp)
        return tree

    def decodeNotification(self,xmlstring):
        """
            Decode the escaped characters (&lt; and &gt;)
            in order to convert it to an ElementTree
        """
        xml = xmlstring
        xml = xml.replace("&lt;", "<")
        xml = xml.replace("&gt;", ">")
        xml = xml.replace("&quot;","\"")
        xml = xml.replace("&amp;","&")
        xml = xml.replace("&apos;","\'")
        return xml

    def read_from_file(self):
        file_name = self.Id + ".txt"
        with open(file_name,"r") as f:
            reader = f.readlines()

    def xmlesc(self,txt):
        return unescape(txt, entities={"&lt;": "<","&gt;":">", "&apos;":"\'", "&quot;": "\""})

    def  setName(self,Name):
        return Name

    def setURI(self,URI):
        return URI

    def getFinesseSub(self,pub):
        """ return CUIC subscriber address to update alternateHosts """
        if pub=="FINESSE_SERVERA" or pub=="XX.XX.XX.XX":
            return "CUIC_ServerB"

        else:
            return "CUIC_SERVERB"
