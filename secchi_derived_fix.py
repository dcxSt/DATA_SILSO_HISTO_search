# rectification des donnes mal rentre de Herr Professor Secchi

import db_search
import db_edit
import db_connection

# find all comments from secchi with the comment derived in it
def find_comments_derived():
    # connect
    cursor,mydb=db_connection.database_connector()
    query="SELECT * FROM DATA d WHERE d.FK_OBSERVERS=49 AND d.COMMENT LIKE 'derived%'"
    cursor.execute(query,())
    secchi_data=cursor.fetchall()
    db_connection.close_database_connection(mydb=mydb)
    return secchi_data


def secchi_derived_fix():
    secchi_data=find_comments_derived()
    secchi_ids=[]
    true_sunspots={}
    groups_number={}

    numbers="1234567890"
    for i in secchi_data:
        secchi_ids.append(i[0])
        derived_number=int(i[8][8:])
        true_sunspots[i[0]]=derived_number
        groups_number[i[0]]=int(i[4])
    
    # fix SUNSPOTS, WOLF and COMMENTS (leave comments for now...)
    # fix SUNSPOTS
    cursor,mydb=db_connection.database_connector()
    for i in secchi_ids:
        db_edit.set_sunspots(i,true_sunspots[i],replace=True,cursor=cursor,mydb=mydb)
        wolf=true_sunspots[i]+10*groups_number[i]
        db_edit.set_wolf(i,wolf,replace=True,cursor=cursor,mydb=mydb)
    
    