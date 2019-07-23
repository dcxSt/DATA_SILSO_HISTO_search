#read_database_mitteilungen.py

strdate='20190613'

#===============================================================================
#===============================================================================

import MySQLdb
import re
import random
import csv
import datetime as dt
import calendar
import sys,os,numpy, scipy
import math as mt
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import pylab as py
from scipy.stats import sigmaclip
from scipy.stats import kstest
from scipy.stats import anderson
from scipy.stats import mode
from scipy import stats
import pandas as pd
import scipy.optimize as optimization
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
import numpy as np
from urllib import urlopen


dirIn='/Users/Laure/Desktop/SSNWork/corr/'
dirBase='/Users/Laure/sunspots/SSN/SSNCALC/newSN/'
dircreate=dirBase+'results_mitteilungen/'
if not os.path.exists(dircreate):
    os.makedirs(dircreate)
dirOut=dircreate
#fileObscsv=open(dirOut+'Observers12.csv','w')

#===============================================================================

#===============================================================================
#db2=MySQLdb.connect(host='soldb.oma.be',user   ='guestdb',passwd ='StfnPdts',db='DATA_SILSO_HISTO')
#Curseur2=db2.cursor()
##query='SELECT T.STATION, T.DATE, T.Groups_T, T.Suns_T, T.Wolf_T FROM Sunspots_collection_'+scurYear+' T WHERE (YEAR(T.date)="'+scurYear+'" and MONTH(T.date)="'+scurMonth+'" and T.DATE!="0000-00-00" and T.Wolf_T!="" ) ORDER BY T.STATION,T.DATE'
#rubricNumber=710
#query = "SELECT * FROM DATA d WHERE d.FK_RUBRICS=(SELECT r.RUBRICS_ID FROM RUBRICS r WHERE r.RUBRICS_NUMBER = "+str(rubricNumber)+")"
#print query
#Curseur2.execute(query)
#Data=Curseur2.fetchall()
#lenData=len(Data)
#
#print lenData
#dates=[];years=[];months=[];days=[];Ngs=[];Nss=[]; Nws=[]
#comments=[]
#i=0
#while i < lenData-1 :
#	line=Data[i]
#	date=line[1].timetuple()
#	year=date[0];month=date[1];day=date[2]
#	print year, month, day
#	Ng=int(line[4]);Ns=int(line[5]);Nw=int(line[6])
#	comment=line[7]
#	dates.append(date)
#	Ngs.append(Ng)
#	Nss.append(Ns)
#	Nws.append(Nw)
#	comments.append(comment)
#	i+=1
#
#

#db2=MySQLdb.connect(host='soldb.oma.be',user   ='guestdb',passwd ='StfnPdts',db='DATA_SILSO_HISTO')
#Curseur2=db2.cursor()
#observerName = "%Wolf%"
#query = "SELECT * FROM OBSERVERS o  WHERE o.LAST_NAME like %s"
#Curseur2.execute(query,(observerName,))
#Data = Curseur2.fetchall()
#lenData=len(Data)
#
#print lenData
#
#i=0
#while i < lenData:
#	line=Data[i]
#	print line
#	i+=1
##for i in Data:
##    print ((i[0]),(i[1]),(i[2]),(i[3]),(i[4]),(i[5]),(i[6]),(i[7]))
#db2=MySQLdb.connect(host='soldb',user   ='guestdb',passwd ='StfnPdts',db='DATA_SILSO_HISTO')
#Curseur2=db2.cursor()
#observerName = "%Wolf%"
#query = "SELECT * FROM OBSERVERS o  WHERE o.LAST_NAME like %s"
#Curseur2.execute(query,(observerName,))
#Data = Curseur2.fetchall()
#lenData=len(Data)
#
#print lenData
#
#i=0
#while i < lenData:
#	line=Data[i]
#	print line
#	i+=1
##for i in Data:
##    print ((i[0]),(i[1]),(i[2]),(i[3]),(i[4]),(i[5]),(i[6]),(i[7]))



db2=MySQLdb.connect(host='soldb.oma.be',user   ='guestdb',passwd ='StfnPdts',db='DATA_SILSO_HISTO')
Curseur2=db2.cursor()
query = "SELECT * FROM OBSERVERS"
Curseur2.execute(query)
Data = Curseur2.fetchall()
lenData=len(Data)

print lenData
ObsID=[]
i=0
while i < lenData:
	line=Data[i]
	ObsID.append(int(line[0]))
	i+=1
print max(ObsID)
#import pdb; pdb.set_trace()
	
ObserversNames=[]
i=0
while i < max(ObsID)+1:
	ObserversNames.append('')
	i+=1
i=0
while i < lenData:
	line=Data[i]
	number=int(line[0])
	print number, len(ObserversNames)
	ObserversNames[number]=line[1]
	print line
	i+=1
#for i in Data:
#    print ((i[0]),(i[1]),(i[2]),(i[3]),(i[4]),(i[5]),(i[6]),(i[7]))
db2.close()
#import pdb; pdb.set_trace()
print ObserversNames[0:15]

db2=MySQLdb.connect(host='soldb.oma.be',user   ='guestdb',passwd ='StfnPdts',db='DATA_SILSO_HISTO')
Curseur2=db2.cursor()

for j in range(0,len(ObserversNames)):
#for j in range(2,3):
	print '-----------------------------------------------------------------------------------------'
	print 'OBSID',j
	observerName = ObserversNames[j]
	if observerName != '' :
#		observerName = '\'%'+ObserversNames[j][0:3]+'%\''
		observerName = ObserversNames[j][0:6]
		observerName = observerName.replace(" ","")
		observerName = observerName.replace("-","")
		observerName = '%'+observerName+'%'
		
		#observerName = '%WOL%'
		observerID= '%3i' % (j)
		print 'OBSERVER',observerID, '---',observerName
		query = "SELECT * FROM DATA o WHERE o.COMMENT like %s OR o.FK_OBSERVERS = "+observerID+" ORDER BY DATE"
#		query = "SELECT * FROM DATA o WHERE o.COMMENT like %s"
		#query = "SELECT * FROM DATA o WHERE o.COMMENT like %s AND NOT o.FK_OBSERVERS = "+observerID
		Curseur2.execute(query,(observerName,))
		Data = Curseur2.fetchall()
		lenData=len(Data)
		
		
		i=0
		while i < lenData:
			line=Data[i]
			#print 'Special',i, '***',lenData, '**',ObserversNames[int(line[3])], '***',line

			if line[1] is not None: 
				date=line[1].timetuple()
				year=date[0];month=date[1];day=date[2]
				if i==0:
					year0=year; month0=month; day0=day
			else:
				print ObserversNames[j], '-',j,'********************************ERROR timetuple***',line
			i+=1
		print ObserversNames[j], '---',year0, month0, day0, 'TO', year, month, day, 'YEARS', (year-year0)+1
		print '---',observerName , '---',lenData

db2.close()



#db2=MySQLdb.connect(host='soldb.oma.be',user   ='guestdb',passwd ='StfnPdts',db='DATA_SILSO_HISTO')
#Curseur2=db2.cursor()
#observerName = "%Wolf%"
#Obs2Name="%Wolfer%"
#starstring="%*%"
#query = "SELECT * FROM DATA o WHERE o.COMMENT like %s OR o.COMMENT like %s AND NOT o.COMMENT like %s"
#Curseur2.execute(query,(observerName,starstring,Obs2Name,))
#Data = Curseur2.fetchall()
#lenData=len(Data)
#
#print lenData
#
#i=0
#while i < lenData:
#	line=Data[i]
#	print ObserversNames[int(line[3])], '***',line
#	i+=1
#print lenData
#db2.close()
#



import pdb; pdb.set_trace()

