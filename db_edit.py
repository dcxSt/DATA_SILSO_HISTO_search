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
def set_comment(id_number,comment,cursor=None,mydb=None,replace=False):
    
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
def set_flag(id_number,cursor=None,mydb=None,close_connection=True):
    cursor,mydb=db_connection.get_cursor(cursor,mydb)
    query="UPDATE DATA d SET FLAG=1 WHERE d.ID="+str(id_number)
    cursor.execute(query,())
    mydb.commit()
    print("ID:",id_number,"\tFLAG: 1")
    if close_connection:
        db_connection.close_database_connection(mydb)

# takes id_number cursor and database connection and sets flag to 0
def remove_flag(id_number,cursor=None,mydb=None):
    cursor,mydb=db_connection.get_cursor(cursor,mydb)
    query="UPDATE DATA d SET FLAG=0 WHERE d.ID="+str(id_number)
    cursor.execute(query,())
    mydb.commit()
    print("ID:",id_number,"\tFLAG: 0")

# sets the given wolf number based off of data ID
def set_wolf(id_number,new_wolf,replace=False,cursor=None,mydb=None):
    cursor,mydb=db_connection.get_cursor(cursor,mydb)
    query="SELECT WOLF FROM DATA d WHERE d.ID="+str(id_number)
    cursor.execute(query,())
    old_wolf=cursor.fetchall()
    if old_wolf:
        old_wolf=old_wolf[0][0]
        if not old_wolf or old_wolf=="" or old_wolf=="NULL":
            replace=True
    else:
        replace=True
    if replace:
        query="UPDATE DATA d SET d.WOLF="+str(new_wolf)+" WHERE d.ID="+str(id_number)
        cursor.execute(query,())
        mydb.commit()
        print("ID:",id_number,"\told_wolf",old_wolf,"\tnew_wolf",new_wolf)
    else:
        print("There is already a wolf number, did not replace it")


### sets the number of sunspots : SUNSPOTS
def set_sunspots(id_number,new_sunspots,replace=False,cursor=None,mydb=None):
    cursor,mydb=db_connection.get_cursor(cursor,mydb)
    query="SELECT SUNSPOTS FROM DATA d WHERE d.ID="+str(id_number)
    cursor.execute(query,())
    old_sunspots=cursor.fetchall()
    if old_sunspots:
        old_sunspots=old_sunspots[0][0]
        if not old_sunspots or old_sunspots=="" or old_sunspots=="NULL":
            replace=True
    else:
        replace=True
    if replace:
        query="UPDATE DATA d SET d.SUNSPOTS="+str(new_sunspots)+" WHERE d.ID="+str(id_number)
        cursor.execute(query,())
        mydb.commit()
        print("ID:",id_number,"\told_sunspots",old_sunspots,"\tnew_sunspots",new_sunspots)
    else:
        print("There is already a SUNSPOTS number, did not replace it")


### sets the group number : GROUPS
def set_groups(id_number,new_groups,replace=False,cursor=None,mydb=None):
    cursor,mydb=db_connection.get_cursor(cursor,mydb)
    query="SELECT GROUPS FROM DATA d WHERE d.ID="+str(id_number)
    cursor.execute(query,())
    old_groups=cursor.fetchall()
    if old_groups:
        old_groups=old_groups[0][0]
        if not old_groups or old_groups=="" or old_groups=="NULL":
            replace=True
    else:
        replace=True
    if replace:
        query="UPDATE DATA d SET GROUPS="+str(new_groups)+"WHERE d.ID="+str(id_number)
        cursor.execute(query,())
        mydb.commit()
        print("ID:",id_number,"\told_groups",old_groups,"\tnew_groups",new_groups)
    else:
        print("There is already a GROUPS number, did not replace it")





