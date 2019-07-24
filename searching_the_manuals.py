# searching the manuals is work involving finding each comment,
# figuring out what it means, and dealing with the data appropriately

# import
import db_connection
import db_edit
import db_search
import pickle
import numpy as np


# this method is from dealing_with_duplicates.py but i copied it here
# because it deals with more fundamental operations that just duplicates
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
        print("in DATA_SILSO_HISTO copied into rubbish bin")#trace

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
    query = "SELECT * FROM DATA WHERE ID="+str(id_number)
    cursor2.execute(query,())
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
        print("in GOOD_DATA_SILSO copied into rubbish bin")#trace

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

# helper method for pink
def correct_typos_for_pink():
    # this method also partakes in the homogenisation of comments
    # makes dictionary with keys as incorrect and values as correct
    # also i'm taking out all accents because they are not very
    # international
    typos={}
    typos["* = très mauvaise définition"]="* = tres mauvaise definition"
    typos["* = se réfère aux observations de Mlle Olga Subbotin"]="* = Olga Subbotin"

    # correct these in both databases
    cursor,mydb=db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    cursor2,mydb2=db_connection.database_connector(the_database="BAD_DATA_SILSO")
    for i in typos:
        query="UPDATE DATA SET COMMENT='"+typos[i]+"' WHERE COMMENT='"+i+"';"
        cursor.execute(query,())
        cursor2.execute(query,())
        mydb.commit()
        mydb2.commit()
        print(i+" --> "+typos[i]+" DONE")
    print("The typos were set right")

    # disconnect
    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb2)

# pink is the colour for data with comments that have * = something and 
# the rest of the comments in the rubric are just marked *, so here we 
# homogenise them
def pink():
    """
    In this method I create a big list of things where we have 
    comments from the same rubric with shorthand comments and making 
    it so that all the comments that mean ttodayhe same things become the 
    same this does not deal with spelling errors"""
    
    # it's important to run typos first
    correct_typos_for_pink()

    # (rubric_number , comment , short-hand)
    suspects=[(752,"r=Ricco","r"),(757,"* = Wolfer P","*"),
    (758,"* = Broger-P","*"),(761,"* = Quimby P","*"),
    (767,"* = Jastremsky","*"),(768,"* = second instrument","*"),
    (777,"* = Wolfer P","*"),(778,"* = Broger P","*"),
    (783,"* = second instrument","*"),(866,"* = P","*"),
    (868,"* = telescope 2","*"),(868,"** = telescope 3","**"),
    (869,"* = P","*"),(871,"* = telescope 2","*"),
    (871,"** = telescope 3","**"),(874,"* = tres mauvaise definition","*"),
    (879,"* = N. Sykora","*"),(883,"m = Mazarella","m"),
    (889,"* = P","*"),(890,"* = P","*"),
    (892,"* = telescope 2","*"),(893,"* = P","*"),
    (895,"A = W. Abold","A"),(895,"S = Sykora","S"),
    (900,"* = direct observation","*"),(1046,"* = disk 10 cm","*"),
    (1033,"* = Olga Subbotin","*"),(13901,"Waldmeier","W"),
    (14001,"Waldmeier","W"),(14401,"Waldmeier","W")]

    # update the comments in both databases
    cursor,mydb=db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    cursor2,mydb2=db_connection.database_connector(the_database="BAD_DATA_SILSO")
    for i in suspects:
        # want to replace short comments with long comments
        rubrics_number = i[0]
        long_comment = i[1]
        short_comment = i[2]
        # find fk_rubrics
        query = "SELECT RUBRICS_ID FROM RUBRICS WHERE RUBRICS_NUMBER = "+str(rubrics_number)
        cursor.execute(query,())
        rubrics_id = cursor.fetchall()[0][0]
        # replace the comment
        query = "UPDATE DATA SET COMMENT='"+long_comment+"' WHERE FK_RUBRICS="+str(rubrics_id)+" AND COMMENT='"+short_comment+"'"
        cursor.execute(query,())
        cursor2.execute(query,())
        mydb.commit()
        mydb2.commit()
        print("\nupdated comment '",short_comment,"' to '",long_comment,
            "' for rubric number",rubrics_number," and rubrics id",rubrics_id)

    # disconnect
    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb2)


#def rubric_specific_corrections():
    # has a list that resembles pink but operates differently:
    # (rubric_number, correction, incorrect original comment)


def find_duplicate_observers(cursor=None,mydb=None,
the_database="DATA_SILSO_HISTO",close_connection=True):
    # returns a dictionary with key = alias -- value = list (obs_ids)

    cursor,mydb=db_connection.get_cursor(cursor=cursor,mydb=mydb,the_database=the_database)
    observers = db_search.select_all_observers() # this boy closes the connection
    
    duplicates={}
    for i in observers:
        alias = i[1]
        obs_id = i[0]
        if alias in duplicates:
            the_ids=duplicates[alias]
            the_ids.append(obs_id)
            duplicates[alias]=the_ids
        else:
            duplicates[alias]=[obs_id]

    print("Observer duplicates:")
    for i in duplicates:
        if len(duplicates[i])>1:
            print(i," = ",duplicates[i])

    if close_connection:
        db_connection.close_database_connection(mydb)
    return duplicates

def find_obs_id_by_date(data):
    # returns a dictionary with key = date -- value =
    # [(obs_id,datapoint id),(obs_id datapoint_id),...]
    obs_id_by_date={}
    for i in data:
        date = i[1]
        if date:
            datapoint_id = i[0]
            obs_id = i[3]
            if date in obs_id_by_date:
                the_observers = obs_id_by_date[date]
                the_observers.append((obs_id,datapoint_id))
                obs_id_by_date[date]=the_observers
            else:
                the_observers=[(obs_id,datapoint_id)]
                obs_id_by_date[date]=the_observers
    return obs_id_by_date

def find_observer_alias_by_id(observers):
    # returns a dictionary : key = id -- value = alias
    alias_by_id={}
    for i in observers:
        the_id = i[0]
        the_alias = i[1]
        alias_by_id[the_id] = the_alias
    return alias_by_id

# makes a dictionary of all the duplicated data by observer alias
def find_duplicates_data(the_database="DATA_SILSO_HISTO"):
    print("FINDING the duplicates...")
    # start by finding duplicates of data, so 2 data points with the 
    # same observer id, with the same 
    cursor,mydb=db_connection.database_connector(the_database=the_database)
    data = db_search.select_all_data()
    cursor,mydb=db_connection.database_connector(the_database=the_database)
    observers = db_search.select_all_observers()

    # dictionary of obs_ids searchable by date of observation
    obs_id_by_date = find_obs_id_by_date(data)

    # dictionary of obs_ids with the same alias
    duplicate_observers = find_duplicate_observers(the_database=the_database)

    # key = observer id -- value  = observer alias
    observer_alias_by_id = find_observer_alias_by_id(observers)

    # dictionary key = observer_alias -- value = list of duplicates
    # list = (id1, id2, date)
    data_duplicates = {}
    for date in obs_id_by_date:
        if date:
            # compare all the observer ids with each other for specified date
            for i in range(len(obs_id_by_date[date])-1):
                for j in range(i+1,len(obs_id_by_date[date])):
                    obs_alias1=observer_alias_by_id[obs_id_by_date[date][i][0]]
                    obs_alias2=observer_alias_by_id[obs_id_by_date[date][j][0]]
                    # if two alias are the same for the same date, add them to the duplicates list
                    if obs_alias1 == obs_alias2:
                        id1=obs_id_by_date[date][i][1]
                        id2=obs_id_by_date[date][j][1]
                        try:
                            duplicates_list=data_duplicates[obs_alias1]
                            duplicates_list.append((id1,id2,date))
                            data_duplicates[obs_alias1]=duplicates_list
                        except KeyError:
                            data_duplicates[obs_alias1]=[(id1,id2,date)]

    return data_duplicates

# makes a dictionary of all the duplicates by observer alias
# the following method is poorly written, slightly better version with it's successor
def greater_duplicates_data(the_database="DATA_SILSO_HISTO",force_recalculate=False):
    # if there is a pickles one out there, load it, else, create a dictionary and pickle it
    try:
        if force_recalculate==True:
            raise FileNotFoundError
        pickle_off = open("greater_duplicates_dictionary.pickle","rb")
        greater_duplicates_dictionary = pickle.load(pickle_off)
        pickle_off.close()
    except FileNotFoundError:
        # takes the duplicates data list and makes a better one
        print("Creating the greater duplicates data list")

        greater_duplicates_dictionary = {}

        data_duplicates = find_duplicates_data()
        cursor,mydb = db_connection.database_connector(the_database=the_database)
        deficient_rubrics_count=0
        for alias in data_duplicates:
            greater_duplicates_dictionary[alias] = []
            # for each duplicate add this to the greater list...
            for duplicate in data_duplicates[alias]:
                id1 = duplicate[0]
                id2 = duplicate[1]
                date = duplicate[2]

                # fetch the data
                query="SELECT * FROM DATA WHERE ID ="+str(id1)
                cursor.execute(query,())
                id1_data = cursor.fetchall()[0]

                fk_rubrics = id1_data[2]
                fk_observers = id1_data[3]

                try:
                    query="SELECT * FROM RUBRICS WHERE RUBRICS_ID="+str(fk_rubrics)
                    cursor.execute(query,())
                    rubrics_data = cursor.fetchall()[0]

                    rubrics_number = rubrics_data[1]
                    mitt_number = rubrics_data[2]
                    page_number = rubrics_data[3]
                    source = rubrics_data[4]
                except:
                    deficient_rubrics_count+=1
                    #print("fk_rubrics deficient, exception caught")
                    rubrics_number = "na"
                    mitt_number = "na"
                    page_number = "na"
                    fk_rubrics = "na"
                    source = "na"

                try:
                    query="SELECT * FROM OBSERVERS WHERE ID="+str(fk_observers)
                    cursor.execute(query,())
                    observer_data = cursor.fetchall()[0]

                    observer_alias = observer_data[1]
                    observer_instrument = observer_data[5]
                except:
                    print("fk_observer deficient, exception caught")
                    observer_alias = "na"
                    observer_instrument = "na"
                

                    

                groups = id1_data[4]
                sunspots = id1_data[5]
                wolf = id1_data[6]
                comment = id1_data[8]
                

                # make the new tuple (without source)
                tuple1=(id1,fk_observers,observer_alias,
                observer_instrument,fk_rubrics,rubrics_number,mitt_number,
                page_number,groups,sunspots,wolf,comment)


                ### --------------------------- ###

                query="SELECT * FROM DATA WHERE ID ="+str(id2)
                cursor.execute(query,())
                id2_data = cursor.fetchall()[0]

                fk_rubrics = id2_data[2]
                fk_observers = id2_data[3]

                # fetch the data
                try:
                    query="SELECT * FROM RUBRICS WHERE RUBRICS_ID="+str(fk_rubrics)
                    cursor.execute(query,())
                    rubrics_data = cursor.fetchall()[0]

                    rubrics_number = rubrics_data[1]
                    mitt_number = rubrics_data[2]
                    page_number = rubrics_data[3]
                    source = rubrics_data[4]
                except:
                    deficient_rubrics_count+=1
                    fk_rubrics = "na"
                    rubrics_number = "na"
                    mitt_number = "na"
                    page_number = "na"
                    source = "na"

                try:
                    query="SELECT * FROM OBSERVERS WHERE ID="+str(fk_observers)
                    cursor.execute(query,())
                    observer_data = cursor.fetchall()[0]

                    observer_alias = observer_data[1]
                    observer_instrument = observer_data[5]
                except:
                    fk_observers = "na"
                    observer_alias = "na"
                    observer_instrument = "na"
                

                groups = id2_data[4]
                sunspots = id2_data[5]
                wolf = id2_data[6]
                comment = id2_data[8]

                # make the new tuple (without source)
                tuple2=(id2,fk_observers,observer_alias,
                observer_instrument,fk_rubrics,rubrics_number,mitt_number,
                page_number,groups,sunspots,wolf,comment)

                # here you can see how i structured my dictionary
                greater_duplicates_dictionary[alias].append((date,tuple1,tuple2))

        # pickle it for later use
        pickling_on = open("greater_duplicates_dictionary.pickle","wb")
        pickle.dump(greater_duplicates_data,pickling_on)
        pickling_on.close()

    return greater_duplicates_dictionary

# duplicates by date dictionary is a better dictionary, returns the dictionary
# mostly copy pasted from greater_duplicates_data
def duplicates_by_date(the_database="DATA_SILSO_HISTO"):
    # takes the duplicates data list and makes a better one
    print("Creating the duplicates dictionary by date")

    duplicates_dictionary_by_date = {}

    data_duplicates = find_duplicates_data()
    cursor,mydb = db_connection.database_connector(the_database=the_database)
    for alias in data_duplicates:
        for duplicate in data_duplicates[alias]:
            id1 = duplicate[0]
            id2 = duplicate[1]
            date = duplicate[2]
            if not date:
                continue

            # fetch the data
            query="SELECT * FROM DATA WHERE ID ="+str(id1)
            cursor.execute(query,())
            id1_data = cursor.fetchall()[0]

            fk_rubrics = id1_data[2]
            fk_observers = id1_data[3]

            try:
                query="SELECT * FROM RUBRICS WHERE RUBRICS_ID="+str(fk_rubrics)
                cursor.execute(query,())
                rubrics_data = cursor.fetchall()[0]

                rubrics_number = rubrics_data[1]
                mitt_number = rubrics_data[2]
                page_number = rubrics_data[3]
                source = rubrics_data[4]
            except:
                fk_rubrics = "na"
                rubrics_number = "na"
                mitt_number = "na"
                page_number = "na"
                source = "na"

            try:
                query="SELECT * FROM OBSERVERS WHERE ID="+str(fk_observers)
                cursor.execute(query,())
                observer_data = cursor.fetchall()[0]

                observer_alias = observer_data[1]
                observer_instrument = observer_data[5]
            except:
                fk_observers = "na"
                observer_alias = "na"
                observer_instrument = "na"
            

                

            groups = id1_data[4]
            sunspots = id1_data[5]
            wolf = id1_data[6]
            comment = id1_data[8]
            date_insert = id1_data[9]
            flag = id1_data[10]
            

            # make the new tuple (without source)
            tuple1=(id1,fk_observers,observer_alias,
            observer_instrument,fk_rubrics,rubrics_number,mitt_number,
            page_number,source,groups,sunspots,wolf,comment,date_insert,flag)


            ### --------------------------- ###

            query="SELECT * FROM DATA WHERE ID ="+str(id2)
            cursor.execute(query,())
            id2_data = cursor.fetchall()[0]

            fk_rubrics = id2_data[2]
            fk_observers = id2_data[3]

            # fetch the data
            try:
                query="SELECT * FROM RUBRICS WHERE RUBRICS_ID="+str(fk_rubrics)
                cursor.execute(query,())
                rubrics_data = cursor.fetchall()[0]

                rubrics_number = rubrics_data[1]
                mitt_number = rubrics_data[2]
                page_number = rubrics_data[3]
                source = rubrics_data[4]
            except:
                fk_rubrics = "na"
                rubrics_number = "na"
                mitt_number = "na"
                page_number = "na"
                source = "na"

            try:
                query="SELECT * FROM OBSERVERS WHERE ID="+str(fk_observers)
                cursor.execute(query,())
                observer_data = cursor.fetchall()[0]

                observer_alias = observer_data[1]
                observer_instrument = observer_data[5]
            except:
                fk_observers = "na"
                observer_alias = "na"
                observer_instrument = "na"
            

            groups = id2_data[4]
            sunspots = id2_data[5]
            wolf = id2_data[6]
            comment = id2_data[8]
            date_insert = id1_data[9]
            flag = id1_data[10]

            # make the new tuple (without source)
            tuple2=(id2,fk_observers,observer_alias,
            observer_instrument,fk_rubrics,rubrics_number,mitt_number,
            page_number,source,groups,sunspots,wolf,comment,date_insert,flag)

            # here you can see how i structured my dictionary
            duplicates_dictionary_by_date[str(date)]=(tuple1,tuple2)

    return duplicates_dictionary_by_date

# this method takes as it's argument the list created by the last one
# and turns it into human readable format
def write_greater_duplicates_data_text(greater_duplicates_dictionary,
filename="greater_duplicates.txt",descriptor=None):
    print("Writing to file",filename)
    f = open(filename,"w")
    if descriptor:
        f.write(descriptor)
        f.write("\n\n")
    for observer in greater_duplicates_dictionary:
        f.write("Observer :   "+str(observer))
        f.write("\n")
        f.write("ID | fk_obs , obs_alias , obs_instrument | fk_rubrics , rubrics_num , mitt_num , page_num | groups , sunspots , wolf | comment")
        f.write("\n\n")
        count=0
        for i in greater_duplicates_dictionary[observer]:
            #count+=1
            #if count>5:
            #    break
            date=i[0]
            tuple1=i[1]
            tuple2=i[2]

            f.write(str(date))
            f.write("\n")
            f.write(str(tuple1[0]))
            f.write(" | ")
            f.write(str(tuple1[1]))
            f.write(" , ")
            f.write(str(tuple1[2]))
            f.write(" , ")
            f.write(str(tuple1[3]))
            f.write(" | ")
            f.write(str(tuple1[4]))
            f.write(" , ")
            f.write(str(tuple1[5]))
            f.write(" , ")
            f.write(str(tuple1[6]))
            f.write(" , ")
            f.write(str(tuple1[7]))
            f.write(" | ")
            f.write(str(tuple1[8]))
            f.write(" , ")
            f.write(str(tuple1[9]))
            f.write(" , ")
            f.write(str(tuple1[10]))
            f.write(" | ")
            f.write(str(tuple1[11]))
            f.write("\n")

            f.write(str(tuple2[0]))
            f.write(" | ")
            f.write(str(tuple2[1]))
            f.write(" , ")
            f.write(str(tuple2[2]))
            f.write(" , ")
            f.write(str(tuple2[3]))
            f.write(" | ")
            f.write(str(tuple2[4]))
            f.write(" , ")
            f.write(str(tuple2[5]))
            f.write(" , ")
            f.write(str(tuple2[6]))
            f.write(" , ")
            f.write(str(tuple2[7]))
            f.write(" | ")
            f.write(str(tuple2[8]))
            f.write(" , ")
            f.write(str(tuple2[9]))
            f.write(" , ")
            f.write(str(tuple2[10]))
            f.write(" | ")
            f.write(str(tuple2[11]))
            f.write("\n\n")

        f.write("\n-----------------------------------------\n")

    f.close()

# sorting the duplicates so that human can get better idea of what's going on
def sorting_duplicates(greater_duplicates_dictionary):
    # non mutually exclusive
    entered_twice_duplicates={}
    entered_differently_duplicates={}
    different_value_duplicates={}
    same_value_duplicates={}
    different_obs_id_duplicates={}
    same_obs_id_duplicates={}
    different_rubric_duplicates={}
    same_rubric_duplicates={}

    for alias in greater_duplicates_dictionary:
        entered_twice_duplicates[alias]=[]
        entered_differently_duplicates[alias]=[]
        different_value_duplicates[alias]=[]
        different_obs_id_duplicates[alias]=[]
        same_obs_id_duplicates[alias]=[]
        different_rubric_duplicates[alias]=[]
        same_rubric_duplicates[alias] = []
        same_value_duplicates[alias] = []
        for i in greater_duplicates_dictionary[alias]:
            # if the groups / sunspots / wolf numbers don't agree add to differnet value
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

            if groups1!=groups2 or sunspots1!=sunspots2 or wolf1!=wolf2:
                different_value_duplicates[alias].append(i)
            else:
                same_value_duplicates[alias].append(i)

            if obs_id1!=obs_id2:
                different_obs_id_duplicates[alias].append(i)
            else:
                same_obs_id_duplicates[alias].append(i)

            if fk_rubrics1!=fk_rubrics2:
                different_rubric_duplicates[alias].append(i)
            else:
                same_rubric_duplicates[alias].append(i)
            
            if groups1==groups2 and sunspots1==sunspots2 and wolf1==wolf2 and obs_id1==obs_id2 and fk_rubrics1==fk_rubrics2:
                entered_twice_duplicates[alias].append(i)
            else:
                entered_differently_duplicates[alias].append(i)
            
    # write the dictionaries to text files
    descriptor = "Duplicates which appeaer to be two exact copies of the same datapoint"
    write_greater_duplicates_data_text(entered_twice_duplicates,filename="entered_twice_duplicates.txt",descriptor=descriptor)
    
    descriptor = "Duplicates which are not quite the same as each other, these ones are more mysterious"
    write_greater_duplicates_data_text(entered_differently_duplicates,filename="entered_differently_duplicates.txt",descriptor=descriptor)
    
    descriptor = "Duplicates which have different sunspot values"
    write_greater_duplicates_data_text(different_value_duplicates,filename="different_value_duplicates.txt",descriptor=descriptor)

    descriptor = "Duplicates which have identical sunspot values"
    write_greater_duplicates_data_text(same_value_duplicates,filename="same_value_duplicates.txt",descriptor=descriptor)

    descriptor = "Duplicates with different observer ids but same observer alias"
    write_greater_duplicates_data_text(different_obs_id_duplicates,filename="different_obs_id_duplicates.txt",descriptor=descriptor)

    descriptor = "Duplicates with same observer ids"
    write_greater_duplicates_data_text(same_obs_id_duplicates,filename="same_obs_id_duplicates.txt",descriptor=descriptor)

    descriptor = "Duplicates with differing rubircs"
    write_greater_duplicates_data_text(different_rubric_duplicates,filename="different_rubric_duplicates.txt",descriptor=descriptor)

    descriptor = "Duplicates with same rubric as each other"
    write_greater_duplicates_data_text(different_obs_id_duplicates,filename="same_rubric_duplicates.txt",descriptor=descriptor)



# method moves everything flagged 3 into the bid
def move_flag3_to_bin():
    # find all the datapoints in DATA_SILSO_HISTO with flag 3
    cursor,mydb=db_connection.database_connector(the_database='DATA_SILSO_HISTO')
    cursor2,mydb2=db_connection.database_connector(the_database='GOOD_DATA_SILSO')
    cursor3,mydb3=db_connection.database_connector(the_database='BAD_DATA_SILSO')

    query = "SELECT ID FROM DATA WHERE FLAG=3"
    cursor.execute(query,())
    ids = cursor.fetchall()
    for id_number in ids:
        move_data_to_bin(id_number=id_number[0],cursor=cursor,mydb=mydb,cursor2=cursor2,mydb2=mydb2,cursor3=cursor3,mydb3=mydb3,close_databases=False)

    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb2)
    db_connection.close_database_connection(mydb3)
#move_flag3_to_bin()


"""
greater_duplicates_dictionary = greater_duplicates_data(the_database='DATA_SILSO_HISTO',force_recalculate=True)
write_greater_duplicates_data_text(greater_duplicates_dictionary=greater_duplicates_dictionary)
sorting_duplicates(greater_duplicates_dictionary)
"""