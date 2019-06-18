# utility methods used search the DATA_SILSO_HISTO sql database

# import statements
import mysql.connector
import numpy as np
import db_connection
import file_io
import pickle


### selects all data in columns in DATA are returns it in list format
def select_all_data(cursor=None,mydb=None):
    cursor,mydb=db_connection.get_cursor(cursor,mydb)
    query = "SELECT * FROM DATA"
    cursor.execute(query,params=())
    data = cursor.fetchall()
    print("data successfully retrieved")

    # close the connection
    db_connection.close_database_connection(mydb)
    return data

### selects all columns in RUBRIC
def select_all_rubrics():
    cursor,mydb=db_connection.database_connector()
    query = "SELECT * FROM RUBRICS"
    cursor.execute(query,())
    rubrics = cursor.fetchall()
    print("rubrics sucessfully retrieved")

    # close the connection
    db_connection.close_database_connection(mydb=mydb)
    return rubrics

### selects all columns in OBSERVERS
def select_all_observers():
    cursor,mydb=db_connection.database_connector()
    query = "SELECT * FROM OBSERVERS"
    cursor.execute(query,())
    observers = cursor.fetchall()
    print("observers sucessfully retrieved")

    # close the connection
    db_connection.close_database_connection(mydb=mydb)
    return observers

### searches database for comments and saves them all into a text file
def different_comments(cursor=None,mydb=None,file_name="comments.txt"):
    cursor,mydb = db_connection.get_cursor(cursor,mydb)
    ### returns all the different types of comment there are and saves them to a text-file
    all_comments=[]
    ### and a dictionary with the frequency of comment, with comments as keys
    #all_comments_and_frequency={}
    
    id_number=3
    query="SELECT * FROM DATA d WHERE d.ID=%s"
    cursor.execute(query % (str(id_number)))
    returned=cursor.fetchall()
    
    while id_number<=206772:
        if returned:
            comment=str(returned[0][8])
            if comment not in all_comments:
                #all_comments_and_frequency[comment]=1
                all_comments.append(comment)
            else:
                #all_comments_and_frequency[comment]+=1
                pass
        id_number+=1
        cursor.execute(query % (str(id_number)))
        returned=cursor.fetchall()
        
    print("\nFound a total of",len(all_comments),"distinct comments")
    text_file = open(file_name,"w")
    for i in all_comments:
        text_file.write(i)
        #freq=all_comments_and_frequency[i]
        #text_file.write(" "+str(freq)+"\n")
    text_file.close()
    print("\nThe comments have been written to the file",file_name)
    
    db_connection.close_database_connection(mydb)

### sorts the comments by rubric and saves it into human-readable files
### it also picles some dodgy data
def more_efficient_sort_comments_by_rubric():
    # select all from DATA_SILSO_HISTO and bring it into data...
    data = select_all_data()
    rubrics = select_all_rubrics()
    observers = select_all_observers()
    print(rubrics[0])
    print(observers[0])

    greater_comments_list=[]
    to_flag=[]
    count=0
    for d in data:
        count+=1
        if count%25000==0: # just for display so we can see how fast it's running
            print("count:",count)
        comment=d[8]
        if comment:
            rubrics_id=d[2]
            # define the rubrics number, mitt number, page number
            rubrics_number=None
            mitt_number=None
            page_number=None
            for i in rubrics:
                if i[0]==rubrics_id:
                    rubrics_number=i[1]
                    mitt_number=i[2]
                    page_number=i[3]
                    break
            if not rubrics_number and rubrics_number!=0:
                # cannot set flag otherwise im importing something that imports this program
                print("rubrics id=",rubrics_id)
                if rubrics_id=='NULL' or rubrics_id=='None' or not rubrics_id:
                    rubrics_id='NULL'
                    rubrics_id=-1#
                rubrics_number='undef'
                mitt_number='undef'
                page_number='undef'
                to_flag.append(d[0])
                print("error RUBRICS id=",d[0])
                print("rubrics id=",rubrics_id)
                print()
                
                """
                db_edit.set_flag(d[0],cursor,mydb)
                print(rubrics_id)
                print("flag set")
                db_edit.set_comment(d[0],"rubrics_id_incorrect",cursor,mydb)
                print("comment set")"""
            # define the observer id
            observer_id=d[3]
            # define the observer alias
            observer_alias=None
            for o in observers:
                if o[0]==observer_id:
                    observer_alias=o[1]
            if not observer_alias:
                print("error OBSERVER id=",d[0])
                observer_alias='undefined->check observer id'
                to_flag.append(d[0])
                
                """
                print(observer_id)
                db_edit.set_flag(d[0],cursor,mydb)
                print("flag set")
                db_edit.set_comment(d[0],"rubrics_id_incorrect",cursor,mydb)
                print("comment set")"""
            
            # add the comment to the list in a correct position
            # remember the greater_comments_list has sublists etc.
            if greater_comments_list:
                for sublist in greater_comments_list:
                    # add the comment to the list
                    # if there is already an entry for this rubrics_id
                    if sublist[0][0]==rubrics_id:
                        for j in sublist:
                            if j[6]==comment and j[4]==observer_id:
                                j[7]+=1
                                break
                        else:# only executed if the for loop did NOT break
                            sublist.append([rubrics_id,rubrics_number,mitt_number,page_number,observer_id,observer_alias,comment,1])
                        break
                else: #only executed if the for loop did NOT break
                    greater_comments_list.append([[rubrics_id,rubrics_number,mitt_number,page_number,observer_id,observer_alias,comment,1]])
            else:
                greater_comments_list=[[[rubrics_id,rubrics_number,mitt_number,page_number,observer_id,observer_alias,comment,1]]]

    # now that we have our greater_comments_list
    print("\nPickling the greater comments list")
    with open("greater_comments_list2.pkl","wb") as g:
        pickle.dump(greater_comments_list,g)
    print("pickling tht to_flag list")
    with open("to_flag.pkl","wb") as g:
        pickle.dump(to_flag,g)
    
    print("writing the greater comments list in .txt format")
    f=open("greater_comments_list2.txt","w")
    for i in greater_comments_list:
        f.write("\n")
        for j in i:
            rubrics_id,rubrics_number,observer_id,observer_alias,comment,freq=str(j[0]),str(j[1]),str(j[2]),str(j[3]),str(j[4]),str(j[5])
            f.write(rubrics_id)
            f.write("  ")
            f.write(rubrics_number)
            f.write("\t")
            f.write(observer_id)
            f.write(" ")
            f.write(observer_alias)
            f.write(" - ")
            f.write(comment)
            f.write(" | ")
            f.write(freq)
            f.write("\n")
    f.close()

    greater_comments_list.sort()
    print("writing the sorted greater comments list in .txt format")
    f=open("sorted_greater_comments_list.txt","w")
    for i in greater_comments_list:
        f.write("\n")
        for j in i:
            rubrics_id,rubrics_number,mitt_number,page_number,observer_id,observer_alias,comment,freq=str(j[0]),str(j[1]),str(j[2]),str(j[3]),str(j[4]),str(j[5]),str(j[6]),str(j[7])
            f.write(rubrics_id)
            f.write("  ")
            f.write(rubrics_number)
            f.write("  ")
            f.write(mitt_number)
            f.write("  ")
            f.write(page_number)
            f.write("  |  ")
            f.write(observer_id)
            f.write("   ")
            f.write(observer_alias)
            f.write(" - ")
            f.write(comment)
            f.write(" | ")
            f.write(freq)
            f.write("\n")
    f.close()

### finds all the data with missing rubrics
def missing_rubric():
    data = select_all_data()
    missing_rubric=[]
    for d in data:
        if (not d[2] or d[2]=='NULL') and d[2]!=0:
            missing_rubric.append((d[0],str(d[1]),d[2],d[3],d[8],str(d[9])))
    for i in missing_rubric:
        print(i)
    print("\nlen(missing_rubric)",len(missing_rubric))
    print("len(data)",len(data))



#missing_rubric()
#more_efficient_sort_comments_by_rubric()


### tests
##data=select_all_data()
##print("\n\n",len(data),"\n\n")
##print(data[100])


###different_comments(file_name="gggg.txt")