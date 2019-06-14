# utility methods used to access the DATA_SILSO_HISTO sql database


# import statements

import numpy as np
import mysql.connector

# this function connects you to the database
def database_connector(the_host="localhost",the_user="root",the_database="DATA_SILSO_HISTO",the_password=None):
    import mysql
    try:
        mydb = mysql.connector.connect(
            host=the_host,
            user=the_user,
            database=the_database
            )

        cursor=mydb.cursor()
        print("\nmysql connection successfully established...")
        return cursor,mydb

    except Exception as e:
        print("\nAn error has occured connecting to mysql database")
        print(e)
        #raise Exception(e)

# checks if you are connected and have a cursor if not it connects you
def get_cursor(cursor=None,mydb=None):
    
    if not cursor and not mydb:
        cursor,mydb = database_connector()
    elif not cursor:
        cursor=mydb.cursor()
    return cursor,mydb

# closes the database connection
def close_database_connection(mydb):
    if mydb.is_connected():
        mydb.close()
        print("Closing MySQL connection...")
    else:
        print("Error,",mydb,"\nwas not connected, why are you closing it?")

# returns string with header of DATA
def header():
    return "ID ; DATE ; FK_RUBRICS ; FK_OBSERVERS ; GROUPS ; SUNSPOTS ; WOLF ; QUALITY ; DATE_INSERT ; COMMENT "

### testing
#cursor,mydb=database_connector()