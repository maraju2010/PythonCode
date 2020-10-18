"""
    function to send authcode string using request library.
"""
import requests
import json
from CDRAnalyzer.settings import global_conf as conf

def _data(msg):
    url = conf.url
    payload = msg
    headers = {'content-type':'application/json'}
    try:
        r = requests.post(url,data=json.dumps(payload),headers=headers)
    except Exception as e:
        print("Exeception occured:{}".format(e))
