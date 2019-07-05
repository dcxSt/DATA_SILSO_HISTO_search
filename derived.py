# script with method to deal with (in general terms) the data which is derived
# from the umbra and the penumbra

# import statements
import numpy as np
import db_connection
import db_edit
import db_transfers


# method to move all the data-points flagged 7 into GOOD_DATA_SILSO
def move_7_to_good():
    # get the ids
    cursor3,mydb3 = db_connection.database_connector(the_database="BAD_DATA_SILSO")
    query = "SELECT ID FROM DATA WHERE FLAG=7"
    cursor3.execute(query,())
    fetched = cursor3.fetchall()
    id_numbers = []
    for i in fetched:
        id_numbers.append(i[0])
    
    # connect to the recipient's database
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")
    # move them from BAD_DATA_SILSO to GOOD_DATA_SILSO
    for i in id_numbers:
        db_transfers.db_transfer(id_number=i,cursor=cursor3,mydb=mydb3,cursor2=cursor2,mydb2=mydb2,close_connections=False)

    # close connections
    db_connection.close_database_connection(mydb3)
    db_connection.close_database_connection(mydb2)

# takes all carrington datapoints from rubric 303 that are in RUBBISH_DATA 
# moves them into DATA, in both DATA_SILSO_HISTO and GOOD_DATA_SILSO
def move_carrington_out_of_rubbish():
    # get the ids that are in rubbish in DATA_SILSO_HISTO (only this one is needed)
    cursor,mydb = db_connection.database_connector(the_database='DATA_SILSO_HISTO')
    query = "SELECT ID FROM RUBBISH_DATA WHERE FK_OBSERVERS=36 AND FLAG=7"
    cursor.execute(query,())
    fetched = cursor.fetchall()
    id_numbers = []
    for i in fetched:
        id_numbers.append(i[0])

    # connect to GOOD_DATA_SILSO
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")

    # for each of these move them out of RUBBISH_DATA and into DATA
    for i in id_numbers:
        db_transfers.move_data_out_of_bin(id_number=i,cursor=cursor,mydb=mydb,cursor2=cursor2,mydb2=mydb2,close_databases=False)

    # disconnect from databases
    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb2)


def move_carrington_to_good():
    # try insert if it doesn't work just give up, it's already there...
    # get the ids that are in DATA_SILSO_HISTO and belong to rubrics 303, fk=175
    cursor,mydb = db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    query = "SELECT ID FROM DATA WHERE FK_RUBRICS=175 AND FK_OBSERVERS=36"
    cursor.execute(query,())
    fetched = cursor.fetchall()
    id_numbers = []
    for i in fetched:
        id_numbers.append(i[0])

    # connect to GOOD_DATA_SILSO
    cursor2,mydb2 = db_connection.database_connector(the_database="GOOD_DATA_SILSO")

    # for each of these copy them from DATA into GOOD_DATA_SILSO
    for i in id_numbers:
        db_transfers.db_transfer(i,sender="DATA_SILSO_HISTO",recipient="GOOD_DATA_SILSO",cursor=cursor,mydb=mydb,cursor2=cursor2,mydb2=mydb2,close_connections=False,dont_delete=True)

    # disconnect from databases
    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb2)





