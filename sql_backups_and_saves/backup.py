#!/home/steve/anaconda3/bin/python3

# backs up myslq databases in the format that I like

import os
import datetime as dt

[date,time] = str(dt.datetime.now()).split(" ")
date_time = date+"_"+time

os.system("mkdir "+date_time)

# back up the databases
os.system("mysqldump -u root --single-transaction --opt DATA_SILSO_HISTO > ./"+date_time+"/DATA_SILSO_HISTO.sql")
os.system("mysqldump -u root --single-transaction --opt GOOD_DATA_SILSO > ./"+date_time+"/GOOD_DATA_SILSO.sql")
os.system("mysqldump -u root --single-transaction --opt BAD_DATA_SILSO > ./"+date_time+"/BAD_DATA_SILSO.sql")

print("backed up databases as date_time :",date_time)

# commit
print("git status:")
os.system("git status")
print("git add")
os.system("git add *")
print("git status")
os.system("git status")
print("git commit")
os.system("git commit -m 'backed up databases at "+date_time+"'")

print("commited :)")
