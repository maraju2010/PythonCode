import xml.etree.ElementTree as ET

class xmlparser(object):
    def __init__(self):
        pass

    def _parse(self,xmlstring):
        causecode=0
        try:
            inputDataXML = ET.fromstring(xmlstring)
            print(inputDataXML)
            AgentState=inputDataXML.find(".//state").text
            print(AgentState)
            if AgentState=="LOGOUT":
                causecode=inputDataXML.find(".//reasonCodeId").text
            if AgentState=="NOT_READY":
                try:
                    causecode=inputDataXML.find(".//reasonCodeId").text
                except Exception as e:
                    print(e)
            if AgentState=="READY":
                causecode=inputDataXML.find(".//reasonCodeId").text
            print(causecode)
            return AgentState,causecode
        except Exception as e:
            print(e)
