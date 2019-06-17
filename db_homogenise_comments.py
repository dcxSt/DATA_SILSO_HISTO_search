# homogenise comments, when executed homogenises all comments to their 'group'

# import statements
import db_edit
import db_connection
import db_search
import file_io

uncertain=["Uncertain","Uncertain\n","Imprecise","LOW QUALITY",
    "Incertain","?","? (Résultats incertains)","?%","? Résultat incertain",
    "? Résultat incertaint","? Résultats incertains","Mauvais comptage",
    "mauvais comptage"]

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

def homogenise_uncertain():
    # n is the supremem of the set of ids
    n = 
    
    # setup a connection 
    cursor,mydb = db_connection.database_connector()


    # stop the connection

