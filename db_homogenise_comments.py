# homogenise comments, when executed homogenises all comments to their 'group'

# import statements
import db_edit
import db_connection
import db_search
import file_io



null=["None","","NULL","\t","\n"," ","  ","   "]

star=["*","*%"]
w_waldmeier=["W Analyse faite par Waldmeier","W Etude faite par Waldmeier",
"W Etude faite pas Waldmeier","W = Etude faite pas Waldmeier",
"W = Etude faite par Waldmeier","Waldmeier"]

"""
for all numbers in howevery big the database is:
    if there is a data with the id number:
        if there is a comment in this data point:
            comment = ...
            if comment in one of the things"""

# checked or unchecked
def homogenise_uncertain():
    ## n is the supremem of the set of ids
    #n = 206773

    uncertain=["Uncertain","Uncertain\n","Imprecise","LOW QUALITY",
        "Incertain","?","? (Résultats incertains)","?%","? Résultat incertain",
        "? Résultat incertaint","? Résultats incertains","Mauvais comptage",
        "mauvais comptage","uncertain"]
    
    data = db_search.select_all_data()
    # connect to the database
    cursor,mydb = db_connection.database_connector()
    print(data[9][8])
    for i in data:
        id_number=i[0]
        comment=i[8]
        if comment in uncertain:
            db_edit.set_comment(id_number,"uncertain",cursor=cursor,mydb=mydb,replace=True)
    
    # close the connection
    db_connection.close_database_connection(mydb=mydb)


#homogenise_uncertain()