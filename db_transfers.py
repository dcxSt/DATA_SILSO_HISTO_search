# this script provides the functions needed for the good 
# and the bad databases to interact

import db_connection
import db_search

def db_transfer(data_id,sender="BAD_DATA_SILSO",recipient="GOOD_DATA_SILSO",
cursor=None,mydb=None,cursor2=None,mydb2=None,close_connections=False):
    cursor,mydb=db_connection.get_cursor(cursor,mydb,the_database=sender)
    # get the data from the data_id
    query="SELECT * FROM DATA d WHERE d.ID="+str(data_id)
    cursor.execute(query,())
    info = cursor.fetchall()[0]

    # check that we really have the correct datapoint
    if data_id != info[0]:
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

    print("successfully fetched data from",sender)#trace

    # write to the new database in it's own format
    cursor2,mydb2=db_connection.get_cursor(cursor=cursor2,mydb=mydb2,the_database=recipient)

    query="INSERT INTO DATA "+\
        "VALUES ("+str(data_id)+" , '"+str(date)+"' , "+str(groups)+" , "+\
            str(sunspots)+" , "+str(wolf)+",'"+str(comment)+"' , '"+\
                str(date_insert)+"' , '"+obs_alias+"' , '"+first_name+"' , '"+\
                    last_name+"' , '"+country+"' , '"+instrument+"' , "+\
                        str(rubrics_number)+" , "+str(mitt_number)+" , "+\
                            str(page_number)+" , "+str(flag)+");"
    
    cursor2.execute(query,())
    mydb2.commit()
    print("Data added to database\n",query)#trace

    # if it is requested close the connections after
    if close_connections:
        db_connection.close_database_connection(mydb=mydb)
        db_connection.close_database_connection(mydb=mydb2)
    


# call the method for debugging with say a random point...
# forgot to take the point out of bad data


#def db_transfer_unflagged(sender="BAD_DATA_SILSO",recipient="GOOD_DATA_SILSO"):


