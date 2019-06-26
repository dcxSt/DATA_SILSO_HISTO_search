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
def set_comment(id_number,comment,cursor=None,mydb=None,replace=False,table_name="DATA"):
    
    cursor,mydb=db_connection.get_cursor(cursor,mydb)
    
    # try to get the original comment
    try:
        query="SELECT COMMENT FROM "+table_name+" d WHERE d.ID="+str(id_number)
        cursor.execute(query,params=())
        original_comment=cursor.fetchall()[0][0]
        print("\noriginal_comment:",end="")
        print(original_comment)
        print("replacing comment:",comment)
        print()
    except:
        original_comment=''
    
    
    if original_comment=='' or replace==True:
        # update table_name and then show the update to user
        query="UPDATE "+table_name+" d SET COMMENT='%s' WHERE d.ID=%s"
        cursor.execute(query % (comment,str(id_number)))
        
        # check that you have properly updated it
        query="SELECT COMMENT FROM "+table_name+" d WHERE d.ID="+str(id_number)
        cursor.execute(query,())
        new_comment = cursor.fetchall()[0][0]
        if new_comment==comment:
            print("successfully updated the comment ")
        print("\nthe comment for ID="+str(id_number)+" has been",end=" ")
        if original_comment=='':
            print("added")
        else:
            print("over-written")
        mydb.commit()
        return True
        

    else:
        print("\nThe data point at ID="+str(id_number)+" already has",
             "a comment:",end="")
        print(original_comment)
        print("it was not replaced")
        return False

# if there is no comment it sets the comment, if there is it adds to it
def add_to_comment(id_number,comment,cursor=None,mydb=None,table_name="DATA"):
    cursor,mydb=db_connection.get_cursor(cursor,mydb)
    
    # try to get the original comment
    try:
        query="SELECT COMMENT FROM "+table_name+" d WHERE d.ID="+str(id_number)
        cursor.execute(query,params=())
        original_comment=cursor.fetchall()[0][0]
        print("\noriginal_comment:",end="")
        print(original_comment)
        print("adding to comment:",comment)
    except:
        original_comment=''

    if original_comment == comment:
        new_comment = comment
    elif original_comment:
        new_comment = original_comment+" ; "+comment
    else:
        new_comment = comment
    try:
        if original_comment[-22:] == " ; suspicious_sunspots" or original_comment[-22:]==" ; suspicious_groups":
            new_comment = original_comment
    except:
        pass
    if original_comment==" ; suspicious_sunspots" or original_comment==" ; suspicious_groups":
        new_comment = comment
    
    # update table_name and then show the update to user
    query="UPDATE "+table_name+" d SET COMMENT='%s' WHERE d.ID=%s"
    cursor.execute(query % (new_comment,str(id_number)))
    
    # check that you have properly updated it
    query="SELECT COMMENT FROM "+table_name+" d WHERE d.ID="+str(id_number)
    cursor.execute(query,())
    the_comment = cursor.fetchall()[0][0]
    if new_comment==the_comment:
        print("successfully updated the comment ")
    print("the comment for ID="+str(id_number)+" has been",end=" ")
    if original_comment=='':
        print("added")
    else:
        print("updated")
    # the all important last line, without this nothing is written to the database
    mydb.commit()

# takes id_number cursor and database connection and adds a flag to the data
def set_flag(id_number,cursor=None,mydb=None,close_connection=True):
    cursor,mydb=db_connection.get_cursor(cursor,mydb)
    query="UPDATE DATA d SET FLAG=1 WHERE d.ID="+str(id_number)
    cursor.execute(query,())
    mydb.commit()
    print("ID:",id_number,"\tFLAG: 1")
    if close_connection:
        db_connection.close_database_connection(mydb)

# sets a flag with a number from 0 to 9 (inclusive)
def set_alternative_flag(id_number,flag_number,cursor=None,mydb=None,close_connection=True,the_database="DATA_SILSO_HISTO"):
    cursor,mydb=db_connection.get_cursor(cursor=cursor,mydb=mydb,the_database=the_database)
    if flag_number>9 or flag_number<0:
        raise Exception
    query="UPDATE DATA d SET FLAG="+str(flag_number)+" WHERE d.ID="+str(id_number)
    cursor.execute(query,())
    mydb.commit()
    print("\nID:",id_number,"\tFLAG:",flag_number)
    if close_connection:
        db_connection.close_database_connection(mydb)

# same as set_alternative_flag but looks at each database and adds flag if there is a matching id_number
def set_alternative_flags_multiple(id_number,flag_number):
    for i in "DATA_SILSO_HISTO","GOOD_DATA_SILSO","BAD_DATA_SILSO":
        cursor,mydb=db_connection.database_connector(the_database=i)
        # if data with this id exists replace it
        try:
            query="SELECT * FROM DATA WHERE ID="+str(id_number)
            cursor.execute(query,())
            current_id = cursor.fetchall()[0][0]
            # if there is nothing the above raises an exception, which is caught
            
            query = "UPDATE DATA SET FLAG="+str(flag_number)+" WHERE ID="+str(id_number)
            cursor.execute(query,())
            mydb.commit()
            print("flag set in",i)
                
        except:
            print("flag not set in",i)
            pass

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





