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
def homogenise_uncertain(the_database="DATA_SILSO_HISTO"):
    ## n is the supremem of the set of ids
    #n = 206773

    uncertain=["Uncertain","Uncertain\n","Imprecise","LOW QUALITY",
        "Incertain","?","? (Résultats incertains)","?%","? Résultat incertain",
        "? Résultat incertaint","? Résultats incertains","Mauvais comptage",
        "mauvais comptage","Uncertain\n "]
    
    data = db_search.select_all_data(the_database=the_database)
    # connect to the database
    cursor,mydb = db_connection.database_connector(the_database=the_database)
    count=0
    for i in data:
        id_number=i[0]
        comment=i[8]
        if comment in uncertain:
            count+=1
            print("count:",count)
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

# homogenise_uncertain(the_database="BAD_DATA_SILSO")

#homogenise_uncertain()
#homogenise_typos()
#homogenise_null()

# here are method i am writing much later on 27 June right now

# for this one i make a list of '*' comments and their rubrics which 
# need correcting and correct them
def correct_asterix_comments():
    # [fk_rubrics,rubrics_numbeR,'proper comment']
    corrections = [(363,587,"* = secondary telescope"),
    (416,744,"* = hand telescope"),
    (424,627,"* = secondary telescope"),
    (450,800,"* = hand telescope"),
    (451,801,"* = hand telescope"),
    (462,809,"* = observation based on photograph"),
    (473,280,"* = hand telescope"),
    (477,281,"* = hand telescope"),
    (483,825,"* = hand telescope"),
    (504,843,"* = hand telescope"),
    (509,844,"* = hand telescope"),
    (511,845,"* = secondary telescope"),
    (513,847,"* = hand telescope"),
    (527,865,"* = hand telescope"),
    (591,906,"* = bad definition of the sun picture")]
    # last one is transliterated from german, i thought their
    # grammer was more concise so i didn't correct it

    cursor,mydb = db_connection.database_connector(the_database='DATA_SILSO_HISTO')
    cursor2,mydb2 = db_connection.database_connector(the_database='BAD_DATA_SILSO')

    for i in corrections:
        query = "UPDATE DATA SET COMMENT='"+i[2]+"' WHERE FK_RUBRICS="+str(i[0])+" AND COMMENT='*'"
        cursor.execute(query,())
        cursor2.execute(query,())
        mydb.commit()
        mydb2.commit()

    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb2)




