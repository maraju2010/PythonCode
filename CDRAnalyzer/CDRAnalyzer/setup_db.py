import sys
sys.path.append('C:/Users/manoraju/Desktop/pythonweb-app/pythonconfigure-karthik/CPO/updated/')
from CDRAnalyzer.settings import global_conf as conf
from CDRAnalyzer.settings import db_conf as db
from CDRAnalyzer.database import  schema


Tables = {"cdr_main":db.main_tb,"recovery":db.recovery_tb,"report":db.report_tb}

def conf_new_db():
    s=schema.schema()
    s.conf_db("CDR_Portal")

def conf_new_table():
    for key,values in Tables.items():
        s=schema.schema()
        s.conf_table(dbname="cdr_portal",tbname=key,cols=values)

if __name__  == "__main__":

    try:
        conf_new_db()
        conf_new_table()

    except Exception as e:
        print("Exeception occured:{}".format(e))
