# searching the manuals is work involving finding each comment,
# figuring out what it means, and dealing with the data appropriately

# import
import db_connection
import db_edit
import db_search

def correct_typos_for_pink():
    # this method also partakes in the homogenisation of comments
    # makes dictionary with keys as incorrect and values as correct
    # also i'm taking out all accents because they are not very
    # international
    typos={}
    typos["* = très mauvaise définition"]="* = tres mauvaise definition"
    typos["* = se réfère aux observations de Mlle Olga Subbotin"]="* = Olga Subbotin"

    # correct these in both databases
    cursor,mydb=db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    cursor2,mydb2=db_connection.database_connector(the_database="BAD_DATA_SILSO")
    for i in typos:
        query="UPDATE DATA SET COMMENT='"+typos[i]+"' WHERE COMMENT='"+i+"';"
        cursor.execute(query,())
        cursor2.execute(query,())
        mydb.commit()
        mydb2.commit()
        print(i+" --> "+typos[i]+" DONE")
    print("The typos were set right")

    # disconnect
    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb2)



def pink():
    """
    In this method I create a big list of things where we have 
    comments from the same rubric with shorthand comments and making 
    it so that all the comments that mean ttodayhe same things become the 
    same this does not deal with spelling errors"""
    
    # it's important to run typos first
    correct_typos_for_pink()

    # (rubric_number , comment , short-hand)
    suspects=[(752,"r=Ricco","r"),(757,"* = Wolfer P","*"),
    (758,"* = Broger-P","*"),(761,"* = Quimby P","*"),
    (767,"* = Jastremsky","*"),(768,"* = second instrument","*"),
    (777,"* = Wolfer P","*"),(778,"* = Broger P","*"),
    (783,"* = second instrument","*"),(866,"* = P","*"),
    (868,"* = telescope 2","*"),(868,"** = telescope 3","**"),
    (869,"* = P","*"),(871,"* = telescope 2","*"),
    (871,"** = telescope 3","**"),(874,"* = tres mauvaise definition","*"),
    (879,"* = N. Sykora","*"),(883,"m = Mazarella","m"),
    (889,"* = P","*"),(890,"* = P","*"),
    (892,"* = telescope 2","*"),(893,"* = P","*"),
    (895,"A = W. Abold","A"),(895,"S = Sykora","S"),
    (900,"* = direct observation","*"),(1046,"* = disk 10 cm","*"),
    (1033,"* = Olga Subbotin","*"),(13901,"Waldmeier","W"),
    (14001,"Waldmeier","W"),(14401,"Waldmeier","W")]

    # update the comments in both databases
    cursor,mydb=db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    cursor2,mydb2=db_connection.database_connector(the_database="BAD_DATA_SILSO")
    for i in suspects:
        # want to replace short comments with long comments
        rubrics_number = i[0]
        long_comment = i[1]
        short_comment = i[2]
        # find fk_rubrics
        query = "SELECT RUBRICS_ID FROM RUBRICS WHERE RUBRICS_NUMBER = "+str(rubrics_number)
        cursor.execute(query,())
        rubrics_id = cursor.fetchall()[0][0]
        # replace the comment
        query = "UPDATE DATA SET COMMENT='"+long_comment+"' WHERE FK_RUBRICS="+str(rubrics_id)+" AND COMMENT='"+short_comment+"'"
        cursor.execute(query,())
        cursor2.execute(query,())
        mydb.commit()
        mydb2.commit()
        print("\nupdated comment '",short_comment,"' to '",long_comment,
            "' for rubric number",rubrics_number," and rubrics id",rubrics_id)

    # disconnect
    db_connection.close_database_connection(mydb)
    db_connection.close_database_connection(mydb2)



def more_synonyms():
    # this is a dictionary with keys as incorrect and values as correct
    synonyms={}

pink()

#def rubric_specific_corrections():
    # has a list that resembles pink but operates differently:
    # (rubric_number, correction, incorrect original comment)
