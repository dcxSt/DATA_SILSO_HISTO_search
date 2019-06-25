# dealing with the duplicates in every way possible

import db_connection
import db_edit
import db_search
import searching_the_manuals


### this method is the backbone of this script, who's sole purpouse is to scrap the
### redundant duplicates. It takes and id_number. In DATA_SILSO_HISTO it moves it into 
### the rubbish bin that i made. With the same id it sees if this id can be found in
### GOOD_DATA_SILSO, if so it moves it into the bin. Then checks if the data is in 
### BAD_DATA_SILSO if so it moves it removes it entirely from the database.
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


# method takes the greater duplicates dictionary and deletes the first of each pair that has been entered twice
def delete_entered_twice_duplicates(greater_duplicates_dictionary):
    # establish 3 connections
    cursor,mydb = db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")
    cursor3,mydb3 = db_connection.database_connector(the_database="BAD_DATA_SILSO")
    for alias in greater_duplicates_dictionary:
        for i in greater_duplicates_dictionary[alias]:
            id_number1 = i[1][0]
            groups1 = i[1][8]
            sunspots1 = i[1][9]
            wolf1 = i[1][10]
            obs_id1 = i[1][1]
            fk_rubrics1 = i[1][4]

            groups2 = i[2][8]
            sunspots2 = i[2][9]
            wolf2 = i[2][10]
            obs_id2 = i[2][1]
            fk_rubrics2 = i[2][4]

            # select only the ones that have very similar stuff
            if groups1==groups2 and sunspots1==sunspots2 and wolf1==wolf2 and obs_id1==obs_id2 and fk_rubrics1==fk_rubrics2:
                # remove only the first one
                move_data_to_bin(id_number=id_number1,cursor=cursor,mydb=mydb,cursor2=cursor2,mydb2=mydb2,cursor3=cursor3,mydb3=mydb3,close_databases=False)

    # close the connections 
    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb2)
    db_connection.close_database_connection(mydb3)

# delete the entered twice duplicates
"""
greater_duplicates_dictionary = searching_the_manuals.greater_duplicates_data(force_recalculate=True)
delete_entered_twice_duplicates(greater_duplicates_dictionary)
"""






