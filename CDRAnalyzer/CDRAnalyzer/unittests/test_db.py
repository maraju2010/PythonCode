#configure test to verify db class

import run
import time
from CDRAnalyzer.monitor import worker,pool
from threading import local
from CDRAnalyzer.settings import global_conf as conf
from CDRAnalyzer.settings import db_conf as db
from CDRAnalyzer.database import  schema
from CDRAnalyzer.database import basedb
import unittest
from datetime import datetime

class testdb(unittest.TestCase):
        def test_DB(self):
            res = conf.MON_PATH
            self.assertIsNotNone(res)

        #def test_conf_new_db(self):
        #    s=schema.schema()
        #    s.conf_db("CDR_Portal")

        #def test_conf_cdr_Table(self):
        #    s=schema.schema()
        #    print (s)
        #    s.conf_table(dbname="CDR_Portal",tbname="CDR_MAIN",cols=db.main_tb)

        #def test_conf_recovery_Table(self):
            #s=schema.schema()
            #print (s)
            #s.conf_table(dbname="CDR_Portal",tbname="recovery",cols=db.test_tb)

        #def test_report_db(self):
        #    s=schema.schema()
        #    start = 1
        #    end = 10
        #    while True:
        #        sql="select count(*) from cdr_portal.cdr_main where RecoveryKey between '{}'\
        #        and '{}';".format(start,end)
        #        print(a)
        #        end = end + 10
        #        print(str(datetime.now()))
                #time.sleep(2)



        #def test_csvdb(self):
        #    print (conf.DATABASES["ENGINE"])
        #    self.w=worker.Worker()
        #    fl=self.w._start()
        #    for f in fl:
        #        if f:
                    #send filename and table name
        #            worker._parser()._parse(f)

if __name__ == '__main__':
    unittest.main()
