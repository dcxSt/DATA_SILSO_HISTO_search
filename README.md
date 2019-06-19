# Des outiles pour changer la base des donnes du SILSO

The aim of this little project is to do a quality control of the data in *DATA_SILSO_HISTO*. Once the data is fixed and cleaned up, it will be stored on a new database - temporarily named *GOOD_DATA_SILSO* in a more user-friendly format to what currently exists. I will also get rid of any useless or redundant columns (such as the observers comment column - there are no comments )': ). A third, temporary database will be mad to keep a closer eye on the data that still needs to be examined with more scrutiny : *BAD_DATA_SILSO*. This database will act as intermediaire entre *DATA_SILSO_HISTO* et *GOOD_DATA_SILSO*. We will effectively be storing 2 databases-worth of information in 3 databases. The original *DATA_SILSO_HISTO* will have the old data and will be corrected in due course. The intermediary *BAD_DATA_SILSO* will start as a copy of *DATA_SILSO_HISTO* and end up empty as the corrected data is removed from it and placed, in the new format, into *GOOD_DATA_SILSO*

**Dans les scripts suivantes il y a des methodes pour search and change la database.**

### db_connection.py
provides methods to connect python to the mysql database using the mysql library

### db_search.py
provides methods to search the DATA_SILSO_HISTO database

### db_edit.py
provide methods to make some basic changes and edits to the database

### file_io.py
basic method for writing to a file


### quality_control_tests.py
some tests to be done on the original database

### db_transfers.py
methods for transfering data from old database to new one:
when some passes the quality control tests, it is unflagged and moved onto the new database and out of the old one

### secchi_derived_fix.py
when executed, this script finds all the data that is marked with a comment 'derived x' (where x /in /mathbb{Z}) and changes the data accordingly. What happened here is unfortunately the astronomer Secchi, instead of recording the number of sunspots he was calculating the total surface area covered by the penumbras of the sunspots, Rudolf Wolf found a way of using his data but where is is writtin in the 'astronomische Mittheilungen' the relative area of sunspot coverage, the people digitalising the data mistakenly used this number as the sunspot number. Luckily they commented the data which had this fishy 'derived x' written next to it...

### db_homogenise_comments.py
there are many comments in this database which either mean exactly the same thing or are typos, this homogenises some of them. (turns 'uncertain','incertain','Uncertain' into 'uncertain')


## useful resources
*Basics of sql* (open in private browsing or annoying messages) includes how to-s on: [https://openclassrooms.com/fr/courses/1959476-administrez-vos-bases-de-donnees-avec-mysql](https://openclassrooms.com/fr/courses/1959476-administrez-vos-bases-de-donnees-avec-mysql)
* [saving a database](https://openclassrooms.com/fr/courses/1959476-administrez-vos-bases-de-donnees-avec-mysql/1961762-supprimez-et-modifiez-des-donnees)

*other sql help*
* [import an sql into a database](https://stackoverflow.com/questions/17666249/how-to-import-an-sql-file-using-the-command-line-in-mysql#17666279)
