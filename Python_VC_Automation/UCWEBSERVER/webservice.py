try:
    from http.server import HTTPServer,BaseHTTPRequestHandler
    from socketserver import ThreadingMixIn
except ImportError:
    try:
        from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
        from SocketServer import ThreadingMixIn
    except ImportError as e:
        print ("caught exception %s" %e)

import xml.etree.ElementTree as ET
import io
import threading
import mqsend
import io
import time
import prop
import re
import logging
from logging.handlers import RotatingFileHandler

logfile = prop.filename
loglevel = prop.loglevel
logger = logging.getLogger(__name__)
logger.setLevel(loglevel)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              logfile, maxBytes=10000, backupCount=10)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(lineno)d- %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

mq = mqsend.MQService(logger)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        try:
            data = self._parse(body)
            logger.info("data parsed webserver %s - %s" % (str(data),body))
            if data is None:
                pass
            else:
                mq._run(data)
        except Exception as e:
            logger.info(e)
        self.send_response(200)
        self.end_headers()
        return

    def _parse(self,snapshot):
        xmlstring = re.sub(' xmlns="[^"]+"', '', snapshot, count=1)
        root = ET.fromstring(xmlstring)
        if len(root.findall(".//CallDisconnect"))>0:
            body1 = root.findall(".//CallDisconnect")
            body2 = root.findall(".//Identification")
            dst = None
            src=None
            descr=None
            CallType = None
            Direction = None
            CauseCode = None
            CauseType = None

            for param in body1:
                 dst = param.find(".//RemoteURI").text
                 CallType = param.find(".//CallType").text
                 Direction = param.find(".//OrigCallDirection").text
                 CauseCode = param.find(".//CauseCode").text
                 CauseType = param.find(".//CauseType").text

            for param in body2:
                 src = param.find(".//IPAddress").text
                 descr = param.find(".//SystemName").text if param.find(".//SystemName").text is not None else "Unknown"

            return "Queue=" + "UCMONQUEUE" + ","+ "Event=" + "Disconnect" + "," + "dst=" + dst + ","\
            +"src=" + src + "," + "descr=" + descr + "," + "CallType=" + CallType + "," \
            + "Direction=" + Direction + ","+ "CauseCode=" + CauseCode + "," +\
             "CauseType=" + CauseType

        if len(root.findall(".//CallSuccessful"))>0:
            body1 = root.findall(".//CallSuccessful")
            body2 = root.findall(".//Identification")
            for param in body1:
                dst = param.find(".//RemoteURI").text
                Direction = param.find(".//Direction").text

            for param in body2:
                src = param.find(".//IPAddress").text
                descr = param.find(".//SystemName").text if param.find(".//SystemName").text is not None else "Unknown"
            return  "Queue=" + "UCMONQUEUE" + "," + "Event=" + "Success" + "," +\
             "dst=" + dst + ","+"src=" + src + "," +  "descr=" + descr +"," +\
              "Direction=" + Direction
        else:
            logger.info("not found in body either calldisconnect or success event")
            pass

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def main():

    server = ThreadedHTTPServer((prop.WebServerIP,prop.Port),SimpleHTTPRequestHandler)
    t1 = threading.Thread(target=server,args=server.serve_forever())
    t1.setDaemon(True)
    t1.start()

if __name__ == "__main__":
    main()
