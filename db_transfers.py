# This script provides the functions needed for the good 
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
# method for transfering and copyting data from old format to new format
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
    
    # get the rubrics information iff there is a rubrics
    if fk_rubrics:
        query="SELECT * FROM RUBRICS r WHERE r.RUBRICS_ID="+str(fk_rubrics)
        cursor.execute(query,())
        info = cursor.fetchall()[0]
        rubrics_number = info[1]
        mitt_number = info[2]
        page_number = info[3]
        rubrics_source = info[4]
        rubrics_source_date = info[5]
    else:
        rubrics_number = None
        mitt_number = None
        page_number = None
        rubrics_source = None
        rubrics_source_date = None

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
        # FLAG IT, it must have a date; later - I don't care about the rubrics source date
        #print("set a flag for where the rubrics source was missing")
        #db_edit.set_flag(id_number=id_number,cursor=cursor,mydb=mydb,close_connection=False)
        #db_edit.set_comment(id_number=id_number,comment="missing rubrics source",cursor=cursor,mydb=mydb,replace=False)
        #return
        pass
    

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
        if date_insert!='NULL': query+="DATE_INSERT='"+str(date_insert)+"',"# without the conditional statement an exception is raised when there is no date_insert...
        query+="OBS_ALIAS='"+str(obs_alias)+"',"
        query+="FIRST_NAME='"+str(first_name)+"',"
        query+="LAST_NAME='"+str(last_name)+"',"
        query+="COUNTRY='"+str(country)+"',"
        query+="INSTRUMENT='"+str(instrument)+"',"
        query+="RUBRICS_NUMBER="+str(rubrics_number)+","
        query+="MITT_NUMBER="+str(mitt_number)+","
        query+="PAGE_NUMBER="+str(page_number)+","
        query+="RUBRICS_SOURCE='"+str(rubrics_source)+"',"
        if rubrics_source_date:
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


#db_transfer(221618,sender="DATA_SILSO_HISTO",close_connections=True,dont_delete=True)

# takes list of id numbers
def transfer_multiple(id_numbers,cursor=None,mydb=None,cursor2=None,mydb2=None,sender=None):
    if cursor and mydb and cursor2 and mydb2:
        for i in id_numbers:
            db_transfer(id_number=i,cursor=cursor,mydb=mydb,cursor2=cursor2,mydb2=mydb2)
    elif not sender:
        for i in id_numbers:
            db_transfer(id_number=i,close_connections=True)
    else:
        for i in id_numbers:
            db_transfer(id_number=i,close_connections=True,sender=sender)


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

# same as above but only affects GOOD_DATA_SILSO, doesn't touch the rest
def move_data_to_bin_only_good(id_number,cursor2=None,mydb2=None,close_databases=True):
    # GOOD_DATA_SILSO
    # if the data is here we move it to RUBBISH_DATA 

    # establish a connection
    cursor2,mydb2 = db_connection.get_cursor(cursor=cursor2,mydb=mydb2,the_database="GOOD_DATA_SILSO")
    
    # first check to see if it's already in the bin
    try:
        no_duplicate_in_bin = True
        query = "SELECT * FROM RUBBISH_DATA d WHERE d.ID="+str(id_number)
        cursor2.execute(query,())
        rubbish_info2=cursor2.fetchall()[0]
        if rubbish_info2[0]==id_number:
            no_duplicate_in_bin = False
    except:
        pass
    
    # add it to the bin first
    query = "SELECT * FROM DATA d WHERE d.ID="+str(id_number)
    cursor2.execute(query,())
    # if there is nothing don't do anything
    try:
        info2=cursor2.fetchall()[0]
        id_number,date,groups,sunspots,wolf,comment,date_insert,obs_alias,first_name,last_name,country,instrument,rubrics_number,mitt_number,page_number,flag,rubrics_source,rubrics_source_date=transcribe_info_new(info2)

        # if it's already in the bin use update
        if no_duplicate_in_bin==False:
            query = "UPDATE RUBBISH_DATA SET "
        # otherwise insert
        else:
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
        query += "RUBRICS_SOURCE_DATE='"+str(rubrics_source_date)+"'"

        # if it's already in the bin use update
        if no_duplicate_in_bin==False:
            query += " WHERE ID="+str(id_number)

        
        cursor2.execute(query,())
        mydb2.commit()
        print("copied into rubbish bin")#trace

        # delete the data
        query = "DELETE FROM DATA WHERE ID="+str(id_number)
        cursor2.execute(query,())
        mydb2.commit()
        print("deleted from original")#trace

    except IndexError:
        print("there does not exist any data with the id_number "+str(id_number)+" in the database GOOD_DATA_SILSO")#trace
        pass

    if close_databases:
        db_connection.close_database_connection(mydb2)


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
def move_data_out_of_bin(id_number,cursor=None,mydb=None,cursor2=None,mydb2=None,
close_databases=True):
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
        #raise Exception# let this slide...
    except Exception:
        print("Some unknown error has occurred, but im going to let it slide")
        

    # close the connections if required
    if close_databases:
        db_connection.close_database_connection(mydb)
        db_connection.close_database_connection(mydb2)


# move carrington's data to rubbish from good data silso
def move_carrington303_good_to_rubbish():
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")
    query = "SELECT * FROM DATA WHERE FLAG=7 AND RUBRICS_NUMBER=303"
    cursor2.execute(query,())
    data = cursor2.fetchall()
    for i in data:
        id_number = i[0]
        move_data_to_bin_only_good(id_number,cursor2,mydb2,close_databases=False)
    db_connection.close_database_connection(mydb2)
    
# gets rid of WOLF - S - M 's data from 1864 that doesn't belong to him; exec only once
def move_wolf_1864_to_rubbish():
    cursor,mydb = db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    # first find the dates where there are already other observers
    query = "SELECT DATE FROM DATA WHERE FK_OBSERVERS IN (17,32,3) AND DATE>='1864-01-01' AND DATE<'1865-01-01'"
    cursor.execute(query,())
    dates_not_wolf = cursor.fetchall()
    query = "SELECT * FROM DATA WHERE FK_OBSERVERS=2 AND DATE>='1864-01-01' AND DATE<'1865-01-01'"
    cursor.execute(query,())
    wolfs_data = cursor.fetchall()
    # ineficient but ez to write
    not_wolf_ids = []
    for i in wolfs_data:
        really_wolf = True
        for j in dates_not_wolf:
            if j[0] in i: really_wolf = False
        if False==really_wolf: not_wolf_ids.append(i[0])

    db_connection.close_database_connection(mydb)

    for i in not_wolf_ids:
        move_data_to_bin(i)

    print("DONE!")

# Execute once
# separates out the data from wolf-s-m 1865 table into different observer
def separate_1865_observers():
    # dictionary of dates in string format without year, they're all 1865
    dic = {}
    dic["Schwabe"] = ["01-03","01-12","01-13","01-20","01-21","01-22",
    "01-28","01-30","02-01","02-06","02-07","02-10","02-16","02-20","02-22",
    "02-23","02-25","02-27","03-01","03-09","03-10","03-11","03-20","04-14",
    "05-01","05-11","05-19","06-02","07-10","07-21","07-25","07-30","08-10",
    "08-13","08-14","08-16","08-17","08-22","09-17","09-23","10-10","10-14",
    "10-23","10-24","10-25","10-28","11-01","11-02","11-08","11-10","11-17",
    "11-21","11-22","11-27","11-29","11-30","12-01","12-03","12-11","12-21",
    "12-23","12-27","12-29","12-30"]
    dic["WOLF - P - M"] = ["01-01","01-06","01-14","01-18","01-29","02-08",
    "02-09","02-11","02-12","02-13","02-14","02-18","02-21","02-24","02-26",
    "03-24","02-27","03-30","04-04","05-06","06-25","08-15","08-27","08-28",
    "10-01","11-09","11-15","11-28","12-17","12-18","12-31"]
    dic["Jenzer"] = ["01-07","02-15","12-22","12-26"]
    dic["Weber"] = ["01-02","01-19","02-04","03-02","03-03","03-07","03-23",
    "03-31","04-15","05-16","10-27","10-31","11-03","11-05","12-04","12-08",
    "12-09","12-20","12-24","12-25"]

    # add the years
    for i in dic:
        for j in dic[i]:
            dic[i][dic[i].index(j)]="1865-"+j

    cursor,mydb = db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")
    cursor3,mydb3 = db_connection.database_connector(the_database="BAD_DATA_SILSO")   

    # move schwabe
    for j in dic["Schwabe"]:
        query1 =  "UPDATE DATA SET FK_OBSERVERS=17 WHERE DATE='"+j+"' AND FK_OBSERVERS=2"
        cursor.execute(query1,())
        cursor3.execute(query1,())
        mydb.commit()
        mydb3.commit()

        query2 = "UPDATE DATA SET OBS_ALIAS='Schwabe',FIRST_NAME='Heinrich',LAST_NAME='Schwabe',COUNTRY='DE',INSTRUMENT='(NULL)',COMMENT='(NULL)' WHERE DATE='"+j+"' AND OBS_ALIAS='WOLF - S - M'"
        cursor2.execute(query2,())
        mydb2.commit()

    # move wolf p
    for j in dic["WOLF - P - M"]:
        query1 = "UPDATE DATA SET FK_OBSERVERS=3 WHERE DATE='"+j+"' AND FK_OBSERVERS=2"
        cursor.execute(query1,())
        cursor3.execute(query1,())
        mydb.commit()
        mydb3.commit()

        query2 = "UPDATE DATA SET OBS_ALIAS='WOLF - P - M',INSTRUMENT='43 mm Portable' WHERE DATE='"+j+"' AND OBS_ALIAS='WOLF - S - M'"
        cursor2.execute(query2,())
        mydb2.commit()

    # move weber
    for j in dic["Weber"]:
        query1 = "UPDATE DATA SET FK_OBSERVERS=32 WHERE DATE='"+j+"' AND FK_OBSERVERS=2"
        cursor.execute(query1,())
        cursor3.execute(query1,())
        mydb.commit()
        mydb3.commit()

        query2 = "UPDATE DATA SET OBS_ALIAS='Weber',FIRST_NAME='XXX',LAST_NAME='Weber',COUNTRY='XXX',INSTRUMENT='(NULL)',COMMENT='(NULL)' WHERE DATE='"+j+"' AND OBS_ALIAS='WOLF - S - M'"
        cursor2.execute(query2,())
        mydb2.commit()
    print("done weber wolfp and schwabe")#trace

    # bin Jenzer
    for j in dic["Jenzer"]:
        # find all the ids
        query = "SELECT ID FROM DATA WHERE FK_OBSERVERS=2 AND DATE='"+j+"'"
        cursor.execute(query,())
        idn = cursor.fetchall()
        if len(idn)>1:
            raise Exception
        idn = idn[0][0]
        move_data_to_bin(idn,cursor=cursor,mydb=mydb,cursor2=cursor2,mydb2=mydb2,cursor3=cursor3,mydb3=mydb3,close_databases=False)
        
    

    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb2)
    db_connection.close_database_connection(mydb3)
    
# Execute once
# separates out the data from wolf-s-m 1866 table into different observers
def separate_1866_observers():
    # dictionary of dates in string format without year, they're all 1866
    dic = {}
    dic["Schwabe"] = ["01-01","01-08","01-14","02-12","02-16","02-21",
    "03-11","08-12","09-11","10-09","10-12","10-23","10-24","11-09","11-17",
    "11-25","12-03","12-10","12-11","12-14","12-16","12-17","12-19","12-20",
    "12-21","12-22","12-23","12-27"]
    dic["WOLF - P - M"] = ["01-02","01-12","01-17","01-23","02-01","02-05",
    "03-21","04-12","06-10","08-03","08-10","09-26","10-14","10-26","11-26"]
    dic["Schmidt"] = ["01-11","11-02","11-27"]
    dic["Weber"] = ["01-05","01-06","01-07","01-15","02-06","02-13","02-19",
    "02-20","02-22","02-24","03-03","03-05","03-06","03-09","03-14","03-24",
    "04-01","04-02","04-06","04-20","05-02","05-05","06-14","08-13","08-15",
    "10-15","10-18","10-22","10-25","10-28","10-29","11-19","11-28","11-30",
    "12-28"]

    fk_dic = {"Weber":32 , "Schmidt":23 , "Schwabe":17 , "WOLF - P - M":3}
    meta = {"Weber":["XXX","Weber","XXX","(NULL)","(NULL)"],
    "Schmidt":["Johan Friedrich Julius","Schmidt","DE","(NULL)","(NULL)"],
    "Schwabe":["Heinrich","Schwabe","DE","(NULL)","(NULL)"],
    "WOLF - P - M":["Rudolph","Wolf","CH","43 mm Portable","Alias= Wolf - Portable - Mittheilung"]}

    for i in dic:
        for j in dic[i]:
            dic[i][dic[i].index(j)] = "1866-"+j
    
    cursor,mydb = db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")
    cursor3,mydb3 = db_connection.database_connector(the_database="BAD_DATA_SILSO")

    for i in dic:
        for j in dic[i]:
            fk_obs = fk_dic[i]
            query1 = "UPDATE DATA SET FK_OBSERVERS="+str(fk_obs)+" WHERE DATE='"+j+"' AND FK_OBSERVERS=2"
            cursor.execute(query1,())
            mydb.commit()
            cursor3.execute(query1,())
            mydb3.commit()

            query2 = "UPDATE DATA SET OBS_ALIAS='"+i+"',FIRST_NAME='"+meta[i][0]+"',"
            query2 += "LAST_NAME='"+meta[i][1]+"',"
            query2 += "COUNTRY='"+meta[i][2]+"',"
            query2 += "INSTRUMENT='"+meta[i][3]+"',"
            query2 += "COMMENT='"+meta[i][4]+"'"
            cursor2.execute(query2,())
            mydb2.commit()


    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb2)
    db_connection.close_database_connection(mydb3)

# transfers all those with flag=2 from BAD_DATA_SILSO to GOOD_DATA_SILSO
def transfer_flag_2():
    cursor3,mydb3 = db_connection.database_connector(the_database="BAD_DATA_SILSO")
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")
    data = db_search.select_all_data(the_database="BAD_DATA_SILSO")
    for d in data:
        idn = d[0]
        flag = d[10]
        if flag==2:
            db_transfer(idn,cursor=cursor3,mydb=mydb3,cursor2=cursor2,mydb2=mydb2)

    db_connection.close_database_connection(mydb2)
    db_connection.close_database_connection(mydb3)

# transfer all those with flag=0 from BAD_DATA_SILSO to GOOD_DATA_SILSO
def transfer_flag_0():
    cursor3,mydb3 = db_connection.database_connector(the_database="BAD_DATA_SILSO")
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")
    data = db_search.select_all_data(cursor=cursor3,mydb=mydb3,the_database="BAD_DATA_SILSO",close_connection=False)
    for d in data:
        idn = d[0]
        flag = d[10]
        if flag==0:
            db_transfer(idn,cursor=cursor3,mydb=mydb3,cursor2=cursor2,mydb2=mydb2)

    db_connection.close_database_connection(mydb2)
    db_connection.close_database_connection(mydb3)

# transfers all those with flag=3 from BAD_DATA_SILSO to GOOD_DATA_SILSO
def transfer_flag_3():
    cursor3,mydb3 = db_connection.database_connector(the_database="BAD_DATA_SILSO")
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")
    data = db_search.select_all_data(cursor=cursor3,mydb=mydb3,the_database="BAD_DATA_SILSO",close_connection=False)
    for d in data:
        idn = d[0]
        flag = d[10]
        if flag==3:
            db_transfer(idn,cursor=cursor3,mydb=mydb3,cursor2=cursor2,mydb2=mydb2)

    db_connection.close_database_connection(mydb2)
    db_connection.close_database_connection(mydb3)

# transfers all those with flag=8 from BAD_DATA_SILSO to GOOD_DATA_SILSO
# the reason i'm writing methods for each of these flags rather than just a general one \
# that takes input is because I don't wanna execute the wrong flag...
def transfer_flag_8():
    cursor3,mydb3 = db_connection.database_connector(the_database="BAD_DATA_SILSO")
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")
    data = db_search.select_all_data(cursor=cursor3,mydb=mydb3,the_database="BAD_DATA_SILSO",close_connection=False)
    for d in data:
        idn = d[0]
        flag = d[10]
        if flag==8:
            db_transfer(idn,cursor=cursor3,mydb=mydb3,cursor2=cursor2,mydb2=mydb2)

    db_connection.close_database_connection(mydb2)
    db_connection.close_database_connection(mydb3)

def transfer_flag_9():
    cursor3,mydb3 = db_connection.database_connector(the_database="BAD_DATA_SILSO")
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")
    data = db_search.select_all_data(cursor=cursor3,mydb=mydb3,the_database="BAD_DATA_SILSO",close_connection=False)
    for d in data:
        idn = d[0]
        flag = d[10]
        if flag==9:
            db_transfer(idn,cursor=cursor3,mydb=mydb3,cursor2=cursor2,mydb2=mydb2)

    db_connection.close_database_connection(mydb2)
    db_connection.close_database_connection(mydb3)



#separate_1866_observers()

#transfer_flag_0()
#transfer_flag_3()
#transfer_flag_8()
#transfer_flag_9()



