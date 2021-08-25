import xml.etree.ElementTree as ET
from TeamObject  import TeamObject

class Layout(object):

    def __init__(self):
        self.TEAM_TABLE = []

    def _parse(self,xmlstring):
        try:
            count=0
            buffer={}
            Id=""
            e = ET.ElementTree(ET.fromstring(xmlstring))
            for elt in e.iter():
                if count==0 and elt.tag=="id":
                    Id=elt.text
                    buffer[Id]=[]
                    count=count+1
                if count==1 and elt.tag=="name":
                    buffer[Id].append(elt.text)
                    count=count+1
                if count==2 and elt.tag=="uri":
                    buffer[Id].append(elt.text)
                    URI = elt.text
                    Id=""
                    count=0
            return buffer

        except Exception as e:
            print("#### Exception while parsing layout %s " %(e))
