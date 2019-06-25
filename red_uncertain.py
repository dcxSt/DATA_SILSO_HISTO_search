### red uncertain

import db_connection

def question_mark():
    # (rubrics_id,rubrics_number,obs_id,obs_alias,'uncertain')
    question_marks=[(171,294,45,'Tacchini','uncertain'),
    (316,484,45,'Tacchini','uncertain'),
    (318,481,55,'Denza','uncertain'),
    (326,676,101,'Catina 1 - Ricco - Mascari'),
    ()]

def non_visible():
    # (rubrics_id,rubrics_number,obs_id,obs_alias,'uncertain')
    none_visibles=[(34,167,25,'Adams','uncertain'),]

def duplicates():
    """there are some data points which are duplicated, this arises
    when we have the same observer appearing twice under the same alias
    but different observer ids...
    """
    # (rubrics_id,rubrics_number,obs_id1,obs_id2)
    """delete all of the observer id2 that is duplicated
    for each of the points you will delete, first check that it truely
    is a duplicate..."""

    """infact i'm gonna make a script to identify all duplicates because
    I have no idea how many there could be as well as any that might not 
    be....ugh! I'm gonna put it in searching_the_manuals"""

def find_duplicate_observers():
    # find all observers which have more than 1 observer id
