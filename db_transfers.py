# this script provides the functions needed for the good 
# and the bad databases to interact

import db_connection
import db_search
import db_edit

"""
pseudocode for db_transfer

get the data from the id_number
check all the info you have
check there is no corresponding id existing in the recipient database
add the correct data to the recipient database
delete the data from the old database
"""

# cursor,mydb is the sender's cursor and mydb
# cursor2,mydb2 is the recipient's cursor and mydb
def db_transfer(id_number,sender="BAD_DATA_SILSO",recipient="GOOD_DATA_SILSO",
cursor=None,mydb=None,cursor2=None,mydb2=None,close_connections=False,
dont_delete=False):
    
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
        # FLAG IT, it must have a date
        print("set a flag for where the rubrics source was missing")
        db_edit.set_flag(id_number=id_number,cursor=cursor,mydb=mydb,close_connection=False)
        db_edit.set_comment(id_number=id_number,comment="missing rubrics source",cursor=cursor,mydb=mydb,replace=False)
        return
    

    # write to the new database in it's own format
    # this is supposing that the database doesn't already have something with the specified id
    cursor2,mydb2=db_connection.get_cursor(cursor=cursor2,mydb=mydb2,the_database=recipient)

    # check there is no id already existing in the new database with this name
    query="SELECT * FROM DATA d WHERE d.ID="+str(id_number)
    cursor2.execute(query,())
    info=cursor2.fetchall()
    if info:
        print("\nThere is already something in good database with the same id!\n")
        if dont_delete:
            pass
        else:
            raise Exception
    else:
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

    if not dont_delete:
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


# takes list of id number
def transfer_multiple(id_numbers,cursor=None,mydb=None,cursor2=None,mydb2=None):
    if cursor and mydb and cursor2 and mydb2:
        for i in id_numbers:
            db_transfer(id_number=i,cursor=cursor,mydb=mydb,cursor2=cursor2,mydb2=mydb2)
    else:
        for i in id_numbers:
            db_transfer(id_number=i,close_connections=True)




# the following method and its 2 helpers were copied here from 
# 'dealing_with_duplicates.py', this is a better place for them

# in DATA_SILSO_HISTO it moves selected data into the RUBBISH_DATA
# in GOOD_DATA_SILSO it also moves it into the bin
# in BAD_DATA_SILSO it removed it entirely from the database (this is slightly worrying...)
def move_data_to_bin(id_number,cursor=None,mydb=None,cursor2=None,mydb2=None,cursor3=None,mydb3=None,close_databases=True):
    # DATA_SILSO_HISTO
    # establish connection with DATA_SILSO_HISTO if there isn't one already
    cursor,mydb = db_connection.get_cursor(cursor=cursor,mydb=mydb,the_database="DATA_SILSO_HISTO")
    # add it to the bin first
    query = "SELECT * FROM DATA d WHERE d.ID="+str(id_number)
    cursor.execute(query,())
    # the try block is because sometimes there are 3 identical datapoints, this circumnavigates the problem
    try:
        info = cursor.fetchall()[0]
        id_number,date,fk_rubrics,fk_observers,groups,sunspots,wolf,quality,comment,date_insert,flag=transcribe_info_old(info)
        
        query = "INSERT INTO RUBBISH_DATA SET "
        query += "ID = "+str(id_number)+","
        query += "DATE = '"+str(date)+"',"
        query += "FK_RUBRICS = "+str(fk_rubrics)+","
        query += "FK_OBSERVERS ="+str(fk_observers)+","
        query += "GROUPS ="+str(groups)+","
        query += "SUNSPOTS ="+str(sunspots)+","
        query += "WOLF ="+str(wolf)+","
        query += "QUALITY = NULL,"
        query += "COMMENT ='"+str(comment)+"',"
        query += "DATE_INSERT ='"+str(date_insert)+"',"
        query += "FLAG ="+str(flag)+";"
        cursor.execute(query,())
        mydb.commit()
        print("copied into rubbish bin")#trace

        # remove it from the database
        query = "DELETE FROM DATA WHERE ID="+str(id_number)
        cursor.execute(query,())
        mydb.commit()
        print("deleted from original")#trace
    except:
        pass

    # GOOD_DATA_SILSO
    # if the data is here we move it as in the above, 
    # remember they have the same id_number regardless of which 
    # database they are in because they were exact copies!

    # establish a connection
    cursor2,mydb2 = db_connection.get_cursor(cursor=cursor2,mydb=mydb2,the_database="GOOD_DATA_SILSO")
    # add it to the bin first
    query = "SELECT * FROM DATA d WHERE d.ID="+str(id_number)
    cursor2.execute(query)
    # if there is nothing don't do anything
    try:
        info2=cursor2.fetchall()[0]
        id_number,date,groups,sunspots,wolf,comment,date_insert,obs_alias,first_name,last_name,country,instrument,rubrics_number,mitt_number,page_number,flag,rubrics_source,rubrics_source_date=transcribe_info_new(info2)

        query = "INSERT INTO RUBBISH_DATA SET "
        query += "ID = "+str(id_number)+","
        query += "DATE = '"+str(date)+"',"
        query += "GROUPS ="+str(groups)+","
        query += "SUNSPOTS ="+str(sunspots)+","
        query += "WOLF ="+str(wolf)+","
        query += "COMMENT ='"+str(comment)+"',"
        query += "DATE_INSERT ='"+str(date_insert)+"',"

        query += "OBS_ALIAS='"+str(obs_alias)+"',"
        query += "FIRST_NAME='"+str(first_name)+"',"
        query += "LAST_NAME='"+str(last_name)+"',"
        query += "COUNTRY='"+str(country)+"',"
        query += "INSTRUMENT='"+str(instrument)+"',"

        query += "RUBRICS_NUMBER="+str(rubrics_number)+","
        query += "MITT_NUMBER="+str(mitt_number)+","
        query += "PAGE_NUMBER="+str(page_number)+","
        query += "FLAG ="+str(flag)+","
        query += "RUBRICS_SOURCE ='"+str(rubrics_source)+"',"
        query += "RUBRICS_SOURCE_DATE='"+str(rubrics_source_date)+"';"
        
        cursor2.execute(query,())
        mydb2.commit()
        print("copied into rubbish bin")#trace

        # delete the data
        query = "DELETE FROM DATA WHERE ID="+str(id_number)
        cursor2.execute(query,())
        mydb2.commit()
        print("deleted from original")#trace

    except IndexError:
        #print("there does not exist any data with the id_number "+str(id_number)+" in the database GOOD_DATA_SILSO")#trace
        pass

    
    # BAD_DATA_SILSO
    # make sure you are connected
    cursor3,mydb3 = db_connection.get_cursor(cursor=cursor3,mydb=mydb3,the_database="BAD_DATA_SILSO")
    # if the data is here we simply scrap it, this is much simpler
    query = "DELETE FROM DATA WHERE ID="+str(id_number)
    cursor3.execute(query,())
    mydb3.commit()

    if close_databases:
        db_connection.close_database_connection(mydb)
        db_connection.close_database_connection(mydb2)
        db_connection.close_database_connection(mydb3)


# helper method for move_data_to_bin()
def transcribe_info_old(info):
    id_number = info[0]
    date = info[1]
    fk_rubrics = info[2]
    fk_observers = info[3]
    groups = info[4]
    sunspots = info[5]
    wolf = info[6]
    quality = 'NULL' # it always is
    comment = info[8]
    date_insert = info[9]
    flag = info[10]
    if not groups and groups!=0:
        groups='NULL'
    if not sunspots and sunspots!=0:
        sunspots='NULL'
    if not wolf and wolf!=0:
        wolf='NULL'
    if not fk_rubrics:
        fk_rubrics='NULL'
    if not fk_observers:
        fk_observers='NULL'
    if comment!='':
        comment=''
    if not flag and flag!=0:
        flag='NULL'
    return id_number,date,fk_rubrics,fk_observers,groups,sunspots,wolf,quality,comment,date_insert,flag

# helper method for move_data_to_bin()
def transcribe_info_new(info):
    id_number = info[0]
    date = info[1]
    groups = info[2]
    sunspots = info[3]
    wolf = info[4]
    comment =info[5]
    date_insert = info[6]
    obs_alias = info[7]
    first_name=info[8]
    last_name = info[9]
    country = info[10]
    instrument = info[11]
    rubrics_number=info[12]
    mitt_number = info[13]
    page_number = info[14]
    flag = info[15]
    rubrics_source = info[16]
    rubrics_source_date = info[17]
    if not groups and groups!=0:
        groups='NULL'
    if not sunspots and sunspots!=0:
        sunspots='NULL'
    if not wolf and wolf!=0:
        wolf='NULL'
    if not comment:
        comment=''
    if not flag and flag!=0:
        flag='NULL'
    if not first_name:
        first_name=''
    if not last_name:
        last_name=''
    if not country:
        country = ''
    if not instrument:
        instrument=''
    if not rubrics_number and rubrics_number!=0:
        rubrics_number='NULL'
    if not mitt_number and mitt_number!=0:
        mitt_number='NULL'
    if not page_number and page_number !=0:
        page_number='NULL'
    if not rubrics_source:
        rubrics_source=''
    if not rubrics_source_date:
        rubrics_source_date='NULL'# Watch out for this one

    return id_number,date,groups,sunspots,wolf,comment,date_insert,obs_alias,first_name,last_name,country,instrument,rubrics_number,mitt_number,page_number,flag,rubrics_source,rubrics_source_date

# in DATA_SILSO_HISTO it moves data from RUBBISH_DATA to DATA
# in GOOD_DATA_SILSO it does the same
# in BAD_DATA_SILSO it does nothing
def move_data_out_of_bin(id_number,cursor=None,mydb=None,cursor2=None,mydb2=None,close_databases=True):
    # DATA_SILSO_HISTO
    # establish connection with DATA_SILSO_HISTO if there isn't one already
    cursor,mydb = db_connection.get_cursor(cursor=cursor,mydb=mydb,the_database="DATA_SILSO_HISTO")

    # first we add it to table DATA
    query = "SELECT * FROM RUBBISH_DATA d WHERE d.ID="+str(id_number)
    cursor.execute(query,())
    try:
        info = cursor.fetchall()[0]
        id_number,date,fk_rubrics,fk_observers,groups,sunspots,wolf,quality,comment,date_insert,flag=transcribe_info_old(info)

        query = "INSERT INTO DATA SET "
        query += "ID = "+str(id_number)+","
        query += "DATE = '"+str(date)+"',"
        query += "FK_RUBRICS = "+str(fk_rubrics)+","
        query += "FK_OBSERVERS ="+str(fk_observers)+","
        query += "GROUPS ="+str(groups)+","
        query += "SUNSPOTS ="+str(sunspots)+","
        query += "WOLF ="+str(wolf)+","
        query += "QUALITY = NULL,"
        query += "COMMENT ='"+str(comment)+"',"
        query += "DATE_INSERT ='"+str(date_insert)+"',"
        query += "FLAG ="+str(flag)+";"
        cursor.execute(query,())
        mydb.commit()
        print("copied into DATA")#trace

        # remove from RUBBISH_DATA
        query = "DELETE FROM RUBBISH_DATA WHERE ID="+str(id_number)
        cursor.execute(query,())
        mydb.commit()
        print("deleted from RUBBISH_DATA")#trace
    except:
        print("\n\nError not in database (maybe)")
        raise Exception

    # GOOD_DATA_SILSO
    # if the data is here we move it as in the above
    # remember they have the same id_number regardless of which database

    # establish a connection
    cursor2,mydb2 = db_connection.get_cursor(cursor=cursor2,mydb=mydb2,the_database="GOOD_DATA_SILSO")
    # add it to DATA first
    query = "SELECT * FROM RUBBISH_DATA d WHERE d.ID="+str(id_number)
    cursor2.execute(query,())
    # if there is nothing raise an excepption
    try:
        info2 = cursor2.fetchall()[0]
        id_number,date,groups,sunspots,wolf,comment,date_insert,obs_alias,first_name,last_name,country,instrument,rubrics_number,mitt_number,page_number,flag,rubrics_source,rubrics_source_date=transcribe_info_new(info2)

        query = "INSERT INTO DATA SET "
        query += "ID = "+str(id_number)+","
        query += "DATE = '"+str(date)+"',"
        query += "GROUPS ="+str(groups)+","
        query += "SUNSPOTS ="+str(sunspots)+","
        query += "WOLF ="+str(wolf)+","
        query += "COMMENT ='"+str(comment)+"',"
        query += "DATE_INSERT ='"+str(date_insert)+"',"

        query += "OBS_ALIAS='"+str(obs_alias)+"',"
        query += "FIRST_NAME='"+str(first_name)+"',"
        query += "LAST_NAME='"+str(last_name)+"',"
        query += "COUNTRY='"+str(country)+"',"
        query += "INSTRUMENT='"+str(instrument)+"',"

        query += "RUBRICS_NUMBER="+str(rubrics_number)+","
        query += "MITT_NUMBER="+str(mitt_number)+","
        query += "PAGE_NUMBER="+str(page_number)+","
        query += "FLAG ="+str(flag)+","
        query += "RUBRICS_SOURCE ='"+str(rubrics_source)+"',"
        query += "RUBRICS_SOURCE_DATE='"+str(rubrics_source_date)+"';"
        
        cursor2.execute(query,())
        mydb2.commit()
        print("copied into DATA")#trace

        # remove from RUBBISH_DATA
        query = "DELETE FROM RUBBISH_DATA WHERE ID="+str(id_number)
        cursor.execute(query,())
        mydb.commit()
        print("deleted from RUBBISH_DATA\n")#trace

    except IndexError:
        print("There does not exist any data with the id_number "+str(id_number)+" in the database GOOD_DATA_SILSO")#trace
        raise Exception
    except Exception:
        input("Some unknown error has occurred")
        

    # close the connections if required
    if close_databases:
        db_connection.close_database_connection(mydb)
        db_connection.close_database_connection(mydb2)



