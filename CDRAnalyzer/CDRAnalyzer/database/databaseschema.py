"""
work in progress, not in use for now.

"""
#configuring schema class
from CDRAnalyzer.database import basedb as base
from CDRAnalyzer.settings import db_conf
from . import compiler

class schema(base.database):

    def __init__(self):
        super(schema,self).__init__()
        self.ds = compiler.BaseDatabaseSchemaEditor()

    def conf_db(self,dbname=None):
        sqlStatement = "CREATE DATABASE %s" % dbname
        self._new_db(sqlStatement)

    def conf_table(self,dbname=None,tbname=None,cols=None):
        sqlStatement = self.ds.create_table(dbname,tbname,cols)
        self._new_tb(sqlStatement)

    def conf_gen_tb(self,dbname,tbname,cols):
        placeholder = ", ".join(["%s"] * len(cols))
        sqlStatement = "insert into {db}.{table} ({columns}) values ({values});".format(db=dbname,table=tbname,
        columns=",".join(cols),values=placeholder)
        return sqlStatement

    def conf_insert_tb(self,sql,row):
        self._insert_tb(sql,row)
        self.con.commit()
    def conf_read_tb(self,dbname=None,tbname=None,params=[],where="",chunks=()):
        start,end = chunks
        if dbname and tbname and len(chunks) >0:
            sql = "select" + " " + ",".join(params) + " " + "from" + " " + \
            dbname.tbname + " " + where + " " + "and between recoverykey = " + str(start) +\
            "and recoverykey =" + str(end) + ";"
        else:
            #Default sql statement
            sql = '''select globalCallID_callId,callingPartyNumber,callingPartyNumber,dateTimeOrigination,
            dateTimeDisconnect,authCodeDescription from cdr_portal.cdr_main where
            length(authCodeDescription)>0 and authCodeDescription != 'Invalid Authorization Code'
            and recoverykey between %s and %s ;''' % (start,end)

        return self._read_tb(sql)

    def _read_count(self,sql):
        #use temporarily
        return self._read_tb(sql)

    def close(self):
        self._close()
