# here is where my tests are, these search the database and comment and flag etc.

import db_connection
import db_search
import db_edit
import file_io
import db_homogenise_comments

# not certain if necessary
import mysql.connector

# finds where there are incorrectly calculated wolf numbers
# flags and comments the incorrect_wolf_indices (of which there is only one)
# returns list of ids where wolf is incorrectly calculated
def incorrect_wolf_test(cursor=None,mydb=None,flag_and_comment=False):
    cursor,mydb = db_connection.get_cursor(cursor,mydb)
    data = db_search.select_all_data(cursor,mydb)
    
    # find the incorrect wolf numbers
    incorrect_wolf_indices=[]
    defective_data_indices=[]
    no_wolf_calculated_indices=[]
    
    for i in range(len(data)):
        if data[i][4]!=None and data[i][5]!=None and data[i][6] == None:
            no_wolf_calcualted_indices.append(i)
        elif data[i][4]==None or data[i][5]==None or data[i][6]==None:
            defective_data_indices.append(i)
        elif data[i][4]*10+data[i][5]!=data[i][6]:
            incorrect_wolf_indices.append(i)
            
    # display the incorrect_wolf_indices data    
    print("\nfound",len(incorrect_wolf_indices),"incorrectly calculated wolf numbers")
    print("ID    Group  Sunspots  Wolf  calculated wolf")
    for i in incorrect_wolf_indices:
        print(data[i][0],"\t",data[i][4],"\t",data[i][5],"\t",data[i][6],"\t",data[i][4]*10+data[i][5])
    
    incorrect_wolf_ids=[]
    for i in incorrect_wolf_indices:
        incorrect_wolf_ids.append(data[i][0])
    
    # reconnect to the database, i think i did something silly and disconected
    cursor,mydb = db_connection.get_cursor()
    # FLAG AND COMMENT 
    if flag_and_comment:
        for i in incorrect_wolf_ids:
            # flag it
            db_edit.set_flag(i,cursor,mydb)
            # comment it
            boolean=db_edit.set_comment(i,"incorrect_wolf_calculation",cursor,mydb,replace=False)
            print(boolean)

    return incorrect_wolf_ids

# flags everything with bad comments
def flag_bad_comments():
    # bad_comments = comments to flag
    bad_comments=["Uncertain","Uncertain\n","Imprecise","LOW QUALITY",
        "Incertain","XXX - Wrong Rubric and/or Observer","Nbre entre parenthése",
        "?","val. déduites","incorrect_wolf_calculation","Change of instrument",
        "change of instrument","*","*%","Mauvais comptage","mauvais comptage",]
    
    cursor,mydb=db_connection.database_connector()
    data = db_search.select_all_data(cursor,mydb)
    # reconnect cause data disconnects you
    cursor,mydb=db_connection.database_connector()
    for i in range(len(data)):
        comment=data[i][8]
        if comment:
            if comment in bad_comments or comment[0]=="*":
                id_number=data[i][0]
                db_edit.set_flag(id_number,cursor,mydb)

    db_connection.close_database_connection(mydb)

    
# flags and comments everything in data that has 
# a rubricsid that doesn't correspond to a real rubrics id...
"""
i accidentally stumbled on this one when trying to compile my comments sheet
"""
def incorrect_rubrics_id():
    data=db_search.select_all_data()
    rubrics=db_search.select_all_rubrics()

# flags all comments in BAD_DATA_SILSO that looks even mildly suspicious
def big_flag(the_database="BAD_DATA_SILSO"):
    cursor,mydb=db_connection.database_connector(the_database=the_database)
    data = db_search.select_all_data(cursor,mydb)
    # reconnect cause data disconnects you
    cursor,mydb=db_connection.database_connector(the_database=the_database)

    flags_set=0
    already_flags=0

    for i in range(len(data)):
        
        if i%5000==0:
            print("count ~",i)
        # copy past from db_transfer
        info=data[i]
        flag = info[10]
        if flag==1:
            already_flags+=1
            continue
        id_number=info[0]
        comment = info[8]
        if comment:
            db_edit.set_flag(id_number=id_number,cursor=cursor,mydb=mydb,close_connection=False)
            flags_set+=1
            continue
        date = info[1]
        if not date:
            db_edit.set_flag(id_number=id_number,cursor=cursor,mydb=mydb,close_connection=False)
            flags_set+=1
            db_edit.set_comment(id_number=id_number,comment="no date",cursor=cursor,mydb=mydb)
            continue
        fk_rubrics = info[2]
        if not fk_rubrics and fk_rubrics!=0:
            db_edit.set_flag(id_number=id_number,cursor=cursor,mydb=mydb,close_connection=False)
            flags_set+=1
            db_edit.set_comment(id_number=id_number,comment="no fk_rubrics",cursor=cursor,mydb=mydb)
            continue
        groups = info[4]
        if not groups and groups!=0:
            db_edit.set_flag(id_number=id_number,cursor=cursor,mydb=mydb,close_connection=False)
            flags_set+=1
            db_edit.set_comment(id_number=id_number,comment="no groups",cursor=cursor,mydb=mydb)
            continue
        sunspots = info[5]
        #if not sunspots and sunspots!=0:
         #   db_edit.set_flag(id_number=id_number,cursor=cursor,mydb=mydb,close_connection=False)
          #  flags_set+=1
           # db_edit.set_comment(id_number=id_number,comment="no sunspots",cursor=cursor,mydb=mydb)
            #continue
        wolf = info[6]
        if not wolf and wolf !=0:
            db_edit.set_flag(id_number=id_number,cursor=cursor,mydb=mydb,close_connection=False)
            flags_set+=1
            db_edit.set_comment(id_number=id_number,comment="no wolf",cursor=cursor,mydb=mydb)
            continue
        fk_observers=info[3]
        # get the observer information
        query="SELECT * FROM OBSERVERS o WHERE o.ID="+str(fk_observers)
        cursor.execute(query,())
        info = cursor.fetchall()[0]
        obs_alias = info[1]
        if not obs_alias:
            db_edit.set_flag(id_number=id_number,cursor=cursor,mydb=mydb,close_connection=False)
            db_edit.set_comment(id_number=id_number,comment="no obs_alias",cursor=cursor,mydb=mydb)
            flags_set+=1
            continue
        
        # get the rubrics information
        query="SELECT * FROM RUBRICS r WHERE r.RUBRICS_ID="+str(fk_rubrics)
        cursor.execute(query,())
        info = cursor.fetchall()[0]
        rubrics_number = info[1]
        if not rubrics_number and rubrics_number!=0:
            db_edit.set_flag(id_number=id_number,cursor=cursor,mydb=mydb,close_connection=False)
            flags_set+=1
            continue
        #mitt_number = info[2]
        #page_number = info[3]
        #rubrics_source = info[4]
        #rubrics_source_date = info[5]
    
    db_connection.close_database_connection(mydb)




def count_flags(the_database="DATA_SILSO_HISTO"):
    cursor,mydb=db_connection.database_connector(the_database=the_database)
    data = db_search.select_all_data(cursor,mydb)
    no_flags=0
    for i in data:
        if i[10]==1:
            no_flags+=1
    return no_flags




