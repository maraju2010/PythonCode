""""
    module reads from sql DB in chunks  and anaylses authcode usage.
    maxtime and maxcount are used to filter authcodes.
"""

import time
import asyncio
from datetime import datetime
from CDRAnalyzer.database import schema
from CDRAnalyzer.util import send as _send
from CDRAnalyzer.settings import global_conf as conf
from CDRAnalyzer.settings import db_conf as db
from CDRAnalyzer.util.exceptions import ImproperlyConfigured
from CDRAnalyzer.loader.report import Report

class auth_code_sn(object):

    def __init__(self):
        self.s = schema.schema()
        self.r = Report()
        self.used_list = []
        self.startchunk = conf.startchunk  # min read from db
        self.endchunk = conf.endchunk    #max read from db
        self.maxchunk = 0

    async def _analyse(self):
        ph = 0      #variable to fetch latest authcode  from used_list
        fh = 0      # variable to fetch 1st authcode from used_list
        count = 0   #counter
        maxcount = conf.maxcount  # read from global conf
        maxtime = conf.maxtime   # read from global conf
        self.startchunk,self.endchunk = self._get_chunk
        try:
            while True:
                self.maxchunk = self._get_maxchunk(conf.defaultquery)
                if self.endchunk < (self.maxchunk if self.maxchunk > 0 else conf.defaultchunk):
                    print("algo loop started %s" % str(datetime.now()))
                    rows = self.s.conf_read_tb(chunks=(self.startchunk,self.endchunk))
                    self.startchunk = self.endchunk + 1
                    self.endchunk = self.startchunk + 1000
                    for row in rows:
                        authcode = row["authCodeDescription"] #fetch authcode
                        t1 = datetime.fromtimestamp(row["dateTimeOrigination"]) #fetch timestamp
                        callingPartyNumber = row["callingPartyNumber"]
                        callId = row["globalCallID_callId"]
                        for index,i in enumerate(self.used_list):
                            if authcode in i:
                                ph = index      #set latestrow
                                count +=1
                                if count == 1:
                                    fh = index  #set firstrow
                        if count == 0:
                            self.used_list.append({authcode:t1})
                        else:
                            #total no of count is greater than configured
                            if count > maxcount:
                                t2 = self.used_list[ph][authcode]
                                diff_time =  t1 - t2
                                if 0 < (diff_time.total_seconds()/60) < maxtime:
                                        print("diff reached here")
                                        self._parse_data(callId,diff_time,authcode,callingPartyNumber)
                                        self._gen_report(row)
                                else:
                                    del self.used_list[fh]
                            else:
                                self.used_list.append({authcode:t1})

                        count = 0
                        fh=0
                        ph=0


                else:
                    print("self.endchunk: %s < self.maxchunk:%s @%s" % (self.endchunk,self.maxchunk,\
                    str(datetime.now())))
                await asyncio.sleep(20)
        except Exception as e:
            print("Exeception occured:{}".format(e))
            if self.maxchunk == 0:
                pass
            else:
                self._handle_exception()

    def _get_maxchunk(self,query):
        maxchunk = self.s._read_count(query)
        return maxchunk[0]["count(*)"]

    @property
    def _get_chunk(self):
        query="select startRecoveryKey,endRecoveryKey FROM cdr_portal.recovery where ID=(select max(ID) from \
        cdr_portal.recovery);"
        qn = self.s._read_count(query)
        if len(qn)>0:
            return self.s._read_count(query)[0].values()
        else:
            return (self.startchunk,self.endchunk)

    def _handle_exception(self):
        cols =["startRecoveryKey","endRecoveryKey","status"]
        sqlStatement = self.s.conf_gen_tb("cdr_portal","recovery",cols)
        data = (self.startchunk,self.endchunk,"R")
        self.s.conf_insert_tb(sqlStatement,data)

    def _parse_data(self,*args):
        msg = str(args[0]) + " " + str(args[1]) + " " + str(args[2]) + " " + str(args[3])
        self._send_data(msg)

    @staticmethod
    def _send_data(msg):
        if msg:
            _send._data(msg)
        else:
            raise ImproperlyConfigured("msg is invalid %s" % msg)


    def _gen_report(self,row):
            sqlrow=[]
            datacol = self._getlist()
            for i in datacol:
                if "maxtime" in i:
                    sqlrow.append(conf.maxtime)
                elif "maxcount" in i:
                    sqlrow.append(conf.maxcount)
                else:
                    sqlrow.append(row[i])
            try:
                self.r._gen_report(tuple(sqlrow))
            except Exception as e:
                print("Exeception occured:{}".format(e))

    def recovery_close(self):
        if self.maxchunk == 0:
            pass
        else:
            self._handle_exception()
        self.s.close()

    def _getlist(self):
        return ("dateTimeOrigination","dateTimeDisconnect","globalCallID_callId",
        "callingPartyNumber","finalCalledPartyNumber","authCodeDescription","maxtime","maxcount")
