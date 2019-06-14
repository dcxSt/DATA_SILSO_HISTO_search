# utility methods used search the DATA_SILSO_HISTO sql database

# import statements
import mysql.connector
import numpy as np
import db_connection
import file_io


### selects all data in columns in DATA are returns it
def select_all_data(cursor=None,mydb=None):
    cursor,mydb=db_connection.get_cursor(cursor,mydb)
    query = "SELECT * FROM DATA"
    cursor.execute(query,params=())
    data = cursor.fetchall()
    print("data successfully retrieved")

    # close the connection
    db_connection.close_database_connection(mydb)
    return data

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

different_comments(file_name="gggg.txt")


### tests
##data=select_all_data()
##print("\n\n",len(data),"\n\n")
##print(data[100])
