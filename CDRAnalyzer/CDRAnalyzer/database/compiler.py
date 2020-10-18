"""
work in progress not in use for now.
"""

class BaseDatabaseSchemaEditor:

    def __init__(self):
        self.sql_create_table = "CREATE TABLE %(db)s.%(table)s (%(definition)s);"

#column_sqls.append("%s %s" % (
            #    self.quote_name(field.column),
#                definition,
#            ))
    def create_table(self,dbname,tbname,cols):
        column_sqls = [cols]

        return self.sql_create_table % {
        "db":dbname,
        "table":tbname,
        "definition":", ".join(column_sqls)
        }
