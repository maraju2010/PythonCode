"""
main interface to SQL DB.

"""

from CDRAnalyzer.settings import global_conf as conf
from CDRAnalyzer.database import schema
from CDRAnalyzer.util.exceptions import ImproperlyConfigured,generalerror
from CDRAnalyzer.util import general as _util
import pymysql


class database(object):

    def __init__(self):
        #configure __init__ to initialize variables
        self.db_vendor = _util._strtranslate(conf.DATABASES["ENGINE"])
        #self.db = conf.database
        self.dbhost = conf.HOST
        self.user = conf.user
        self.pwd = conf.password
        self.charSet = conf.charSet
        self.cursorclass = conf.cursorType

        if self.db_vendor == "mysqldb":
            try:
                self.con = pymysql.connect(host=self.dbhost, #host
                                        user=self.user, #username
                                        passwd=self.pwd,#password
                                        charset=self.charSet,
                                        cursorclass=self.cursorclass)  #

                self.cur = self.con.cursor()

            except Exception as e:
                print("Exeception occured:{}".format(e))

        else:
            raise ImproperlyConfigured("conf.DATABASES is not configured properly")

    def _gen_db(self):
        #configure this function to insert data into db
        self.cur.executemany(stmt,self.reader)
        self.con.commit()

    def _new_db(self,sql):
        #configure this function to create new db
        try:
            self.cur.execute(sql)
        except Exception as e:
            print("Exeception occured:{}".format(e))
        finally:
            self.con.close()

    def _new_tb(self,sql):
        #configure this function to create new table
        try:
            self.cur.execute(sql)
        except Exception as e:
            print("Exeception occured:{}".format(e))
        finally:
            self.con.close()

    def _insert_tb(self,sql,row):
        #configure this function to insert rows into table
        if type(row)==tuple:
            try:
                self.cur.execute(sql,row)
            except Exception as e:
                print("Exeception occured:{}".format(e))
        else:
            try:
                self.cur.execute(sql,list(row.values()))
            except Exception as e:
                print("Exeception occured:{}".format(e))


    def _read_tb(self,sql):
        # read data from db
        try:
            self.cur.execute(sql)
            self.con.commit()
            return self.cur.fetchall()
        except Exception as e:
            print("Exeception occured:{}".format(e))

    def _delete_tb(self,sql):
        #configure this function to delete table
        pass

    def _delete_db(self,sql):
        #configure this function to delete database
        pass

    def _close(self):
        #configure this function to close existing database connection
        self.con.close()
