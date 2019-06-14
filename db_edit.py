# utility methods used to edit the DATA_SILSO_HISTO sql database
# for now it's just comments and flags

# import statements
import db_search

# not sure if needed
import db_connection
import mysql.connector

# takes cursor, id and comment, and adds the comment to the id number
# if there is already a comment, does not replace comment unless specified
# return boolean T if updated, F if there was already a comment
def comment(id_number,comment,cursor=None,mydb=None,replace=False):
    
    cursor,mydb=db_connection.get_cursor()
    
    query="SELECT COMMENT FROM DATA d WHERE d.ID="+str(id_number)
    cursor.execute(query,params=())
    original_comment=cursor.fetchall()[0][0]
    print("\noriginal_comment:",end="")
    print(original_comment)
    print("replacing comment:",comment)
    print()
    
    
    if original_comment=='' or replace==True:
        # update DATA and then show the update to user
        query="UPDATE DATA d SET COMMENT='%s' WHERE d.ID=%s"
        cursor.execute(query % (comment,str(id_number)))
        
        # check that you have properly updated it
        query="SELECT COMMENT FROM DATA d WHERE d.ID="+str(id_number)
        cursor.execute(query,())
        new_comment = cursor.fetchall()[0][0]
        if new_comment==comment:
            print("successfully updated the comment ")
        print("\nthe comment for ID="+str(id_number)+" has been",end=" ")
        if original_comment=='':
            print("added")
        else:
            print("over-written")
        # the all important last line, without this nothing is written to the database
        print("commit")
        mydb.commit()
        return True
        

    else:
        print("\nThe data point at ID="+str(id_number)+" already has",
             "a comment:",end="")
        print(original_comment)
        print("it was not replaced")
        return False
        
    

# takes id_number cursor and database connection and adds a flag to the data
def set_flag(id_number,cursor=None,mydb=None):
    cursor,mydb=db_connection.get_cursor(cursor,mydb)
    query="UPDATE DATA d SET FLAG=1 WHERE d.ID="+str(id_number)
    cursor.execute(query,())
    mydb.commit()
    print("ID:",id_number,"\tFLAG: 1")

# takes id_number cursor and database connection and sets flag to 0
def remove_flag(id_number,cursor=None,mydb=None):
    cursor,mydb=db_connection.get_cursor(cursor,mydb)
    query="UPDATE DATA d SET FLAG=0 WHERE d.ID="+str(id_number)
    cursor.execute(query,())
    mydb.commit()
    print("ID:",id_number,"\tFLAG: 0")
