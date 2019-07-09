# Des outiles pour changer la base des donnes du SILSO


## Preamble
The aim of this little project is to do a quality control of the data in *DATA_SILSO_HISTO*. Once the data is fixed and cleaned up, it will be stored on a new database - temporarily named *GOOD_DATA_SILSO* in a more user-friendly format to what currently exists. I will also get rid of any useless or redundant columns (such as the observers comment column - there are no comments )': ). A third, temporary database will be mad to keep a closer eye on the data that still needs to be examined with more scrutiny : *BAD_DATA_SILSO*. This database will act as intermediaire entre *DATA_SILSO_HISTO* et *GOOD_DATA_SILSO*. We will effectively be storing 2 databases-worth of information in 3 databases. The original *DATA_SILSO_HISTO* will have the old data and will be corrected in due course. The intermediary *BAD_DATA_SILSO* will start as a copy of *DATA_SILSO_HISTO* and end up empty as the corrected data is removed from it and placed, in the new format, into *GOOD_DATA_SILSO*

## Python scripts, their methods and descriptors

### db_edit.py

##### set_comment()
 return boolean T if updated, F if there was already a comment
 if there is already a comment, does not replace comment unless specified
 takes cursor, id and comment, and adds the comment to the id number


##### add_to_comment()
 if there is no comment it sets the comment, if there is it adds to it


##### set_flag()
 takes id_number cursor and database connection and adds a flag to the data


##### set_alternative_flag()
 sets a flag with a number from 0 to 9 (inclusive)


##### set_alternative_flags_multiple()
 same as set_alternative_flag but looks at each database and adds flag if there is a matching id_number


##### remove_flag()
 takes id_number cursor and database connection and sets flag to 0


##### set_wolf()
 sets the given wolf number based off of data ID


##### set_sunspots()
 sets the number of sunspots : SUNSPOTS


##### set_groups()
 sets the group number : GROUPS


##### insert_old_format()
 inserts data into the database in the format of DATA_SILSO_HISTO


### derived.py

##### move_7_to_good()
 method to move all the data-points flagged 7 into GOOD_DATA_SILSO


##### move_carrington_out_of_rubbish()
 moves them into DATA, in both DATA_SILSO_HISTO and GOOD_DATA_SILSO
 takes all carrington datapoints from rubric 303 that are in RUBBISH_DATA 


##### move_carrington_to_good()


### searching_the_manuals.py

##### move_data_to_bin()
 because it deals with more fundamental operations that just duplicates
 this method is from dealing_with_duplicates.py but i copied it here


##### transcribe_info_old()
 helper method for move_data_to_bin()


##### transcribe_info_new()
 helper method for move_data_to_bin()


##### correct_typos_for_pink()
 helper method for pink


##### pink()
 homogenise them
 the rest of the comments in the rubric are just marked *, so here we 
 pink is the colour for data with comments that have * = something and 


##### find_duplicate_observers()


##### find_obs_id_by_date()


##### find_observer_alias_by_id()


##### find_duplicates_data()
 makes a dictionary of all the duplicated data by observer alias


##### greater_duplicates_data()
 the following method is poorly written, slightly better version with it's successor
 makes a dictionary of all the duplicates by observer alias


##### duplicates_by_date()
 mostly copy pasted from greater_duplicates_data
 duplicates by date dictionary is a better dictionary, returns the dictionary


##### write_greater_duplicates_data_text()
 and turns it into human readable format
 this method takes as it's argument the list created by the last one


##### sorting_duplicates()
 sorting the duplicates so that human can get better idea of what's going on


##### move_flag3_to_bin()
 method moves everything flagged 3 into the bid


### test_sound.py

### db_connection.py

##### database_connector()
 this function connects you to the database


##### get_cursor()
 checks if you are connected and have a cursor if not it connects you


##### close_database_connection()
 closes the database connection


##### header()
 returns string with header of DATA


### quality_control_tests.py

##### incorrect_wolf_test()
 returns list of ids where wolf is incorrectly calculated
 flags and comments the incorrect_wolf_indices (of which there is only one)
 finds where there are incorrectly calculated wolf numbers


##### flag_bad_comments()
 flags everything with bad comments


##### incorrect_rubrics_id()


##### big_flag()
 flags all comments in BAD_DATA_SILSO that looks even mildly suspicious


##### count_flags()


##### move_unflagged()
 def move unflagged from bad to good


##### count_data()
 tells you how big the database is, used to verify i transfered everything correctly when moving the data to new format


##### unreasonable_sn_flag()


### db_search.py

##### select_all_data()
 selects all data in columns in DATA are returns it in list format


##### select_all_data_general()
 selects all data in columns from any table from any database


##### select_all_rubrics()
 selects all columns in RUBRIC


##### select_all_observers()
 selects all columns in OBSERVERS


##### different_comments()
 searches database for comments and saves them all into a text file


##### more_efficient_sort_comments_by_rubric()
 it also picles some dodgy data
 sorts the comments by rubric and saves it into human-readable files


##### missing_rubric()
 finds all the data with missing rubrics


### file_io.py

##### save_list_to_text_file()
 save 1D list to text file (works for array too i think)


### db_transfers.py

##### db_transfer()
 method for transfering and copyting data from old format to new format
 cursor2,mydb2 is the recipient's cursor and mydb
 cursor,mydb is the sender's cursor and mydb


##### transfer_multiple()
 takes list of id numbers


##### move_data_to_bin()
 in BAD_DATA_SILSO it removed it entirely from the database (this is slightly worrying...)
 in GOOD_DATA_SILSO it also moves it into the bin
 in DATA_SILSO_HISTO it moves selected data into the RUBBISH_DATA


##### move_data_to_bin_only_good()
 same as above but only affects GOOD_DATA_SILSO, doesn't touch the rest


##### transcribe_info_old()
 helper method for move_data_to_bin()


##### transcribe_info_new()
 helper method for move_data_to_bin()


##### move_data_out_of_bin()
 in BAD_DATA_SILSO it does nothing
 in GOOD_DATA_SILSO it does the same
 in DATA_SILSO_HISTO it moves data from RUBBISH_DATA to DATA


##### move_carrington303_good_to_rubbish()
 move carrington's data to rubbish from good data silso


### dealing_with_duplicates.py

##### move_data_to_bin()
 BAD_DATA_SILSO if so it moves it removes it entirely from the database.
 GOOD_DATA_SILSO, if so it moves it into the bin. Then checks if the data is in 
 the rubbish bin that i made. With the same id it sees if this id can be found in
 redundant duplicates. It takes an id_number only! In DATA_SILSO_HISTO it moves it into 
 this method is the backbone of this script, who's sole purpouse is to scrap the


##### transcribe_info_old()
 helper method for move_data_to_bin()


##### transcribe_info_new()
 helper method for move_data_to_bin()


##### delete_entered_twice_duplicates()
 method takes the greater duplicates dictionary and deletes the first of each pair that has been entered twice


##### flag_many_duplicates()
 method to flag the duplicate that is missing values (sunspots / wolf == na or none or something)


##### change_date_rubric()
 while leaving the rest of the date unchanged
 and changes every date from this rubrics_number to the year specified
 method that takes a cursor, a database, a rubrics_number and a year


##### change_dates()
 calls change_date_rubrics alot


##### unflag()
 UNFLAGS CERTAIN THINGS WHICH SHOULD BE UNFLAGED


##### change_alias_to_brunner_assistent()
 ALIAS to 'Brunner Assistent'


### create_readme.py

##### get_py_filenames()
 method for returning all the .py filenames in the directory


##### get_ipynb_filenames()
 method for returning all the .ipynb filenames in the directory


##### get_method_description_dictionary()
 key = filename ; value = [[method_name,description],...]
 returns big dictionary of methods and descriptors in each file


##### write_title()
 write the title


##### write_preamble()
 write the preamble


##### write_body()
 write the body


##### write_links()
 write the links section


##### write_readme()
 writes the readme file


### secchi_derived_fix.py

##### find_comments_derived()
 find all comments from secchi with the comment derived in it


##### secchi_derived_fix()


### db_homogenise_comments.py

##### homogenise_uncertain()
 checked


##### homogenise_null()


##### homogenise_typos()


##### correct_asterix_comments()
 need correcting and correct them
 for this one i make a list of '*' comments and their rubrics which 


### graphs_helper.py

##### data_by_obs_alias_good()
 method that organises the data from good_database into dictionary searchable by observer alias


##### data_by_obs_alias_histo()


##### get_data_by_obs_seperate_flags()
 returns data by observer where each observer has a list of 10 sublists (1/flag)


##### display_seperate_flags()
 shows figure of some observer's observations seperated by flag


##### display_seperate_flags_all()


##### get_full_carrington_dictionaries()
 to help out with the Carrington investigation


##### blacklist_dates()
 but now I allowed carrington303 to have data from before 1859 so it's to filter those too
 originally this was to figure out if there are discrepancies in date
 helper for get_carrington_dictionaries_59to60


##### get_carringdon_dictionaries_59to60()
 makes searchable dictionary for carrington


##### round_to_int()
 rounds each element in list to nearset int


##### get_sunspots()
 returns sunspots numbers, for derived carrington


### red_uncertain.py

##### question_mark()


##### non_visible()


##### duplicates()


##### find_duplicate_observers()


## Links and Resources

* [the github project where i try to keep things organised (ish)](https://github.com/users/dcxSt/projects/2?fullscreen=true)

* *Basics of sql* (open in private browsing or annoying messages) includes how to-s on: [https://openclassrooms.com/fr/courses/1959476-administrez-vos-bases-de-donnees-avec-mysql](https://openclassrooms.com/fr/courses/1959476-administrez-vos-bases-de-donnees-avec-mysql)

* [saving a database](https://openclassrooms.com/fr/courses/1959476-administrez-vos-bases-de-donnees-avec-mysql/1961762-supprimez-et-modifiez-des-donnees)

* [import an sql into a database](https://stackoverflow.com/questions/17666249/how-to-import-an-sql-file-using-the-command-line-in-mysql#17666279)

