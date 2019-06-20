# this script provides the functions needed for the good 
# and the bad databases to interact

import db_connection
import db_search

"""
pseudocode for db_transfer

get the data from the id_number
check all the info you have
check there is no corresponding id existing in the recipient database
add the correct data to the recipient database
delete the data from the old database
"""
def db_transfer(id_number,sender="BAD_DATA_SILSO",recipient="GOOD_DATA_SILSO",
cursor=None,mydb=None,cursor2=None,mydb2=None,close_connections=False):
    cursor,mydb=db_connection.get_cursor(cursor,mydb,the_database=sender)

    # get the data from the id_number
    query="SELECT * FROM DATA d WHERE d.ID="+str(id_number)
    cursor.execute(query,())
    info = cursor.fetchall()
    if not info:
        print("\n\nError, selected id that doesn't exist!\n")
        raise Exception
    info=info[0]

    # check that we really have the correct datapoint
    if id_number != info[0]:
        raise Exception

    date = info[1]
    fk_rubrics = info[2]
    fk_observers = info[3]
    groups = info[4]
    sunspots = info[5]
    wolf = info[6]
    comment = info[8]
    date_insert = info[9]
    flag = info[10]

    # get the observer information
    query="SELECT * FROM OBSERVERS o WHERE o.ID="+str(fk_observers)
    cursor.execute(query,())
    info = cursor.fetchall()[0]
    obs_alias = info[1]
    first_name = info[2]
    last_name = info[3]
    country = info[4]
    instrument = info[5]
    
    # get the rubrics information
    query="SELECT * FROM RUBRICS r WHERE r.RUBRICS_ID="+str(fk_rubrics)
    cursor.execute(query,())
    info = cursor.fetchall()[0]
    rubrics_number = info[1]
    mitt_number = info[2]
    page_number = info[3]
    rubrics_source = info[4]
    rubrics_source_date = info[5]

    print("successfully fetched data from",sender)#trace

    # check all the data and put it in correct format
    if date==None:
        date='NULL'
    if groups==None:
        groups='NULL'
    if sunspots==None:
        sunspots='NULL'
    if comment==None:
        comment='NULL'
    if wolf==None:
        wolf='NULL'
    if date_insert==None:
        date_insert='NULL'
    if obs_alias==None:
        print("Error, defective data!")
        raise Exception
    if first_name==None:
        first_name='NULL'
    if last_name==None:
        last_name='NULL'
    if country==None:
        country='NULL'
    if instrument==None:
        instrument='NULL'
    if mitt_number==None:
        mitt_number='NULL'
    if page_number==None:
        page_number='NULL'
    if rubrics_number==None:
        rubrics_number='NULL'
    if flag==None:
        flag='NULL'
    if flag==1:
        print("this data is flagged what are you doing!")
        raise Exception
    if rubrics_source==None:
        rubrics_source='NULL'
    if rubrics_source_date==None:
        rubrics_source_date='NULL'
    

    # write to the new database in it's own format
    # this is supposing that the database doesn't already have something with the specified id
    cursor2,mydb2=db_connection.get_cursor(cursor=cursor2,mydb=mydb2,the_database=recipient)

    # check there is no id already existing in the new database with this name
    query="SELECT * FROM DATA d WHERE d.ID="+str(id_number)
    cursor2.execute(query,())
    info=cursor2.fetchall()
    if info:
        print("\n\nthere is already something in good database with the same id! this is very bad!\n")
        raise Exception
    
    # insert the data into the new database GOOD_DATA_SILSO
    query="INSERT INTO DATA SET "
    query+="ID="+str(id_number)+","
    query+="DATE='"+str(date)+"',"
    query+="GROUPS="+str(groups)+","
    query+="SUNSPOTS="+str(sunspots)+","
    query+="WOLF="+str(wolf)+","
    query+="COMMENT='"+str(comment)+"',"
    query+="DATE_INSERT='"+str(date_insert)+"',"
    query+="OBS_ALIAS='"+str(obs_alias)+"',"
    query+="FIRST_NAME='"+str(first_name)+"',"
    query+="LAST_NAME='"+str(last_name)+"',"
    query+="COUNTRY='"+str(country)+"',"
    query+="INSTRUMENT='"+str(instrument)+"',"
    query+="RUBRICS_NUMBER="+str(rubrics_number)+","
    query+="MITT_NUMBER="+str(mitt_number)+","
    query+="PAGE_NUMBER="+str(page_number)+","
    query+="RUBRICS_SOURCE='"+str(rubrics_source)+"',"
    query+="RUBRICS_SOURCE_DATE='"+str(rubrics_source_date)+"',"
    query+="FLAG="+str(flag)

    cursor2.execute(query,())
    mydb2.commit()
    print("Data added to database")#trace

    # since everything went well and no exceptions were raised 
    # we can delete the original in BAD_DATA_SILSO
    query="DELETE FROM DATA WHERE ID="+str(id_number)
    cursor.execute(query,())
    mydb.commit()
    print("Data ID="+str(id_number)+" deleted from database",sender)#trace


    # if it is requested close the connections after
    if close_connections:
        db_connection.close_database_connection(mydb=mydb)
        db_connection.close_database_connection(mydb=mydb2)
    

def transfer_multiple(id_numbers,cursor=None,mydb=None,cursor2=None,mydb2=None):
    if cursor and mydb and cursor2 and mydb2:
        for i in id_numbers:
            db_transfer(id_number=i,cursor=cursor,mydb=mydb,cursor2=cursor2,mydb2=mydb2)
    else:
        for i in id_numbers:
            db_transfer(id_number=i,close_connections=True)
            



# call the method for debugging with say a random point...
# forgot to take the point out of bad data
# db_transfer(id_number=5,close_connections=True)# testing

#def db_transfer_unflagged(sender="BAD_DATA_SILSO",recipient="GOOD_DATA_SILSO"):


