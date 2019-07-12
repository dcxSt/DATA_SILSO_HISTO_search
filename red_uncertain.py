# script that deals with the data marked 'red questionmark'

import db_connection
import db_transfers
import pickle
import db_search

# defines a list of question marks:
# (rubrics_id,rubrics_number,obs_id,obs_alias,comment)
def get_question_marks():
    question_marks=[(171,294,45,'Tacchini','uncertain'),
    (316,484,45,'Tacchini','uncertain'),
    (318,481,55,'Denza','uncertain'),
    (326,676,101,'Catina 1 - Ricco - Mascari','uncertain'),
    (4,4,4,"Rumovski","Uncertain"),
    (4,4,4,"Rumovski","uncertain"),
    (7,7,6,"Vagetius","uncertain"),
    (171,294,45,"Tacchini","uncertain"),
    (316,484,45,"Tacchini","uncertain"),
    (318,481,55,"Denza","uncertain"),
    (326,676,101,"Ricco - Mascari","uncertain"),
    (451,801,117,"Broger","uncertain"),
    (452,802,69,"Winkler","uncertain"),
    (456,758,104,"Broger","uncertain"),
    (458,806,106,"Mascari","uncertain"),
    (460,759,69,"Winkler","uncertain"),
    (477,821,117,"Broger","uncertain"),
    (485,826,106,"Mascari","uncertain"),
    (487,769,106,"Mascari","uncertain"),
    (491,643,122,"Wolfer, Mooser ","uncertain"),
    (509,844,104,"Broger","uncertain"),
    (528,777,56,"Wolfer","uncertain"),
    (529,778,117,"Broger","uncertain"),
    (530,779,69,"Mascari","uncertain"),
    (539,787,106,"Mascari","uncertain"),
    (550,868,69,"Winkler","uncertain"),
    (556,874,94,"Guillaume","uncertain"),
    (568,883,56,"Mascari","uncertain"),
    (569,889,56,"Wolfer","uncertain"),
    (570,890,117,"Broger","uncertain"),
    (572,892,69,"Winkler","uncertain"),
    (578,898,113,"Kleiner","uncertain"),
    (590,905,124,"Subbotin","uncertain"),
    (593,908,101,"Catania 1 - Ricco - Mascari","uncertain"),
    (550,868,69,"Winkler","uncertain"),
    (556,874,132,"Guillaume","uncertain"),
    (568,883,106,"Mascari","uncertain"),
    (569,889,56,"Wolfer","uncertain"),
    (570,890,117,"Broger","uncertain"),
    (572,892,113,"Kleiner","uncertain"),
    (590,905,124,"Subbotin","uncertain"),
    (593,908,101,"Catania 1 - Ricco - Mascari","uncertain"),
    (954,1031,132,"Guillaume","uncertain"),
    (960,1037,101,"Catania 1 - Ricco - Mascari","uncertain"),
    (961,12902,117,"Broger","uncertain"),
    (963,12904,178,"Buser","uncertain"),
    (964,13001,177,"Brunner","uncertain"),
    (967,13004,178,"Buser","uncertain"),
    (968,13101,177,"Brunner","uncertain"),
    (969,13102,104,"Broger","uncertain"),
    (970,13103,177,"Brunner","uncertain"),
    (972,13201,177,"Brunner","uncertain"),
    (973,13202,117,"Broger","uncertain"),
    (974,13203,177,"Brunner","uncertain"),
    (975,13204,178,"Buser","uncertain"),
    (976,13401,177,"Brunner","uncertain"),
    (977,13402,117,"Broger","uncertain"),
    (978,13403,177,"Brunner","uncertain"),
    (979,13404,178,"Buser","uncertain"),
    (980,13501,177,"Brunner","uncertain"),
    (981,13502,177,"Brunner","uncertain"),
    (982,13503,189,"Waldmeier","uncertain"),
    (983,13504,178,"Buser","uncertain"),
    (984,13601,177,"Brunner","uncertain"),
    (985,13602,177,"Brunner","uncertain"),
    (987,13604,178,"Buser","uncertain"),
    (990,13703,189,"Waldmeier","uncertain"),
    (992,13902,177,"Brunner","uncertain"),
    (994,14002,177,"Brunner","uncertain"),
    (995,14101,177,"Brunner","uncertain"),
    (996,14102,177,"Brunner","uncertain"),
    (997,14103,190,"Rapp","uncertain"),
    (998,14201,177,"Brunner","uncertain"),
    (999,14202,177,"Brunner","uncertain"),
    (1001,14202,190,"Rapp","uncertain"),
    (1003,14302,177,"Brunner","uncertain"),
    (1005,14304,190,"Rapp","uncertain"),
    (1006,14401,177,"Brunner","uncertain"),
    (1007,14402,177,"Brunner","uncertain"),
    (1009,14404,190,"Rapp","uncertain")]
    return question_marks

# flags the list of question marks
def flag_and_comment_question_marks():
    cursor,mydb = db_connection.database_connector()
    cursor3,mydb3 = db_connection.database_connector(the_database="BAD_DATA_SILSO")
    qms = get_question_marks()
    data = db_search.select_all_data()
    fk_rubrics = [q[0] for q in qms]
    rubrics = [q[1] for q in qms]
    qms_left_wanting = [] # these are still to investigate
    count=0
    for q in qms:
        # find the ids of the culprits (innefficiently but hey)
        hitlist_ids=[]
        for i in data:
            comment = i[8]
            flag = i[10]
            fk_rub = i[2]
            # if same rubric and same problem
            if comment == q[4] and flag==1 and fk_rub == q[0]:
                hitlist_ids.append(i[0])
        if len(hitlist_ids)==0:
            print("not found in rubrics",q[1])
            qms_left_wanting.append(q)
        else:
            for i in hitlist_ids:
                query = "UPDATE DATA SET FLAG=2,COMMENT='?' WHERE ID="+str(i)
                cursor.execute(query,())
                cursor3.execute(query,())
                mydb.commit()
                mydb3.commit()
            print("updated data in rubrics",q[1])
        count+=len(hitlist_ids)
    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb3)
                

flag_and_comment_question_marks()
print(count)
input()


# method for generating the list of dates where Adams has 'none observed'
def get_adams_dates():
    dates=[]
    for i in range(25,31):
        dates.append("1820-09-"+str(i))
        dates.append("1820-10-"+str(i))
    dates.append("1820-10-31")
    for i in range(1,12):
        if i<10:
            dates.append("1820-10-0"+str(i))
        else:
            dates.append("1820-10-"+str(i))
    for i in range(1,8):
        dates.append("1820-11-"+str(i))
    for i in range(20,30):
        dates.append("1820-12-"+str(i))
    for i in range(5,25):
        if i<10:
            dates.append("1821-02-0"+str(i))
        else:
            dates.append("1821-02-"+str(i))
    for i in range(1,9):
        dates.append("1820-04-0"+str(i))
    for i in range(5,32):
        if i<10:
            dates.append("1821-05-0"+str(i))
        else:
            dates.append("1821-05-"+str(i))
    for i in range(1,14):
        if i<10:
            dates.append("1821-06-0"+str(i))
        else:
            dates.append("1821-06-"+str(i))
    for i in range(18,31):
        dates.append("1821-06-"+str(i))
    for i in range(1,16):
        if i<10:
            dates.append("1821-07-0"+str(i))
        else:
            dates.append("1821-07-"+str(i))
    for i in range(26,32):
        dates.append("1821-07-"+str(i))
    for i in range(1,7):
        dates.append("1821-08-0"+str(i))
    for i in range(20,32):
        dates.append("1821-08-"+str(i))
    for i in range(1,24):
        if i<10:
            dates.append("1821-09-0"+str(i))
        else:
            dates.append("1821-09-"+str(i))
    for i in range(1,17):
        if i<10:
            dates.append("1821-11-0"+str(i))
        else:
            dates.append("1821-11-"+str(i))
    for i in range(25,32):
        dates.append("1821-12-"+str(i))
    for i in range(1,32):
        if i<10:
            dates.append("1822-01-0"+str(i))
        else:
            dates.append("1822-01-"+str(i))
    for i in range(1,29):
        if i<10:
            dates.append("1822-02-0"+str(i))
        else:
            dates.append("1822-02-"+str(i))
    for i in range(1,4):
        dates.append("1822-03-0"+str(i))
    for i in range(12,21):
        dates.append("1822-04-"+str(i))
    for i in range(2,30):
        if i<10:
            dates.append("1822-05-0"+str(i))
        else:
            dates.append("1822-05-"+str(i))
    for i in range(10,31):
        dates.append("1822-06-"+str(i))
    for i in range(1,22):
        if i<10:
            dates.append("1822-07-0"+str(i))
        else:
            dates.append("1822-07-"+str(i))
    for i in range(4,32):
        if i<10:
            dates.append("1822-08-0"+str(i))
        else:
            dates.append("1822-08-"+str(i))
    for i in range(1,31):
        if i<10:
            dates.append("1822-09-0"+str(i))
            dates.append("1822-10-0"+str(i))
            dates.append("1822-11-0"+str(i))
            dates.append("1822-12-0"+str(i))
            dates.append("1823-01-0"+str(i))
        else:
            dates.append("1882-09-"+str(i))
            dates.append("1822-10-"+str(i))
            dates.append("1822-11-"+str(i))
            dates.append("1822-12-"+str(i))
            dates.append("1823-01-"+str(i))
    dates.append("1822-10-31")
    dates.append("1822-12-31")
    dates.append("1823-01-31")
    for i in range(1,29):
        if i<10:
            dates.append("1823-02-0"+str(i))
        else:
            dates.append("1823-02-"+str(i))
    for i in range(1,13):
        if i<10:
            dates.append("1823-03-0"+str(i))
        else:
            dates.append("1823-03-"+str(i))
    for i in range(16,32):
        dates.append("1823-03-"+str(i))
    for i in range(1,31):
        if i<10:
            dates.append("1823-04-0"+str(i))
            dates.append("1823-05-0"+str(i))
        else:
            dates.append("1823-04-"+str(i))
    
    return dates

# method for INSERTing data to database for the missing 0.0 entries in rubrics 34
def add_adams():
    cursor,mydb = db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    dates = get_adams_dates()
    for d in dates:
        query = "INSERT INTO DATA SET DATE='"+d+"',FK_RUBRICS=34,FK_OBSERVERS=25,"
        query += "GROUPS=0,SUNSPOTS=0,WOLF=0,COMMENT='none visible',DATE_INSERT='2019-07-12',FLAG=0"
        cursor.execute(query,())
        mydb.commit()
    db_connection.close_database_connection(mydb)

"""
Pseudocode for flagging 2 method
for each datapint in the datapoint list
first check to see if the aliases match
if not add these ones to list of to investigate
check to see if the comments match
if so change comment to ? and flag to 2
if not check to see if comment is?, if it is set flag to 2
if not and comment!='?' add it to a list of things to investigate

display the list of things to investigate, maybe pickle it

Pseudocode for moving 2 and 0
for each guy in bad data silso marked with 2 or 0 flag
transfer him # not very hard
"""



