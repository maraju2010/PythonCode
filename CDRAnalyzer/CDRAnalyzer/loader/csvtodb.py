"""
module to convert csv to db.

"""

import csv
from CDRAnalyzer.database import schema
from CDRAnalyzer.settings import global_conf as conf
from CDRAnalyzer.settings import db_conf as cols

class to_db(schema.schema):

    def __init__(self):
        super(to_db,self).__init__()
        self.path = conf.MON_PATH

    def read_fp(self,fp=None,tb=None,db=None):
        self.tbname = tb
        self.dbname = db
        self.fp = self.path + fp
        with open(self.fp) as csvfile:
            dt = self._get_col_datatypes(csvfile)
            csvfile.seek(0)
            self.reader = csv.DictReader(csvfile)
            fields = self.reader.fieldnames
            cols = []
            #set field and type
            for f in fields:
                cols.append("%s" % f)
            #csvfile.seek(0)
            #generate insert statement
            sqlStatement = self.conf_gen_tb(self.dbname,self.tbname,cols)
            for data in self.reader:
                self._insert_tb(sqlStatement,data)
            self.con.commit()

    @staticmethod
    def _get_col_datatypes(csvfile):
        dr = csv.DictReader(csvfile)
        fieldTypes = {}
        for entry in dr:
            print (entry)
            fieldslLeft = [f for f in dr.fieldnames if f not in fieldTypes.keys()]
            if not fieldslLeft: break
            for field in fieldslLeft:
                data = entry[field]
                if data.isdigit():
                    fieldTypes[field] = "INT"
                elif "date" in field:
                    fieldTypes[field] = 'BIGINT'
                else:
                    fieldTypes[field] = "TEXT"
        return fieldTypes
