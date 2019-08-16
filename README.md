# Des outiles pour changer la base des donnes du SILSO


## Preamble
The aim of this little project is to do a quality control of the data in *DATA_SILSO_HISTO*. 

I will also get rid of any useless or redundant columns (such as the observers comment column - there are no comments )': ). A third, temporary database will be made to keep a closer eye on the data that still needs to be examined with more scrutiny : *BAD_DATA_SILSO*. This database will act as intermediaire entre *DATA_SILSO_HISTO* et *GOOD_DATA_SILSO*. We will effectively be storing 2 databases-worth of information in 3 databases. The original *DATA_SILSO_HISTO* will have the old data and will be corrected in due course. The intermediary *BAD_DATA_SILSO* will start as a copy of *DATA_SILSO_HISTO* and end up empty as the corrected data is removed from it and placed, in the new format, into *GOOD_DATA_SILSO*

The readme lists first the names of and functions contained in each of my .py files, followed by the .ipynb with the first markdown code-block as a descriptor.


## Python scripts, their methods and descriptors: 

### db_edit.py
***utility methods used to edit the DATA_SILSO_HISTO sql database, for now it's just comments and flags***

**set_comment()**  [44]	 return boolean T if updated, F if there was already a comment
 if there is already a comment, does not replace comment unless specified
 takes cursor, id and comment, and adds the comment to the id number


**add_to_comment()**  [45]	 if there is no comment it sets the comment, if there is it adds to it


**set_flag()**  [9]	 takes id_number cursor and database connection and adds a flag to the data


**set_alternative_flag()**  [11]	 sets a flag with a number from 0 to 9 (inclusive)


**set_alternative_flags_multiple()**  [21]	 same as set_alternative_flag but looks at each database and adds flag if there is a matching id_number


**remove_flag()**  [7]	 takes id_number cursor and database connection and sets flag to 0


**set_wolf()**  [19]	 sets the given wolf number based off of data ID


**set_sunspots()**  [19]	 sets the number of sunspots : SUNSPOTS


**set_groups()**  [19]	 sets the group number : GROUPS


**insert_old_format()**  [34]	 inserts data into the database in the format of DATA_SILSO_HISTO


***

### derived.py
***script with method to deal with (in general terms) the data which is derived, from the umbra and the penumbra***

**move_7_to_good()**  [20]	 method to move all the data-points flagged 7 into GOOD_DATA_SILSO


**move_carrington_out_of_rubbish()**  [21]	 moves them into DATA, in both DATA_SILSO_HISTO and GOOD_DATA_SILSO
 takes all carrington datapoints from rubric 303 that are in RUBBISH_DATA 


**move_carrington_to_good()**  [21]	 get the ids that are in DATA_SILSO_HISTO and belong to rubrics 303, fk=175
 try insert if it doesn't work just give up, it's already there...


***

### searching_the_manuals.py
***searching the manuals is work involving finding each comment,, figuring out what it means, and dealing with the data appropriately***

**move_data_to_bin()**  [101]	 because it deals with more fundamental operations that just duplicates
 this method is from dealing_with_duplicates.py but i copied it here


**transcribe_info_old()**  [28]	 helper method for move_data_to_bin()


**transcribe_info_new()**  [50]	 helper method for move_data_to_bin()


**correct_typos_for_pink()**  [25]	 helper method for pink


**pink()**  [53]	 homogenise them
 the rest of the comments in the rubric are just marked *, so here we 
 pink is the colour for data with comments that have * = something and 


**find_duplicate_observers()**  [1]	

**find_obs_id_by_date()**  [18]	

**find_observer_alias_by_id()**  [9]	

**find_duplicates_data()**  [41]	 makes a dictionary of all the duplicated data by observer alias


**greater_duplicates_data()**  [138]	 the following method is poorly written, slightly better version with it's successor
 makes a dictionary of all the duplicates by observer alias


**duplicates_by_date()**  [125]	 mostly copy pasted from greater_duplicates_data
 duplicates by date dictionary is a better dictionary, returns the dictionary


**write_greater_duplicates_data_text()**  [1]	 and turns it into human readable format
 this method takes as it's argument the list created by the last one


**sorting_duplicates()**  [81]	 sorting the duplicates so that human can get better idea of what's going on


**move_flag3_to_bin()**  [15]	 method moves everything flagged 3 into the bid


***

### test_sound.py
***testing the sound***

***

### db_connection.py
***utility methods used to access the DATA_SILSO_HISTO sql database***

**database_connector()**  [1]	 this function connects you to the database


**get_cursor()**  [15]	 checks if you are connected and have a cursor if not it connects you


**close_database_connection()**  [7]	 closes the database connection


**header()**  [3]	 returns string with header of DATA


***

### create_graphs_helper_readme.py
***/home/steve/anaconda3/bin/python3***

**get_contents()**  [6]	 returns the contents of the specified file, thows exception if no file found


**write_body()**  [22]	 writes the main part of the file - the important stuff


**main()**  [9]	 writes to the file 'GRAPHS_HELPER_README.md'


***

### quality_control_tests.py
***here is where my tests are, these search the database and comment and flag etc.***

**incorrect_wolf_test()**  [40]	 returns list of ids where wolf is incorrectly calculated
 flags and comments the incorrect_wolf_indices (of which there is only one)
 finds where there are incorrectly calculated wolf numbers


**flag_bad_comments()**  [21]	 flags everything with bad comments


**incorrect_rubrics_id()**  [4]	

**big_flag()**  [84]	 flags all comments in BAD_DATA_SILSO that looks even mildly suspicious


**count_flags()**  [10]	

**move_unflagged()**  [27]	 def move unflagged from bad to good


**count_data()**  [6]	 tells you how big the database is, used to verify i transfered everything correctly when moving the data to new format


**unreasonable_sn_flag()**  [38]	

***

### Lockwood-Lefevre-re-analysis-read_RGO_comp_yearly.py
***ead_RGO_comp_yearly.py***

**leapyr()**  [9]	

**date_conv()**  [1]	

**num_days_in_month()**  [1]	

**binbymonth()**  [1]	

**binbyyear()**  [1]	

**remove_edges()**  [1]	

**comp_all()**  [1]	

**comp_res()**  [1]	

***

### db_search.py
***utility methods used search the DATA_SILSO_HISTO sql database***

**select_all_data()**  [12]	 selects all data in columns in DATA are returns it in list format


**select_all_data_general()**  [12]	 selects all data in columns from any table from any database


**select_all_rubrics()**  [11]	 selects all columns in RUBRIC


**select_all_observers()**  [11]	 selects all columns in OBSERVERS


**different_comments()**  [36]	 searches database for comments and saves them all into a text file


**more_efficient_sort_comments_by_rubric()**  [139]	 it also picles some dodgy data
 sorts the comments by rubric and saves it into human-readable files


**missing_rubric()**  [11]	 finds all the data with missing rubrics


**select_online_sn()**  [22]	 returns data from the online database that is saved in my folder 'online_sn'


***

### file_io.py
***file io, does things like reading and writing to textfiles***

**save_list_to_text_file()**  [21]	 save 1D list to text file (works for array too i think)


***

### db_transfers.py
***This script provides the functions needed for the good , and the bad databases to interact***

**db_transfer()**  [1]	 method for transfering and copyting data from old format to new format
 cursor2,mydb2 is the recipient's cursor and mydb
 cursor,mydb is the sender's cursor and mydb


**transfer_multiple()**  [12]	 takes list of id numbers


**move_data_to_bin()**  [101]	 in BAD_DATA_SILSO it removed it entirely from the database (this is slightly worrying...)
 in GOOD_DATA_SILSO it also moves it into the bin
 in DATA_SILSO_HISTO it moves selected data into the RUBBISH_DATA


**move_data_to_bin_only_good()**  [76]	 same as above but only affects GOOD_DATA_SILSO, doesn't touch the rest


**transcribe_info_old()**  [28]	 helper method for move_data_to_bin()


**transcribe_info_new()**  [50]	 helper method for move_data_to_bin()


**move_data_out_of_bin()**  [1]	 in BAD_DATA_SILSO it does nothing
 in GOOD_DATA_SILSO it does the same
 in DATA_SILSO_HISTO it moves data from RUBBISH_DATA to DATA


**move_carrington303_good_to_rubbish()**  [10]	 move carrington's data to rubbish from good data silso


**move_wolf_1864_to_rubbish()**  [24]	 gets rid of WOLF - S - M 's data from 1864 that doesn't belong to him; exec only once


**separate_1865_observers()**  [83]	 seperates out the data from wolf-s-m 1865 table into different observer
 Execute once


**separate_1866_observers()**  [52]	 separates out the data from wolf-s-m 1866 table into different observers
 Execute once


**transfer_flag_2()**  [13]	 transfers all those with flag=2 from BAD_DATA_SILSO to GOOD_DATA_SILSO


**transfer_flag_0()**  [13]	 transfer all those with flag=0 from BAD_DATA_SILSO to GOOD_DATA_SILSO


**transfer_flag_3()**  [13]	 transfers all those with flag=3 from BAD_DATA_SILSO to GOOD_DATA_SILSO


**transfer_flag_8()**  [13]	 that takes input is because I don't wanna execute the wrong flag...
 the reason i'm writing methods for each of these flags rather than just a general one \
 transfers all those with flag=8 from BAD_DATA_SILSO to GOOD_DATA_SILSO


**transfer_flag_9()**  [15]	

***

### dealing_with_duplicates.py
***dealing with the duplicates in every way possible***

**move_data_to_bin()**  [102]	 BAD_DATA_SILSO if so it moves it removes it entirely from the database.
 GOOD_DATA_SILSO, if so it moves it into the bin. Then checks if the data is in 
 the rubbish bin that i made. With the same id it sees if this id can be found in
 redundant duplicates. It takes an id_number only! In DATA_SILSO_HISTO it moves it into 
 this method is the backbone of this script, who's sole purpouse is to scrap the


**transcribe_info_old()**  [28]	 helper method for move_data_to_bin()


**transcribe_info_new()**  [51]	 helper method for move_data_to_bin()


**delete_entered_twice_duplicates()**  [53]	 method takes the greater duplicates dictionary and deletes the first of each pair that has been entered twice


**flag_many_duplicates()**  [84]	 method to flag the duplicate that is missing values (sunspots / wolf == na or none or something)


**change_date_rubric()**  [42]	 while leaving the rest of the date unchanged
 and changes every date from this rubrics_number to the year specified
 method that takes a cursor, a database, a rubrics_number and a year


**change_dates()**  [23]	 calls change_date_rubrics alot


**unflag()**  [15]	 UNFLAGS CERTAIN THINGS WHICH SHOULD BE UNFLAGED


**change_alias_to_brunner_assistent()**  [25]	 ALIAS to 'Brunner Assistent'


**take_out_wolf_1862_duplicates()**  [24]	 takes out some of wolf's duplicates, run once


***

### create_readme.py
***/home/steve/anaconda3/bin/python3***

**get_py_filenames()**  [3]	 method for returning all the .py filenames in the directory


**get_ipynb_filenames()**  [3]	 method for returning all the .ipynb filenames in the directory


**get_method_description_dictionary()**  [27]	 key = filename ; value = [[method_name,description],...]
 returns big dictionary of methods and descriptors in each file


**get_size_methods_dictionary()**  [35]	 returns a dictionary key = filename ; value = dictionary with key = methodname, value = num lines


**get_ipynb_descriptors_dic()**  [32]	 get the ipynb number of blocks and descriptors dictionary


**get_subheaders_dictionary()**  [21]	 returns dictionary key = script ; value = subheadding of script


**write_title()**  [5]	 write the title


**write_preamble()**  [9]	 write the preamble


**write_body()**  [16]	 write the main body of the readme file


**write_ipynb()**  [12]	 write the jupiter-notebooks section


**write_links()**  [9]	 write the links section


**write_readme()**  [9]	 writes the readme file


***

### db_graphs_compare.py
***this script is a bit like graphs helper, it contains methods to plot, things for use in a jupyter notebook. Specifically, plots and charts that bring into evidence the types of changes I , implemented; comparing the original with the new.***

**fetch_all_data()**  [13]	 helper method for many functions to get data, observers and rubrics from each database


**find_overlap()**  [32]	 helper method, identifies id numbers that the databases have in common etc.


**pie_charts_1()**  [82]	 method to plot a pie chart that shows how much data was deleted / input


**pie_charts_2()**  [87]	 method to plot pie chart and bar chart to show how the data was modified


**pie_charts_3()**  [40]	 method to plot pie chart and bar chart with the different flags


***

### secchi_derived_fix.py
***rectification des donnes mal rentre de Herr Professor Secchi***

**find_comments_derived()**  [10]	 find all comments from secchi with the comment derived in it


**secchi_derived_fix()**  [22]	

***

### db_homogenise_comments.py
***homogenise comments, when executed homogenises all comments to their 'group'***

**homogenise_uncertain()**  [24]	 checked


**homogenise_null()**  [11]	

**homogenise_typos()**  [30]	

**correct_asterix_comments()**  [36]	 need correcting and correct them
 for this one i make a list of '*' comments and their rubrics which 


***

### graphs_helper.py
***methods to help me display some information graphically***

**data_by_obs_alias_good()**  [11]	 key = obs_alias , value = data
 searchable by observer alias ; 
 method that organises the data from good_database into dictionary 


**data_by_obs_alias_histo()**  [15]	 really slow - avoid using
 same as above but for different database format


**get_data_by_obs_seperate_flags()**  [33]	 returns data by observer where each observer has a list of 10 sublists (1/flag)


**display_seperate_flags()**  [54]	 shows figure of some observer's observations seperated by flag only for GOOD_DATA_SILSO


**display_seperate_flags_all()**  [78]	 shows figure with 3 subfigures: groups, sunspots, wolf


**display_all_databases()**  [67]	 plots nothing if there 
 takes observer alias and g/s/r and plots different databases in different colors


**display_compare_observers()**  [1]	 exclude_these_rubrics is a list of rubrics number you don't want to plot, leave list empty if none
 online_sn (boolean) if True plots a smoothed plot of the current sunspot number V2.0 with smoothing factor smoothness\n
 figsize size of the figure also 2d-tuple\n
 interval = 2d-tuple (date1,date2) with date1<date2\n
 This function has alot of functionality, it's work listing it out.\n
 takes observerS aliases and database and plots each observer on the same plot.


**get_smoothed_sn()**  [17]	 the higher the smoothness, the smoother the plot
 takes date interval and returns x,y arrays of smoothed data to plot from the online sunspots number


**display_wolf_drift()**  [1]	 \nThe slope displayed is indicative of drift
 \n- cutoff is a factor that determines where you start cutting off outlier data
 \n- squish_wolf is to squish the scaling factor of wolf number plotted
 \n- interval takes string tuple of len 2
 Plots the drift of an observer, uses wolf number V.2.0 as baseline


**dates_to_decimal()**  [24]	 converts an array of dates into an array of floats that represent dates


**decimal_to_dates()**  [20]	 converts an array of decimal_dates to array of dates


**line()**  [3]	 it's a helper function for those that are using scipy.optimize.curve_fit for a line of best fit
 line of best fit 2 unknowns function


**size_data_by_observer_hist()**  [90]	 method to identify observers in DATA_SILSO_HISTO.OBSERVERS and how much data is associated with each one


**event_plot()**  [1]	 Takes interval and list of observer aliases and does an event plot to show you when they recorded what data


**days_in()**  [6]	 generates dates of all days in specified interval (inclusive)
 helper method for stacked_area_plot


**stacked_area_plot()**  [1]	 Takes interval, and does a stacked area plot witht he observers in that interval


**frequency_wolf_histogram()**  [1]	 sup_freq is a positive integer
 data interval is tuple with 2 integers
 zero is boolean choses wether to include zero into the plot
 takes observer - plots histogram frequency vs wolf


**comparing_two_observers()**  [129]	 below (5+6) plot the calibration factor that determines the relative k coefficient
 plot also a smoothed date / frequency plot with both observers (4)
 plot two histograms comparing the observers' sunspots, group and wolf (1,2,3) for their over-lapping interval


**get2observers_data()**  [11]	 small helper method for the histograms method...


**get_hist_data()**  [61]	 helper method for frequency_wolf_histogram, gets the histogram data


**get_full_carrington_dictionaries()**  [25]	 to help out with the Carrington investigation
 CARRINGTON


**blacklist_dates()**  [19]	 but now I allowed carrington303 to have data from before 1859 so it's to filter those too
 originally this was to figure out if there are discrepancies in date
 helper for get_carrington_dictionaries_59to60
 CARRINGTON


**get_carringdon_dictionaries_59to60()**  [13]	 makes searchable dictionary for carrington
 CARRINGTON


**round_to_int()**  [6]	 rounds each element in list to nearset int
 CARRINGTON


**get_sunspots()**  [15]	 returns sunspots numbers, for derived carrington
 CARRINGTON


***

### red_uncertain.py
***script that deals with the data marked 'red questionmark'***

**get_question_marks()**  [83]	 (rubrics_id,rubrics_number,obs_id,obs_alias,comment)
 defines a list of question marks:


**flag_and_comment_question_marks()**  [35]	 flags the list of question marks


**get_adams_dates()**  [125]	 method for generating the list of dates where Adams has 'none observed'


**add_adams()**  [10]	 method for INSERTing data to database for the missing 0.0 entries in rubrics 34


***



## Jupyter notebooks:

**Wolf Wolfer Eventplots.ipynb**  [code blocks = 13]  The Frequency and number of observations plots is getting over-crowded so I am opening this notebook enitrely for doing event-plot for the Wolf / Wolfer investigation

**Histograms.ipynb**  [code blocks = 19]  Testing the histogram plotting function

**Schwabe Drawings data.ipynb**  [code blocks = 9]  

**Stacked Area Charts.ipynb**  [code blocks = 20]  Some stacked area charts of the data, it's purpose is similar to the event-plot but allows us to see more clearely how the tables are constructed from 1860 to 1870. The stacked area charts also allows us to see where there are not many observations being made. Unfortunately the method is not optimally designed, it does the job but you may have to wait a while for it to load... For instance it takes about 1 minuet to load a 40 year time interval which is NOT GOOD :(, you shoulda taken comp 257 lol, if you wanna make inneficient algorithems at least do it in c or java or smt... The fluctuations you see in the drawings are seasonal.

**suspicious sunspots plots.ipynb**  [code blocks = 23]  This notebook displays sunspot numbers which are unusually big. Here is also where the graphs that show the edits I made to Tacchini's data is stored.

**random_plots_and_graphs.ipynb**  [code blocks = 14]  Here there are the plots where I discovered Carrington and Kew's anomalous data which turned out to be the area measurements

**derived_plots.ipynb**  [code blocks = 8]  Shitty notebook that isn't very useful, I think I made this one before the other two, it has some Secchi plots as well as Carrington plots

**Schwabe early notebook.ipynb**  [code blocks = 7]  Testing the home-made method: display_seperate_flags_all. There isn't very much content in this notebook.

**Frequency and number of observation plots.ipynb**  [code blocks = 20]  The following plots are to do with when and where who is recording what we have bar-charts that display the number of data-points associated with each observer and an event-plot that show for each observer, when they recorded the data they did

**MittDBPython.ipynb**  [code blocks = 18]  One of the first Jupiter notebooks created, it's pretty useless now

**carrington_investigation_wolf.ipynb**  [code blocks = 15]  Notebook devoted to carrington's converstion from total area of surface of sunspot number into the derived sunspots numbers

**wolf_wolfer_investigation.ipynb**  [code blocks = 21]  This is the first notebook in which I test my display_wolf_drift() method in the hope of perhaps picking up on the drift of wolf.\nAs the title suggests there are also many plots of Wolf's and Wolfer's data as well as some people during their period of data collection.

**secchi_derivation.ipynb**  [code blocks = 22]  A bunch of methods were executed here to keep track of the derivation of Secchi's data when it was on-going. Because there are only to be executed once as they edit the databases, most of the content has been commented out with \\nThere are also some of Secchi's plots added after the derivation.

**carrington_investigation_groups.ipynb**  [code blocks = 7]  This notebook is dedicated to Carrington's data, specifically for the derivation / estimation of the sunspots number based off of his area measurements.

**executing_commands.ipynb**  [code blocks = 22]  This is one of the first notebooks I made, it's purpose is to execute commands that I wrote in the .py files, but it's pretty useless now. It was a good peduncle that lead to the creation of a better system (to borrow Alan Watts' analogy).

**kew_derivation.ipynb**  [code blocks = 15]  In this notebook there is the derivation of Kew's sunspots numbers from his area measurements. Since it's already been done I pickled the before and after and you can see the graphs without actually changing the data in the sql databases.

## Links and Resources

* [the github project where i try to keep things organised (ish)](https://github.com/users/dcxSt/projects/2?fullscreen=true)

* *Basics of sql* (open in private browsing or annoying messages) includes how to-s on: [https://openclassrooms.com/fr/courses/1959476-administrez-vos-bases-de-donnees-avec-mysql](https://openclassrooms.com/fr/courses/1959476-administrez-vos-bases-de-donnees-avec-mysql)

* [saving a database](https://openclassrooms.com/fr/courses/1959476-administrez-vos-bases-de-donnees-avec-mysql/1961762-supprimez-et-modifiez-des-donnees)

* [import an sql into a database](https://stackoverflow.com/questions/17666249/how-to-import-an-sql-file-using-the-command-line-in-mysql#17666279)

