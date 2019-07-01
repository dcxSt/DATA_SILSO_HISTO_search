# dealing with the duplicates in every way possible

import db_connection
import db_edit
import db_search
import searching_the_manuals


### this method is the backbone of this script, who's sole purpouse is to scrap the
### redundant duplicates. It takes an id_number only! In DATA_SILSO_HISTO it moves it into 
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

# delete the entered twice duplicates (just running the method)
"""
greater_duplicates_dictionary = searching_the_manuals.greater_duplicates_data(force_recalculate=True)
delete_entered_twice_duplicates(greater_duplicates_dictionary)
"""

# method to flag the duplicate that is missing values (sunspots / wolf == na or none or something)
def flag_many_duplicates():
    # get the proper duplicates dictionary
    duplicates_dictionary_by_date = searching_the_manuals.duplicates_by_date(the_database="DATA_SILSO_HISTO")

    # keep track of the counts
    single_deficient_count=0
    both_deficient_count=0
    both_clean_count=0

    # establish 3 connections
    cursor,mydb = db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")
    cursor3,mydb3 = db_connection.database_connector(the_database="BAD_DATA_SILSO")

    # for each duplicate
    for date in duplicates_dictionary_by_date:
        tuple1 = duplicates_dictionary_by_date[date][0]
        tuple2 = duplicates_dictionary_by_date[date][1]
        
        id1=tuple1[0]
        id2=tuple2[0]

        # determine if one or both are deficient, so identical tests on both
        deficient1=False
        fk_observer,fk_rubrics = tuple1[1],tuple1[4]
        groups,sunspots,wolf = tuple1[9],tuple1[10],tuple1[11]
        flag = tuple1[14]
        # if observers or rubrics are missing...
        if fk_observer=="na" or fk_rubrics=="na" or fk_rubrics==0:
            deficient1=True
        elif flag==4 or flag==5:
            deficient1=True
        elif sunspots==None or groups==None:
            deficient1=True
        elif sunspots>150 or groups>30:
            deficient1=True

        # determine if one or both are deficient, so identical tests on both
        deficient2=False
        fk_observer,fk_rubrics = tuple2[1],tuple2[4]
        groups,sunspots,wolf = tuple2[9],tuple2[10],tuple2[11]
        flag = tuple2[14]
        if fk_observer==36 and sunspots>100:
            print("flag:",flag)
        # if observers or rubrics are missing...
        if fk_observer=="na" or fk_rubrics=="na" or fk_rubrics==0:
            deficient2=True
        elif flag==4 or flag==5:
            deficient2=True
        elif groups==None or sunspots==None:
            deficient2=True
        elif sunspots>150 or groups>30:
            deficient2=True


        if deficient1 and not deficient2:
            single_deficient_count+=1
            db_edit.set_alternative_flags_multiple(id_number=id1,flag_number=3)
            
        elif deficient2 and not deficient1:
            single_deficient_count+=1
            db_edit.set_alternative_flags_multiple(id_number=id2,flag_number=3)

        elif deficient1 and deficient2:
            both_deficient_count+=1

        else:
            both_clean_count+=1

                

        # flag the bad one with FLAG=3

    
    # close the connections 
    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb2)
    db_connection.close_database_connection(mydb3)

    print("\n\n\nSingle deficient count =",single_deficient_count)
    print("both_deficient_count =",both_deficient_count)
    print("both clean count =",both_clean_count)

# method that flags errors highlighted in corrections_needed.md
def flag3_from_correction_txt():
    # list of id's where penumbra is written and needs to go into the rubbish bin database
    penumbra = [31460]


# method that takes a cursor, a database, a rubrics_number and a year
# and changes every date from this rubrics_number to the year specified
# while leaving the rest of the date unchanged
def change_date_rubric(rubrics_number,new_year,old_year,cursor,mydb,new_format=True):
    # I can use this for all databases cause DATE is in DATA regardless of format
    # there is just a slight ajustment in initial query for new format vs old format
    if new_format==True:
        query = "SELECT ID,DATE FROM DATA WHERE RUBRICS_NUMBER="+str(rubrics_number)
        cursor.execute(query,())
        data = cursor.fetchall()
        print()
        
    else:
        # i think this works but ought to check, sometimes python is dodgy
        query = "SELECT ID,DATE FROM DATA WHERE FK_RUBRICS IN (SELECT RUBRICS_ID FROM RUBRICS WHERE RUBRICS_NUMBER="+str(rubrics_number)+")"
        cursor.execute(query,())
        data = cursor.fetchall()

    # arrange all the dates into a dictionary so I can sort them well
    old_date_dictionary_by_id = {}
    for i in data:
        id_number = i[0]
        date = str(i[1]) # string representation of the date
        old_date_dictionary_by_id[id_number] = date

    new_date_dictionary_by_id = {}
    # make a dictionary with corrected version
    for id_number in old_date_dictionary_by_id:
        old_date = old_date_dictionary_by_id[id_number]
        if old_date[:4] != str(old_year):
            print("\nfor the id number",id_number)
            print("date found = ",old_date)
            print("old_year should be : ",old_year)
            print("something fishy is goin on")
            input("(enter to continue anyway)")
        new_date = str(new_year)+old_date[4:]
        new_date_dictionary_by_id[id_number] = new_date

    # make the change to the database
    for id_number in new_date_dictionary_by_id:
        new_date = new_date_dictionary_by_id[id_number]
        query = "UPDATE DATA SET DATE='"+str(new_date)+"' WHERE ID="+str(id_number)
        cursor.execute(query,())
        mydb.commit()

# calls change_date_rubrics alot
def change_dates():
    # open the connections
    cursor,mydb = db_connection.database_connector(the_database='DATA_SILSO_HISTO')
    cursor2,mydb2 = db_connection.database_connector(the_database='GOOD_DATA_SILSO')
    cursor3,mydb3 = db_connection.database_connector(the_database='BAD_DATA_SILSO')

    change_date_rubric(rubrics_number=12902,new_year=1931,old_year=1908,cursor=cursor,mydb=mydb,new_format=False)
    change_date_rubric(rubrics_number=12902,new_year=1931,old_year=1908,cursor=cursor2,mydb=mydb2,new_format=True)
    change_date_rubric(rubrics_number=12902,new_year=1931,old_year=1908,cursor=cursor3,mydb=mydb3,new_format=False)

    change_date_rubric(rubrics_number=1279,new_year=1920,old_year=1919,cursor=cursor,mydb=mydb,new_format=False)
    change_date_rubric(rubrics_number=1279,new_year=1920,old_year=1919,cursor=cursor2,mydb=mydb2,new_format=True)
    change_date_rubric(rubrics_number=1279,new_year=1920,old_year=1919,cursor=cursor3,mydb=mydb3,new_format=False)

    change_date_rubric(rubrics_number=820,new_year=1900,old_year=1899,curosr=cursor,mydb=mydb,new_format=False)
    change_date_rubric(rubrics_number=820,new_year=1900,old_year=1899,curosr=cursor2,mydb=mydb2,new_format=True)
    change_date_rubric(rubrics_number=820,new_year=1900,old_year=1899,curosr=cursor3,mydb=mydb3,new_format=False)

    # close the connections
    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb2)
    db_connection.close_database_connection(mydb3)

# UNFLAGS CERTAIN THINGS WHICH SHOULD BE UNFLAGED
def unflag():
    for i in "DATA_SILSO_HISTO","BAD_DATA_SILSO","GOOD_DATA_SILSO":
        cursor,mydb = db_connection.database_connector(the_database=i)
        query="SELECT * FROM DATA WHERE FLAG=3 AND FK_RUBRICS!='NULL' AND FK_OBSERVERS!='NULL' AND GROUPS<60 AND SUNSPOTS<250"
        cursor.execute(query,())
        data=cursor.fetchall()
        ids=[]
        for j in data:
            ids.append(j[0])
        for j in ids:
            query="UPDATE DATA SET FLAG=1 WHERE ID="+str(j)
            cursor.execute()
            mydb.commit()
        db_connection.close_database_connection(mydb)

# ALIAS to 'Brunner Assistent'
def change_alias_to_brunner_assistent():
    brunner_assistent_rubrics=[1675,12503,12903,13003,13103,13203,
    13403,13502,13602,13702,13902,14002,14102,14202,14302,14402]
    # first do the old database
    cursor,mydb = db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    cursor3,mydb3 = db_connection.database_connector(the_database="BAD_DATA_SILSO")
    for rubrics_number in brunner_assistent_rubrics:
        query = "UPDATE DATA SET FK_OBSERVERS=191 WHERE FK_RUBRICS IN (SELECT RUBRICS_ID FROM RUBRICS WHERE RUBRICS_NUMBER="+str(rubrics_number)+")"
        cursor.execute(query,())
        mydb.commit()
        cursor3.execute(query,())
        mydb3.commit()
    # close these two databases
    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb3)

    # now do something a little more complicated for the new database
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")
    for rubrics_number in brunner_assistent_rubrics:
        query = "UPDATE DATA SET OBS_ALIAS='Brunner Assistent',FIRST_NAME='XXX',LAST_NAME='Brunner Assistent',COUNTRY='XXX',INSTRUMENT='8 cm open 64 increase' WHERE RUBRICS_NUMBER="+str(rubrics_number)
        cursor2.execute(query,())
        mydb2.commit()
    db_connection.close_database_connection(mydb2)


#flag_many_duplicates()
