import prop
import requests
import datetime

class xml_api(object):
    '''
    This class is written using class method. Class method is invoked first and sends request to endpoint
    and fetches the response and then __init__ is called by class itself to create object instance
    and instance variable

    It sends http request to phone and retrieves response.

    '''

    def __init__(self,res):      
        self.response=res.text

    @classmethod
    def getrequest(cls,ipaddr,username,password,req="True"):
        codec_username=username
        codec_password=password
        url=prop.EndpointURL
        headers={"content-type":"text/xml"}
        session=requests.Session()
        session.trust_env=False
        if req=="True":
            try:
                res=session.get(url.replace("dummyip",ipaddr),headers=headers,
                auth=(codec_username,codec_password),timeout=2)
                res.close()
                return cls(res)
            except Exception as e:
                return e
        else:
            try:
                res=session.get("http://" + ipaddr + "/getxml?location=/Status/Call",
                headers=headers,auth=(codec_username,codec_password),timeout=2)
                res.close()
                return cls(res)
            except Exception as e:
                return e
