# here is where my tests are, these search the database and comment and flag etc.

import db_connection
import db_search
import db_edit
import file_io

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
            boolean=db_edit.comment(i,"incorrect_wolf_calculation",cursor,mydb,replace=False)
            print(boolean)

    return incorrect_wolf_ids

# flags everything with bad comments
def flag_bad_comments():
    # define a list of bad comments
    bad_comments=["Uncertain","Imprecise","LOW QUALITY",
    "Incertain"]



### testing
##ids=incorrect_wolf_test(flag_and_comment=True)
##for i in ids:
##    print("id:",i)