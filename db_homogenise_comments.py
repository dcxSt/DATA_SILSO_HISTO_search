# homogenise comments, when executed homogenises all comments to their 'group'

# import statements
import db_edit
import db_connection
import db_search
import file_io





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

# checked
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
    for i in data:
        id_number=i[0]
        comment=i[8]
        if comment in uncertain:
            db_edit.set_comment(id_number,"uncertain",cursor=cursor,mydb=mydb,replace=True)
    
    # close the connection
    db_connection.close_database_connection(mydb=mydb)

def homogenise_null():
    no_comment=["None","NULL","\t","\n"," ","  ","   "]
    data = db_search.select_all_data()
    cursor,mydb=db_connection.database_connector()
    for i in data:
        id_number=i[0]
        comment=i[8]
        if comment in no_comment:
            db_edit.set_comment(id_number,comment="",cursor=cursor,mydb=mydb,replace=True)
    db_connection.close_database_connection(mydb=mydb)

def homogenise_typos():
    S_et_W=["S et W","S et W "]
    schwabe=["Schwabe","schwabe"]
    wolf=["Wolf","wolf","wolfw"]
    leppig=["Leppig","leppig"]
    zucconi=["Zucconi","zucconi","ZUCCONI"]
    change_of_instrument=["change of instrument","Change of instrument"]
    mascari=["Mascari","mascari"]
    schwarzenbrunner=["*=Schwarzenbrunner","*=schwarzenbrunner"]
    waldmeier=["Waldmeier",
    "waldmeier",
    "W Analyse faite par Waldmeier",
    "W Etude faite par Waldmeier",
    "W Etude faite pas Waldmeier",
    "? Etude faite pas Waldmeier",
    "W = Etude faite pas Waldmeier",
    "W = Etude faite par Waldmeier",]
    to_change=[S_et_W,schwabe,wolf,leppig,zucconi,change_of_instrument,
    mascari,schwarzenbrunner,waldmeier]
    
    data = db_search.select_all_data()
    cursor,mydb=db_connection.database_connector()
    for i in data:
        id_number=i[0]
        comment=i[8]
        for j in to_change:
            if comment in j:
                db_edit.set_comment(id_number,j[0],cursor=cursor,mydb=mydb,replace=True)
    db_connection.close_database_connection(mydb=mydb)


#homogenise_uncertain()
#homogenise_typos()
#homogenise_null()
