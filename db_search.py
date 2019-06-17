# utility methods used search the DATA_SILSO_HISTO sql database

# import statements
import mysql.connector
import numpy as np
import db_connection
import file_io
import pickle
import db_edit


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

"""
for each rubric, make a list to be written to text file and append it...

for each rubric:
    for each data point with this rubric id:
        if there is a comment
        find the observer
        !!!if the comment and observer are already on the list, add 1 to the freqency
        if the comment and the observer are not on the list, add them to the list with freq 1
    once you have done this, add this list to the bigger list
"""

def sort_comments_by_rubric():
    
    # select all from DATA_SILSO_HISTO and bring it into data...
    data = select_all_data()
    rubrics = select_all_rubrics()
    observers = select_all_observers()


    # make a list where each element is a list comprised of :
    # comments_list_entry : [rubric id, rubric number, observer id, observer alias, 
    # comment, total number of appearences]
    greater_comments_list=[]
    for r in rubrics:
        comments_list=[] 
        # comments_list [[rubric_id,rubric_number,observer_id,observer alias,comment,no app]]
        rubrics_id=r[0]
        rubrics_number=r[1]
        print("Checking rubrics_id",rubrics_id,"; rubrics_number",rubrics_number)
        for d in data:
            # for each data point with this rubric id
            if d[2]==rubrics_id:
                comment=d[8]
                # if there is a comment find the observer
                if comment:
                    observer_id = d[3]
                    # find the observer
                    observer_alias=None
                    for o in observers:
                        if o[0]==observer_id:
                            observer_alias=o[1]
                            break
                    if not observer_alias:
                        print("Exception raised!")
                        print("It seems there is an observer id in the data \
                            the has no corresponding observer id in the observer list!")
                        raise Exception
                    # if there is no list add them
                    if not comments_list:
                        comments_list.append([rubrics_id,rubrics_number,observer_id,
                        observer_alias,comment,1])
                    # if the comment and the observer are not on the list add them
                    else:
                        # loop through the list to find if they are on the
                        for entry in comments_list:
                            if entry[0]==rubrics_id and entry[1]==rubrics_number and entry[2]==observer_id and entry[4]==comment:
                                entry[5]+=1
                            break
                        else:
                            # if the loop did not break, then add entry to the comments list
                            comments_list.append([rubrics_id,rubrics_number,observer_id,
                            observer_alias,comment,1])
        if comments_list:
            greater_comments_list.append(comments_list)
    with open("greater_comments_list.pkl","wb") as g:
        pickle.dump(greater_comments_list,g)
    #with open("greater_comments_list.pkl","rb") as g:
    #    greater_comments_list = pickle.load(g)
    
    # now that we have the greater_comments_list i will append the comments list 
    # i will write it to a text file
    f = open("greater_comments_list.txt","w")
    for i in greater_comments_list:
        f.write("\n")
        if i:# shouldn't need this if all well...
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
        else:
            print("Error, there is an empty list in greater_comments_list")
    f.close()


def more_efficient_sort_comments_by_rubric():
    # select all from DATA_SILSO_HISTO and bring it into data...
    data = select_all_data()
    rubrics = select_all_rubrics()
    observers = select_all_observers()
    print(rubrics[0])
    print(observers[0])

    greater_comments_list=[]
    for d in data:
        comment=d[8]
        if comment:
            rubrics_id=d[2]
            # define the rubrics number
            rubrics_number=None
            for i in rubrics:
                if i[0]==rubrics_id:
                    rubrics_number=i[1]
                    break
            if not rubrics_number and rubrics_number!=0:
                # flag it
                db_edit.set_flag(d[0],cursor,mydb)
                print(rubrics_id)
                print("flag set")
                db_edit.set_comment(d[0],"rubrics_id_incorrect",cursor,mydb)
                print("comment set")
            # define the observer id
            observer_id=d[3]
            # define the observer alias
            observer_alias=None
            for o in observers:
                if o[0]==observer_id:
                    observer_alias=o[1]
            if not observer_alias:
                print(observer_id)
                db_edit.set_flag(d[0],cursor,mydb)
                print("flag set")
                db_edit.set_comment(d[0],"rubrics_id_incorrect",cursor,mydb)
                print("comment set")
            
            # add the comment to the list in a correct position
            # remember the greater_comments_list has sublists etc.
            if greater_comments_list:
                for i in greater_comments_list:
                    # add the comment to the list
                    # if there is already an entry for this rubrics_id
                    if i[0][0]==rubrics_id:
                        for j in i:
                            if j[4]==comment and j[2]==observer_id:
                                j[5]+=1
                                break
                        else:# only executed if the for loop did NOT break
                            j.append([rubrics_id,rubrics_number,observer_id,observer_alias,comment,1])
                        break
                else: #only executed if the for loop did NOT break
                    greater_comments_list.append([[rubrics_id,rubrics_number,observer_id,observer_alias,comment,1]])
            else:
                greater_comments_list.append([[rubrics_id,rubrics_number,observer_id,observer_alias,comment,1]])

    # now that we have our greater_comments_list
    with open("greater_comments_list2.pkl","wb") as g:
        pickle.dump(greater_comments_list,g)
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
            



more_efficient_sort_comments_by_rubric()


### tests
##data=select_all_data()
##print("\n\n",len(data),"\n\n")
##print(data[100])


###different_comments(file_name="gggg.txt")