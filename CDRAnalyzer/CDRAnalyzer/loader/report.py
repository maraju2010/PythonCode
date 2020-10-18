"""
    module to generate reports of suspicious authcodes.
"""
from CDRAnalyzer.settings import db_conf as db
from CDRAnalyzer.settings import global_conf as conf
from CDRAnalyzer.database import schema

class Report(schema.schema):

    def __init__(self):
        super(Report,self).__init__()
        self.path = conf.MON_PATH
        self.cols = self._create_column
        self.stmt = self.conf_gen_tb(dbname="CDR_Portal",tbname="report",cols=self.cols)
        print (self.stmt)

    def _gen_report(self,row):
        self.conf_insert_tb(self.stmt,row)

    @property
    def _create_column(self):
        cols = []
        for f in (db.report_tb).split(","):
            s= f.partition(" ")
            k=s[2].split(" ")
            if "PRIMARY" in k:
                pass
            elif "AUTO_INCREMENT" in k:
                pass
            elif "ID" in k:
                pass
            else:
                cols.append(k[3])
        return cols
