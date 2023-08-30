import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        # the user and password created and modified as ncessary
        connection = pymysql.connect(host = 'localhost', 
                                    user = 'root', 
                                    password = 'guitarblue4145A!', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        # begin connection to the database
        self.connection = connection
    # this is to connect the correct queries to the correct 
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # INSERT queries automatically generate the ID NUMBER of each row
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data filtered by the statement(s) and thurn it into a List Of Dictionaries
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries must only change or delete.  Nothing else!
                    self.connection.commit()
            except Exception as e:
                # failed queries should return false instead of crashing the site
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 
# connectToMySQL takes the database from MySQL to create an instance of MySQLConnection to automatically import to the page
def connectToMySQL(db):
    return MySQLConnection(db)