#read_RGO_comp_yearly.py


strdate='20150929'
firstyear=1933.
lastyear=1946.
nyears=lastyear-firstyear
lastRGO=1960.


#lastRGO=1946.+nyears#1976.
##if last RGO > 1976 = 1976
#if lastRGO > 1976. : lastRGO =1976.

#optimize the exponent or use Lockwood 0.871 and 1 (Ra, Ng) values of m.
optmexp=1.

instance='_newNG_yearly_last_'+str(lastRGO).strip()+'_'+strdate

#===============================================================================
# 
# 
#===============================================================================
import re
import random
import csv
import datetime as dt
import sys,os,numpy
import math as mt
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import pylab as py
import fits
from scipy import stats
from scipy.integrate import quad
from scipy.stats.stats import pearsonr
import scipy.stats as st

dirIn='/Users/Laure/sunspots/catalogs/'
dirOut='/Users/Laure/Desktop/Lockwood/yearly/1920/'

#===============================================================================
def leapyr(n):
    if n % 400 == 0:
        return True
    if n % 100 == 0:
        return False
    if n % 4 == 0:
        return 1.
    else:
        return 0.
#print leapyr(1900)
#===============================================================================
#===============================================================================
def date_conv(year, month, day, hour, minutes, seconds):
	NUM_DAYS_IN_YR = 365. + leapyr(year)
	if leapyr(year) > 0.:
		days = [31,29,31,30,31,30,31,31,30,31,30,31]
	else:
		days = [31,28,31,30,31,30,31,31,30,31,30,31]
	nbdays=0.
	if month > 1:
		for i in range(1,int(month)):
			nbdays+=days[i-1]
			#print nbdays
		nbdays+=day-1.
		fracyear=year+nbdays/NUM_DAYS_IN_YR+hour/(NUM_DAYS_IN_YR*24)+minutes/(NUM_DAYS_IN_YR*24*60.)+seconds/(NUM_DAYS_IN_YR*24*60.*60.)
	else: #january
		nbdays=day-1.
		fracyear=year+nbdays/NUM_DAYS_IN_YR+hour/(NUM_DAYS_IN_YR*24)+minutes/(NUM_DAYS_IN_YR*24*60.)+seconds/(NUM_DAYS_IN_YR*24*60.*60.)
#	import pdb; pdb.set_trace()

	return fracyear
#===============================================================================

#===============================================================================
def num_days_in_month(year, month):
	NUM_DAYS_IN_YR = 365. + leapyr(year)
	if leapyr(year) > 0.:
		days = [31,29,31,30,31,30,31,31,30,31,30,31]
	else:
		days = [31,28,31,30,31,30,31,31,30,31,30,31]
	ndays=days[int(month-1)]
	return ndays
#===============================================================================


#===============================================================================
#====================================BIN BY MONTH===============================
#===============================================================================
def binbymonth(time,data,year,month):
	time=np.asarray(time)
	data=np.asarray(data)
	bintime=[] ; bindata=[] ; binstddata=[] 
	nbli=0 ; nblines=len(data)
	currentmonth=0. ; nvalue=0
	for i in range(0,len(time)):
		yearval=year[i]
		monthval=month[i]
		if yearval >= 1800.:
			if monthval != currentmonth and currentmonth > 0:
				valtime=[] ; valdata=[] 
				count=0. ; count0=0. ; counts=0.
				for jj in range(nvalue, nvalue+len(time[nvalue:nbli])):
					#print 'TIME', float(time[jj])
					valtime.append(float(time[jj]))
					valdata.append(float(data[jj]))
					count0+=1.
				dayd=num_days_in_month(currentyear,currentmonth)/2.
				binvaltime=date_conv(currentyear,currentmonth,dayd,0.,0.,0.)
				#binvaltime=numpy.mean(valtime)
				binvaldata=numpy.mean(valdata)
				stdev=(numpy.std(valdata))#/mt.sqrt(count0)
				bintime.append(binvaltime)
				bindata.append(binvaldata)
				binstddata.append(stdev)
				#print 'binbymonth', currentyear,';',currentmonth,';', binvaltime, ';',binvaldata,';', stdev , "\r"
				nvalue=nbli
				
			if i == nblines-1 :
				#print 'IN END'
				valtime=[] ; valdata=[] 
				count=0. ; count0=0. ; counts=0.
				for jj in range(nvalue, nvalue+len(time[nvalue:nbli])):
					#print 'TIME', float(time[jj])
					valtime.append(float(time[jj]))
					valdata.append(float(data[jj]))
					count0+=1.
				dayd=num_days_in_month(currentyear,currentmonth)/2.
				binvaltime=date_conv(currentyear,currentmonth,dayd,0.,0.,0.)
				#binvaltime=numpy.mean(valtime)
				binvaldata=numpy.mean(valdata)
				stdev=(numpy.std(valdata))#/mt.sqrt(count0)
				bintime.append(binvaltime)
				bindata.append(binvaldata)
				binstddata.append(stdev)
				#print 'binbymonth END', currentyear,';',currentmonth,';', binvaltime, ';',binvaldata,';', stdev
			nbli+=1
			currentmonth=monthval
			currentyear=yearval
	#import pdb; pdb.set_trace()

	return bintime, bindata, binstddata
#===============================================================================




#===============================================================================
#====================================BIN BY YEAR===============================
#===============================================================================
#problem of edges with the function to take a look at !!!
def binbyyear(time,data,year):
	time=np.asarray(time)
	data=np.asarray(data)
	bintime=[] ; bindata=[] ; binstddata=[] 
	nbli=0 ; nblines=len(data)
	currentyear=0. ; nvalue=0
	for i in range(0,len(time)):
		yearval=year[i]
		#print 'YEARVAL ', yearval, currentyear
		#if mt.modf(yearval)[1] > 1875.:
		#	import pdb; pdb.set_trace()

		if yearval >= 1800.:
			#print yearval, currentyear
			if yearval != currentyear and currentyear > 0:
				valtime=[] ; valdata=[] 
				count=0. ; count0=0. ; counts=0.
				for jj in range(nvalue, nvalue+len(time[nvalue:nbli])):
					valtime.append(float(time[jj]))
					valdata.append(float(data[jj]))
					#if currentyear == 1874.:
					#	print 'VALUES BINYEAR ', time[jj], data[jj]
					count0+=1.
				if count0 >=50.:
					binvaltime=float(mt.modf(currentyear)[1])+0.5
				else:
					binvaltime=numpy.mean(valtime)
				binvaldata=numpy.mean(valdata)
				stdev=(numpy.std(valdata))#/mt.sqrt(count0)
				bintime.append(binvaltime)
				bindata.append(binvaldata)
				binstddata.append(stdev)
				#if currentyear == 1874.:
				#	print 'binbyyear', currentyear,';', binvaltime, ';',binvaldata,';', stdev
				nvalue=nbli
				
			if i == nblines-1 :
				#print 'IN END'
				valtime=[] ; valdata=[] 
				count=0. ; count0=0. ; counts=0.
				for jj in range(nvalue, nvalue+len(time[nvalue:nbli])):
					valtime.append(float(time[jj]))
					valdata.append(float(data[jj]))
					count0+=1.
				if count0 >=200.:
					binvaltime=float(mt.modf(currentyear)[1])+0.5
				else:
					binvaltime=numpy.mean(valtime)
				binvaldata=numpy.mean(valdata)
				stdev=(numpy.std(valdata))#/mt.sqrt(count0)
				bintime.append(binvaltime)
				bindata.append(binvaldata)
				binstddata.append(stdev)
				#if currentyear == 1874.:
				#	print 'binbyyear END', currentyear,';', binvaltime, ';',binvaldata,';', stdev
			nbli+=1
			currentyear=yearval
	

	return bintime, bindata, binstddata
#===============================================================================

def remove_edges(time, data, sigma, n):
	newtime=[]
	newdata=[]
	newsigma=[]
	for i in range(0,len(time)):		
		if i >= n and i <= len(time)-n:
			newtime.append(time[i])
			newdata.append(data[i])
			newsigma.append(sigma[i])
	return newtime, newdata, newsigma

#===============================================================================
def comp_all(fc0, time1,data1,time2,data2, lastyear):
	mindiff=(1./365.25)*5. ; 	datac=[]  ; iok=0.
	for j in range(0,len(time1)):
		datea=np.asarray(time2)
		toto=(datea >= time1[j]-(mindiff/2.)) & (datea <= time1[j]+(mindiff/2.))
		print 'TIME 1', time1[j]
		if any(toto) :
			iok+=1.
			r = np.array(range(len(toto)))
			tata=np.asarray(r[toto])
			if len(tata) > 1.:
				print 'PROBLEME len(toto)'
				import pdb; pdb.set_trace()
							
			time=time2[tata[0]]
			print 'TIME 2', time, time1[j]

			if mt.modf(time)[1] <= lastyear:					
				datac.append(fc0*data2[tata[0]])
			else:
				datac.append(data2[tata[0]])
	
	if len(data1)  != len(datac):
		print 'CHECK LENGTH', len(data1), len(datac)
		import pdb; pdb.set_trace()

	prgoc, mrgoc = numpy.polyfit(data1,datac, 1,cov=True)
		
	RAG=[] ; residual=[] 
	for ii in range(0,len(data1)):
		RAG.append(prgoc[0]*data1[ii]+prgoc[1])
		residual.append(datac[ii]-(prgoc[0]*data1[ii]+prgoc[1]))



	return time1, datac, RAG, residual 



#===============================================================================
#===============================================================================
def comp_res(fc, time1,data1,time2,data2,lastyear, err1=0., err2=0., mexp=0.871, type='area'):
	if type == 'area' :
		add=0.
	else:
		add=100.
#binyearRGO, binsimRGO, yearbinR, yearlyR, 1946.
#time1 binyearRGO
#time2 yearbinR
	
	oldvalue=0.
	aa=[] ; bb=[]; tt=[] ; pp=[] ; aan=[] ; bbn=[] ; ttn=[] ; ppn=[]
	restoplot=[] ; pdf=[] ; pdfn=[]; restoplotn=[] ; iok=0.
	mindiff=(1./365.25)*5.
	
	for i in range(0,len(fc)):
		if i%50. == 0.:
			print 'FC ', i, fc[i]
		datac=[] 
		for j in range(0,len(time1)):
			if j%500. == 0.:
				print 'TIME1 ',j,  time1[j]
			datea=np.asarray(time2)
			toto=(datea >= time1[j]-(mindiff/2.)) & (datea <= time1[j]+(mindiff/2.))
			if any(toto) :
				iok+=1.
				r = np.array(range(len(toto)))
				tata=np.asarray(r[toto])
				if len(tata) > 1.:
					print 'PROBLEME len(toto)'
					import pdb; pdb.set_trace()
					
				time=time2[tata[0]]
				#print 'TIME CHECK', time1[j], time
				if mt.modf(time)[1] <= lastyear:					
					datac.append(fc[i]*data2[tata[0]])
				else:
					datac.append(data2[tata[0]])
				

		#	for k in range(0, len(time2)):
		#		
		#		if abs(time2[k]-time1[j]) <= mindiff:
		#			iok+=1.
		#			if mt.modf(time2[k])[1] <= lastyear:					
		#				datac.append(fc[i]*data2[k])
		#			else:
		#				datac.append(data2[k])
		#		#else:
		#		#	if abs(time2[k]-time1[j]) <= mindiff *6.:
		#		#		#print 'TIME', time2[k], data2[k], time1[j], data1[j], iok, abs(time2[k]-time1[j]), mindiff

		
		if len(data1) != len(datac):
			print 'PROBLEME'
			import pdb; pdb.set_trace()
		#prgoc, mrgoc, errgoc=fits.linear3fit(data1,datac)
		prgoc, mrgoc = numpy.polyfit(data1,datac, 1,cov=True)

		#print 'FIT', prgoc[0],prgoc[1]	

		RAG=[] ; residual=[] ; residuala=[] ; residualb=[]
	 	for ii in range(0,len(data1)):
			RAG.append(prgoc[0]*data1[ii]+prgoc[1])
			residual.append(datac[ii]-(prgoc[0]*data1[ii]+prgoc[1]))
			if mt.modf(time1[ii])[1] <= lastyear:
				residuala.append(datac[ii]-(prgoc[0]*data1[ii]+prgoc[1]))
			else:
				residualb.append(datac[ii]-(prgoc[0]*data1[ii]+prgoc[1]))
	
		deltaa=numpy.mean(residuala) ; deltab=numpy.mean(residualb)
		#print i, ii, deltaa, deltab
		#print 'RES ALL', fc[i], (deltaa-deltab)
	
		t,p=stats.ttest_ind(residuala,residualb, axis=0, equal_var = False)
	
		sigmaa=numpy.std(residuala) ; sigmab=numpy.std(residualb)
	
		if err1 != 0. and err2!=0.:
			errag=[]
			for ii in range(0,len(data1)):
				errag.append(prgoc[0]*mexp*data1[ii]**(mexp-1.)*err1[ii])
			sigma1a=numpy.mean(errag); sigma2a=numpy.mean(err2)
			#import pdb; pdb.set_trace()


		na=len(residuala) ; nb=len(residualb)
		a=sigmaa**2/na ; b= sigmab**2/nb
		n=(a+b)**2/((a**2/(na-1.))+(b**2/(nb-1.)))
		#print 'A,B, N ', a, b, n
		#if n >=171. :
		#	n=171.
		#pdfc=(mt.gamma((n+1)/2) / ((mt.sqrt(n*mt.pi)*mt.gamma(n/2))))* (1. + ((t**2)/n))**(-1.*((n+1)/2))
		pdfc=1.
		
		if (deltaa-deltab) >= -0.1 and (deltaa-deltab) <=0.1:
			print 'RES ', fc[i], (deltaa-deltab),prgoc[0],prgoc[1] 
			
			figname='fig14'+str(i+add).strip()
			
			figname=figure(i+add,figsize=(10.0,10.0),dpi=90)
			matplotlib.rcParams.update({'font.size': 20})
			matplotlib.rc('xtick', labelsize=15) 
			matplotlib.rc('ytick', labelsize=15) 
			
			ax1 = figname.add_subplot(211)
			#plt.axes([0.2, 0.1, 0.6, 0.8]) 
			plt.axis([firstyear,1977.,0. , 250.]) 
			plt.plot(time1,RAG, color='r', linewidth=3) 
			plt.plot(time1,datac, color='g', linewidth=3) 
			plt.title('Rc RaG')
			#plt.xlabel('Time')
			plt.ylabel('Rc / Rag')
			
			ax2 = figname.add_subplot(212)
			plt.axis([firstyear,1977.,-100, 100]) 
			plt.plot(time1,residual, color='r', linewidth=3) 
			plt.title('Residuals')
			plt.xlabel('Time')
			plt.ylabel('residuals')
			
			#plt.show()
			savefig(dirOut+'Residuals_time_'+type+'RGO_'+str(firstyear).strip()+'_'+str(lastyear).strip()+str(fc[i]).strip()+'_'+'.png',dpi=72)

			
			
			if oldvalue > 0. and (deltaa-deltab) < 0. or 	oldvalue < 0. and (deltaa-deltab) > 0.:
				fc0=(oldvalue+fc[i])/2.
				pos0=i-1.
				#with final value
				timeres, datares, Rsim, ressim=comp_all(fc0, time1,data1,time2,data2, lastyear)				
				
			oldvalue=fc[i]
			

			#import pdb; pdb.set_trace()
		restoplot.append(deltaa-deltab)
		aa.append(prgoc[0])
		bb.append(prgoc[1])
		tt.append(t)
		pp.append(p)
		#pdf.append(pdfc)
	
	mini=min(pp)
	values=[]
	for ii in range(0,len(pp)):
		values.append(mt.ceil(pp[ii]/mini))

	for ii in range(0,len(pp)):
		pdf.append(10*(values[ii]/sum(values)))
	
	toto=0. ; debut=int(pos0) ; sigmapdf=-1.
	for ii in range(debut,len(pp)):
		toto+=values[ii]
		percent=100.*(toto/sum(values))
		#print 'PERCENT ', percent
		if percent >= 34.0 and percent <= 34.5:
			sigmapdf=fc[ii]-fc0
		
	print 'SIGMA PDF', sigmapdf
	#import pdb; pdb.set_trace()
	
	
	return restoplot, aa, bb, tt, pp, pdf, fc0, Rsim, datares,ressim, sigmapdf
#===============================================================================
#===============================================================================
#===============================================================================





yearw=[] ; monthw=[] ; dayw=[] ; datew=[] ;wolf=[]

#daily Wolf
fileTable=open(dirIn+'Ri_data_1818_2015.txt','r')
strlines=fileTable.readlines()
fileTable.close()
nblines=len(strlines)
for i in range(0,nblines) :
	valyear=float(strlines[i][0:4])
	#print 'year *', strlines[i][0:4], '*'
	valmonth=float(strlines[i][4:6])
	#print 'MONTH *', strlines[i][4:6], '*'
	valday=float(strlines[i][6:8])
	#print 'DAY *', strlines[i][6:8], '*'
	valdate=float(strlines[i][10:18])
	#print 'valdate *', strlines[i][10:18], '*'
	#print 'wolf *', strlines[i][19:23], '*'
	index=strlines[i].find('?')
	if index < 0.:
		valwolf=float(strlines[i][19:23])
	else:
		valwolf=-99.
	if valyear >= firstyear:
		yearw.append(valyear)
		monthw.append(valmonth)
		dayw.append(valday)
		datew.append(valdate)
		wolf.append(valwolf)


#import pdb; pdb.set_trace()

#===============================================================================
#ADD MONTHLY R also ************************


#===============================================================================
yearmw=[] ; monthmw=[] ;datemw=[] ;wolfm=[]

#daily Wolf
fileTable=open(dirIn+'Ri_data_monthly.txt','r')
strlines=fileTable.readlines()
fileTable.close()
nblines=len(strlines)
for i in range(0,nblines) :
	valyear=float(strlines[i][0:4])
	#print 'year *', strlines[i][0:4], '*'
	valmonth=float(strlines[i][4:6])
	#print 'MONTH *', strlines[i][4:6], '*'
	valdate=float(strlines[i][7:16])
	#print 'valdate *', strlines[i][7:16], '*'
	#print 'wolf *', strlines[i][19:25], '*'
	valwolf=float(strlines[i][19:23])

	yearmw.append(valyear)
	monthmw.append(valmonth)
	datemw.append(valdate)
	wolfm.append(valwolf)


#import pdb; pdb.set_trace()

#===============================================================================

#===============================================================================
datewy=[];wolfy=[]

#yearly Wolf
#fileTable=open(dirIn+'Ri_data_yearly.txt','r')
fileTable=open(dirIn+'Ri_data_yearly_1874.txt','r')
strlines=fileTable.readlines()
fileTable.close()
nblines=len(strlines)
for i in range(0,nblines) :
	valdate=float(strlines[i][0:7])
	valwolf=float(strlines[i][7:14])
	datewy.append(valdate)
	wolfy.append(valwolf)
	#print valdate, valwolf


#import pdb; pdb.set_trace()

#===============================================================================


#===============================================================================
datenghs=[]; nghs=[]

#yearly Wolf
fileTable=open('/Users/Laure/sunspots/catalogs/GNhs_y.txt','r')
strlines=fileTable.readlines()
fileTable.close()
nblines=len(strlines)
for i in range(0,nblines) :
	valdate=float(strlines[i][0:8])
	valng=float(strlines[i][8:15])
	if valng >= 0.:
		datenghs.append(valdate)
		nghs.append(valng)
		print valdate, '*', valng


#import pdb; pdb.set_trace()

#===============================================================================

#===============================================================================
datengbb=[]; ngbb=[]

#yearly Wolf
fileTable=open('/Users/Laure/sunspots/catalogs/GNbb2_y.txt','r')
strlines=fileTable.readlines()
fileTable.close()
nblines=len(strlines)
for i in range(0,nblines) :
	valdate=float(strlines[i][0:7])
	valng=float(strlines[i][7:14])
	if valng >= 0.:
		datengbb.append(valdate)
		ngbb.append(1.1*valng)
		print valdate, '*', valng


#import pdb; pdb.set_trace()

#===============================================================================

#characterize the difference between RGO_daily_values_20150902.txt 
#and RGOSOON_daily_values_20150909.txt data... what difference does it 
#make in the yearly values (the minima are higher in the first one
# because we miss the lowest values

ngroups=[] ; areagr=[]; year=[] ; month=[]; day=[] ; date=[]

#RGO_daily_values_20150902.txt
#fileTable=open(dirIn+'RGO/RGO_daily_areas.txt','r')
#fileTable=open(dirIn+'RGO/RGO_daily_values_20150902.txt','r')
fileTable=open(dirIn+'RGO/RGOSOON_daily_values_20150909.txt','r')
strlines=fileTable.readlines()
fileTable.close()
nblines=len(strlines)
for i in range(0,nblines) :
	#print 'STRLINES', strlines[i]
	#print 'VALAREA *', strlines[i][23:29], '*'
	valarea=float(strlines[i][23:29])
	valng=float(strlines[i][19:24])
	#print 'VALNG *', strlines[i][19:24], '*'
	#print 'YEAR *', strlines[i][0:5], '*'
	valyear=float(strlines[i][0:5])
	#print 'MONTH *', strlines[i][5:8], '*'
	valmonth=float(strlines[i][5:8])
	#print 'DAY *', strlines[i][8:11], '*'
	valday=float(strlines[i][8:11])
	valdate=date_conv(valyear, valmonth, valday, 12., 0., 0.)
	if valyear >= firstyear and valyear <= lastRGO and valarea >= 0.: #limit dataset to real RGO data
	#print 'VALAREA', valarea, valyear
#	if valyear <= lastRGO and valarea >= 0.: #limit dataset to real RGO data
		year.append(valyear)
		month.append(valmonth)
		day.append(valday)
		areagr.append(valarea)
		ngroups.append(valng)
		date.append(valdate)
		print valyear, valmonth, valday, valdate, valarea, valng	
		#import pdb; pdb.set_trace()


#import pdb; pdb.set_trace()


dateRGO=date ; areaRGO=areagr ; yearRGO=year ; monthRGO=month ; ngRGO=ngroups 
#===============================================================================
binyearRGO, binngyRGO, binstngyRGO=binbyyear(dateRGO,ngRGO, yearRGO)
binyearRGO, binareayRGO, binstaryRGO=binbyyear(dateRGO,areaRGO, yearRGO)
#import pdb; pdb.set_trace()


#common RGO HS BB
dateRHS=[]; ngRHS=[] ;arRHS=[] ; ngHSR=[] ; dateHSR=[] ; ratioRGHS=[] ; ngBBR=[] ; ratioRGBB=[]

for i in range(0,len(binyearRGO)):
	datea=np.asarray(datenghs)
	dateb=np.asarray(datengbb)
	toto=(datea >= binyearRGO[i]-(0.5/365.25)) & (datea <= binyearRGO[i]+(0.5/365.25)) 
	titi=(dateb >= binyearRGO[i]-(0.5/365.25)) & (dateb <= binyearRGO[i]+(0.5/365.25))
	if any(toto) and any(titi):
		r = np.array(range(len(toto)))
		tata=np.asarray(r[toto])
		rou = np.array(range(len(titi)))
		toutou=np.asarray(r[titi])
		ngRHS.append(binngyRGO[i])
		arRHS.append(binareayRGO[i])
		dateHSR.append(binyearRGO[i])
		ngHSR.append(nghs[tata[0]])
		ngBBR.append(ngbb[toutou[0]])
		ratioRGHS.append(binngyRGO[i]/nghs[tata[0]])
		ratioRGBB.append(binngyRGO[i]/ngbb[toutou[0]])
		
		print binyearRGO[i],binngyRGO[i], nghs[tata[0]], ngbb[tata[0]]

#import pdb; pdb.set_trace()


fig26 = plt.figure(26,figsize=(4.0,6.0),dpi=300)

#plt.suptitle('Binning by days', fontsize=12)
matplotlib.rcParams.update({'font.size': 8})
matplotlib.rc('xtick', labelsize=10) 
matplotlib.rc('ytick', labelsize=10) 
plt.subplots_adjust(bottom=0.18, left=.15, right=.95, top=0.9, wspace=.03)

ax1 = fig26.add_subplot(211)
#plt.axes([0.2, 0.1, 0.6, 0.8])
#plt.plot(binyearRGO,binngyRGO, color='blue', linewidth=1) 
plt.plot(dateHSR,ngRHS, color='black', linewidth=2) 
plt.plot(dateHSR,ngHSR, color='red', linewidth=2) 
plt.plot(dateHSR,ngBBR, color='g', linewidth=2) 
plt.legend(('RGO','','H&S', 'BB'), loc=(1880, 10.)) 

plt.axis([1874,1976,0., 15])
plt.xlabel('Time')
plt.ylabel('NG')

#ax1.plot([(1, 2), (3, 4)], [(4, 3), (2, 3)])
ax2 = fig26.add_subplot(212)
#plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.plot(dateHSR,ratioRGHS, color='red', linewidth=1) 
plt.plot(dateHSR,ratioRGBB, color='g', linewidth=1) 
xx=[1874,2000]
yy=[1.,1]
plt.plot(xx,yy,'--', color='black', linewidth=1) 

plt.axis([1874,1976,0, 2])
plt.xlabel('Time')
plt.ylabel('ratio')
savefig(dirOut+"NG_RGO_HS_BB.png",dpi=300)

fig27 = plt.figure(27,figsize=(7.0,4.0),dpi=300)

#plt.suptitle('Binning by days', fontsize=12)
matplotlib.rcParams.update({'font.size': 8})
matplotlib.rc('xtick', labelsize=10) 
matplotlib.rc('ytick', labelsize=10) 
plt.subplots_adjust(bottom=0.18, left=.15, right=.95, top=0.9, wspace=.03)
xx=[1945,1945]
yy=[0.,4000.]

ax1 = fig27.add_subplot(211)
plt.axis([1830, 2015, 0, 17])
#plt.axes([0.2, 0.1, 0.6, 0.8])
#plt.plot(binyearRGO,binngyRGO, color='blue', linewidth=1) 
plt.plot(dateHSR,ngRHS, color='black', linewidth=2) 
plt.plot(xx,yy,'--', color='black', linewidth=1) 

#plt.axis([1874,1976,0., 15])
plt.xlabel('Time')
plt.ylabel('NG')

#ax1.plot([(1, 2), (3, 4)], [(4, 3), (2, 3)])
ax2 = fig27.add_subplot(212)
plt.axis([1830, 2015, 0,3100.])
#plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.plot(dateHSR,arRHS, color='black', linewidth=2) 
plt.plot(xx,yy,'--', color='black', linewidth=1) 

#plt.axis([1874,1976,0, 2])
plt.xlabel('Time')
plt.ylabel('Area')
savefig(dirOut+'NG_Area_RGO_'+str(firstyear).strip()+'_'+str(lastyear).strip()+instance+'.png',dpi=300)

#import pdb; pdb.set_trace()


#common WOLF RGO
dateRGOw=[]; areaRGOw=[] ; wolfRGO=[] ; yearRGOw=[] ; monthRGOw=[] ; ngRGOw=[]

for i in range(0,len(datew)):
	datea=np.asarray(dateRGO)
	toto=(datea >= datew[i]-(0.5/365.25)) & (datea <= datew[i]+(0.5/365.25))
	if any(toto) :
		r = np.array(range(len(toto)))
		tata=np.asarray(r[toto])
		dateRGOw.append(datew[i])
		yearRGOw.append(yearw[i])
		monthRGOw.append(monthw[i])
		areaRGOw.append(areaRGO[tata[0]])
		ngRGOw.append(ngRGO[tata[0]])
		wolfRGO.append(wolf[i])
		if i%100. == 0.:
			print datew[i],wolf[i], areaRGO[tata[0]]
#	else:
#		dateRGOw.append(datew[i])
#		areaRGOw.append(-99.)

#import pdb; pdb.set_trace()
		

#===============================================================================
#========================SUNSPOT AREA VS WOLF DAILY VAL=========================
#===============================================================================


#===============================================================================
#mexp=0.732#0.871
#===============================================================================



fig10=figure(10,figsize=(10.0,10.0),dpi=90)
#rcParams['figure.figsize'] = 10, 10
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

plt.axes([0.2, 0.1, 0.6, 0.8]) 

plt.plot(areaRGOw,wolfRGO, 'o',color='r', linewidth=1) 
#plt.axis([1981,1983,0.,4.])
#plt.xlabel('Years')
#plt.ylabel('Sunspot Number')
#plt.title('Sunspot Number SIDC')

#plt.title('Daily area RGO + SOON (ZOOM)')
plt.xlabel('Sunspot Area(msh)')
plt.ylabel('Wolf Number V1.0')
savefig(dirOut+"SunspotArea_Wolf.png",dpi=72)







#===============================================================================
#========================SUNSPOT AREA VS WOLF MONTHLY VAL=======================
#===============================================================================

#import pdb; pdb.set_trace()

#binyearRGO, binareayRGO, binstaryRGO=binbyyear(dateRGOw,areaRGOw, yearRGOw)
#binyearRGO, binngyRGO, binstngyRGO=binbyyear(dateRGOw,ngRGOw, yearRGOw)
#binyearwRGO0, binwolfyRGO0, binstwolfRGO0=binbyyear(dateRGOw,wolfRGO, yearRGOw)

#Essayer avec 
#binyearRGO0, binareayRGO0, binstaryRGO0=binbyyear(dateRGO,areaRGO, yearRGO)
#binyearRGO0, binngyRGO0, binstngyRGO0=binbyyear(dateRGO,ngRGO, yearRGO)
#binyearwRGO0, binwolfyRGO0, binstwolfRGO0=binbyyear(dateRGOw,wolfRGO, yearRGOw)
#pour voir si ca marche mieux pour NG et avec 1874 et pas 1876

#remove edges
#binyearwRGO, binwolfyRGO, binstwolfRGO=remove_edges(binyearwRGO0, binwolfyRGO0, binstwolfRGO0, 2)
#binyearRGO, binareayRGO, binstaryRGO=remove_edges(binyearRGO0, binareayRGO0, binstaryRGO0,2)
#binyearRGO, binngyRGO, binstngyRGO=remove_edges(binyearRGO0, binngyRGO0, binstngyRGO0,2)
# do not remove edges
binyearwRGO, binwolfyRGO, binstwolfRGO=binbyyear(dateRGOw,wolfRGO, yearRGOw)
binyearRGO, binareayRGO, binstaryRGO=binbyyear(dateRGO,areaRGO, yearRGO)
binyearRGO, binngyRGO, binstngyRGO=binbyyear(dateRGO,ngRGO, yearRGO)

#import pdb; pdb.set_trace()


#noise = numpy.random.normal(0.,0.3*numpy.std(binareayRGO),len(binareayRGO))
#binareayRGO0=binareayRGO


#fig40=figure(40,figsize=(10.0,10.0),dpi=90)
#matplotlib.rcParams.update({'font.size': 20})
#matplotlib.rc('xtick', labelsize=15) 
#matplotlib.rc('ytick', labelsize=15) 

#plt.axes([0.2, 0.1, 0.6, 0.8]) 

#plt.plot(binyearRGO,binareayRGO0,color='r', linewidth=2) 

##binareayRGO=binareayRGO0+noise
##for i in range(0,len(binareayRGO)):
##	if binareayRGO[i] < 0. :
##		binareayRGO[i]=0.
##

#plt.plot(binyearRGO,binareayRGO,color='g', linewidth=2) 

#plt.xlabel('Time years')
#plt.ylabel('Sunspot Area(msh)')
#savefig(dirOut+"Noise_addition_0.3.png",dpi=72)




#import pdb; pdb.set_trace()


#project yearly wolf (wolfy) on RGO dates
#i.e. keep only dates between firstyear and 1976
binyearwRGO=[] ; binwolfyRGO=[]
for i in range(0, len(wolfy)):
	if datewy[i] >= firstyear and datewy[i] <= lastRGO+0.999 :
		binyearwRGO.append(datewy[i])
		binwolfyRGO.append(wolfy[i])

#import pdb; pdb.set_trace()

if optmexp > 0.:

	fig12=figure(12,figsize=(10.0,10.0),dpi=90)
	#rcParams['figure.figsize'] = 10, 10
	matplotlib.rcParams.update({'font.size': 20})
	matplotlib.rc('xtick', labelsize=15) 
	matplotlib.rc('ytick', labelsize=15) 
	
	plt.axes([0.2, 0.1, 0.6, 0.8]) 
	mexp0=range(1000) ; mexp=[] ; rr=[] ; ppr=[]	
	rra=[] ; ppra=[] ; rrb=[] ; pprb=[]
	for i in range(0,len(mexp0)):
		mexp.append((float(mexp0[i])/666.67)+0.01)
		
		
	for i in range(0,len(mexp)):
		binsimRGO=[]; binsimRGOa=[] ;binsimRGOb=[]
		binwolfyRGOa=[] ; binwolfyRGOb=[]
		for j in range(0,len(binareayRGO)):
			binsimRGO.append(binareayRGO[j]**mexp[i])
			if mt.modf(binyearRGO[j])[1] <= lastyear:
				binsimRGOa.append(binareayRGO[j]**mexp[i])
				binwolfyRGOa.append(binwolfyRGO[j])
				
			else:
				binsimRGOb.append(binareayRGO[j]**mexp[i])
				binwolfyRGOb.append(binwolfyRGO[j])
			
		#import pdb; pdb.set_trace()

		r,pr=pearsonr(binsimRGO,binwolfyRGO)
		ra,pra=pearsonr(binsimRGOa,binwolfyRGOa)
		rb,prb=pearsonr(binsimRGOb,binwolfyRGOb)
		
		
		
		
		if r >= 0.98:
			print i, mexp[i], r, pr, ra, pra, rb, prb
		rr.append(r)
		ppr.append(pr)
		rra.append(ra)
		ppra.append(pra)
		rrb.append(rb)
		pprb.append(prb)
	correl=np.asarray(rr)
	toto=(correl >= max(rr))
	r = np.array(range(len(toto)))
	tata=np.asarray(r[toto])
	print 'RESULT', mexp[tata[0]], max(rr)
	
	
	na=len(binwolfyRGOa) ; maa=max(rra) ; pdfa=[] ; signa=[]
	for i in range(0,len(rra)):
		za=((0.5*mt.log((1.+rra[i])/(1.-rra[i])))-(0.5*mt.log((1.+maa)/(1.-maa))))/mt.sqrt((1./(na-3.))+(1./(na-3.)))
		pdfa.append(st.norm.cdf(za))
		signa.append(1.-(2.*st.norm.cdf(za)))
		print mexp[i], rra[i], maa, na, za, (1.-(2.*st.norm.cdf(za)))
	correl=np.asarray(rra)
	toto=(correl >= max(rra))
	r = np.array(range(len(toto)))
	tata=np.asarray(r[toto])
	
	print 'RESULT A', mexp[tata[0]], max(rra)
	
	nb=len(binwolfyRGOb) ; mab=max(rrb) ; pdfb=[] ; signb=[]
	for i in range(0,len(rrb)):
		zb=((0.5*mt.log((1.+rrb[i])/(1.-rrb[i])))-(0.5*mt.log((1.+mab)/(1.-mab))))/mt.sqrt((1./(nb-3.))+(1./(nb-3.)))
		pdfb.append(st.norm.cdf(zb))
		signb.append(1.-(2.*st.norm.cdf(zb)))
		print mexp[i], rrb[i], mab, nb, zb, (1.-(2.*st.norm.cdf(zb)))
	correl=np.asarray(rrb)
	toto=(correl >= max(rrb))
	r = np.array(range(len(toto)))
	tata=np.asarray(r[toto])
	
	print 'RESULT B', mexp[tata[0]], max(rrb)
	resexp0=mexp[tata[0]]
	
	significance=[]
	for i in range(0,len(mexp)):
		significance.append((1.-signa[i])*(1.-signb[i]))
	correl=np.asarray(significance)
	toto=(correl >= max(significance))
	r = np.array(range(len(toto)))
	tata=np.asarray(r[toto])
	
	print 'RESULTS combined', mexp[tata[0]]
	#import pdb; pdb.set_trace()
		
	resexp=mexp[tata[0]]
	
	fig20=figure(20,figsize=(10.0,10.0),dpi=90)
	#rcParams['figure.figsize'] = 10, 10
	matplotlib.rcParams.update({'font.size': 20})
	matplotlib.rc('xtick', labelsize=15) 
	matplotlib.rc('ytick', labelsize=15) 
	
	plt.axes([0.2, 0.1, 0.6, 0.8]) 
	plt.plot(mexp,rr, color='black', linewidth=3) 
	plt.plot(mexp,rra, color='red', linewidth=3) 
	plt.plot(mexp,rrb, color='blue', linewidth=3) 
	xx=[0.871,0.871] ; yy=[0., 1.]
	plt.plot(xx,yy, '--', color='black', linewidth=2) 
	xx=[resexp,resexp] ; yy=[0., 1.]
	plt.plot(xx,yy, '--', color='r', linewidth=2) 
	
	plt.axis([0.,1.5,0.8, 1.])
	#plt.xlabel('Years')
	#plt.ylabel('Sunspot Number')
	#plt.title('Sunspot Number SIDC')
	
	#plt.title('p value T-Test')
	plt.xlabel('m factor')
	plt.ylabel('correlation')
	savefig(dirOut+'CorrelationAreaRGO_'+str(firstyear).strip()+'_'+str(lastyear).strip()+'_'+str(resexp).strip()+instance+'.png',dpi=72)
	
	
	fig21=figure(21,figsize=(10.0,10.0),dpi=90)
	#rcParams['figure.figsize'] = 10, 10
	matplotlib.rcParams.update({'font.size': 20})
	matplotlib.rc('xtick', labelsize=15) 
	matplotlib.rc('ytick', labelsize=15) 
	
	plt.axes([0.2, 0.1, 0.6, 0.8]) 
	#plt.plot(mexp,sign, color='black', linewidth=3) 
	plt.plot(mexp,signa, color='red', linewidth=3) 
	plt.plot(mexp,signb, color='blue', linewidth=3) 
	xx=[0.871,0.871] ; yy=[0., 1.]
	plt.plot(xx,yy, '--', color='black', linewidth=2) 
	xx=[resexp,resexp] ; yy=[0., 1.]
	plt.plot(xx,yy, '--', color='r', linewidth=2) 
	
	#plt.axis([min(dateRGO),max(dateRGO),0., 40.])
	#plt.xlabel('Years')
	#plt.ylabel('Sunspot Number')
	#plt.title('Sunspot Number SIDC')
	
	#plt.title('p value T-Test')
	plt.xlabel('m factor')
	plt.ylabel('Significance')
	savefig(dirOut+'SignAreaRGO_'+str(firstyear).strip()+'_'+str(lastyear).strip()+'_'+str(resexp).strip()+instance+'.png',dpi=72)
	
	
	fig22=figure(22,figsize=(10.0,10.0),dpi=90)
	#rcParams['figure.figsize'] = 10, 10
	matplotlib.rcParams.update({'font.size': 20})
	matplotlib.rc('xtick', labelsize=15) 
	matplotlib.rc('ytick', labelsize=15) 
	
	plt.axes([0.2, 0.1, 0.6, 0.8]) 
	plt.plot(mexp,significance, color='black', linewidth=3) 
	xx=[0.871,0.871] ; yy=[0., 1.]
	plt.plot(xx,yy, '--', color='black', linewidth=2) 
	xx=[resexp,resexp] ; yy=[0., 1.]
	plt.plot(xx,yy, '--', color='r', linewidth=2) 
	
	#plt.axis([min(dateRGO),max(dateRGO),0., 40.])
	#plt.xlabel('Years')
	#plt.ylabel('Sunspot Number')
	#plt.title('Sunspot Number SIDC')
	
	#plt.title('p value T-Test')
	plt.xlabel('m factor')
	plt.ylabel('(1-Sa)(1-Sb)')
	savefig(dirOut+'ProbAreaRGO_'+str(firstyear).strip()+'_'+str(lastyear).strip()+'_'+str(resexp).strip()+instance+'.png',dpi=72)
	
	
	
	
	
	
	fig25 = plt.figure(25,figsize=(4.0,6.0),dpi=300)
	
	#plt.suptitle('Binning by days', fontsize=12)
	matplotlib.rcParams.update({'font.size': 8})
	matplotlib.rc('xtick', labelsize=10) 
	matplotlib.rc('ytick', labelsize=10) 
	plt.subplots_adjust(bottom=0.18, left=.15, right=.95, top=0.9, wspace=.03)
	
	
	
	#ax1 = fig11b.add_subplot(331)
	#plt.errorbar(meanRi,meanratio, yerr=stdratio,color='black', fmt='o')
	#plt.axis([0., 250,1.05, 1.22])
	#plt.title('bin=1d + bin Ri = '+ str(binsize))
	
	ax1 = fig25.add_subplot(311)
	#plt.axes([0.2, 0.1, 0.6, 0.8]) 
	plt.plot(mexp,rr, color='black', linewidth=3) 
	plt.plot(mexp,rra, color='red', linewidth=3) 
	plt.plot(mexp,rrb, color='blue', linewidth=3) 
	xx=[0.871,0.871] ; yy=[0., 1.]
	plt.plot(xx,yy, '--', color='black', linewidth=2) 
	xx=[resexp,resexp] ; yy=[0., 1.]
	plt.plot(xx,yy, '--', color='r', linewidth=2) 
	
	plt.axis([0.,1.5,0.8, 1.])
	plt.xlabel('m factor')
	plt.ylabel('correlation')
	
	#ax1.plot([(1, 2), (3, 4)], [(4, 3), (2, 3)])
	ax2 = fig25.add_subplot(312)
	#plt.axes([0.2, 0.1, 0.6, 0.8]) 
	plt.plot(mexp,signa, color='red', linewidth=3) 
	plt.plot(mexp,signb, color='blue', linewidth=3) 
	xx=[0.871,0.871] ; yy=[0., 1.]
	plt.plot(xx,yy, '--', color='black', linewidth=2) 
	xx=[resexp,resexp] ; yy=[0., 1.]
	plt.plot(xx,yy, '--', color='r', linewidth=2) 
	plt.axis([0.,1.5,0.0, 1.])
	plt.xlabel('m factor')
	plt.ylabel('Significance')
	
	ax3 = fig25.add_subplot(313)
	#plt.axes([0.2, 0.1, 0.6, 0.8]) 
	plt.plot(mexp,significance, color='black', linewidth=3) 
	xx=[0.871,0.871] ; yy=[0., 1.]
	plt.plot(xx,yy, '--', color='black', linewidth=2) 
	xx=[resexp,resexp] ; yy=[0., 1.]
	plt.plot(xx,yy, '--', color='r', linewidth=2) 
	plt.axis([0.,1.5,0.0, 1.])
	plt.xlabel('m factor')
	plt.ylabel('(1-Sa)(1-Sb)')
	
	
	savefig(dirOut+'Correlations_AreaRGO_'+str(firstyear).strip()+'_'+str(lastyear).strip()+'_'+str(resexp).strip()+instance+'.png',dpi=300)
	#combined
	mexp=resexp
	#after jump
	#mexp=resexp0
else:
	mexp=0.871	
#	mexp=0.732	
	
#import pdb; pdb.set_trace()

binsimRGO=[]
for i in range(0,len(binareayRGO)):
	binsimRGO.append(binareayRGO[i]**mexp)



yearbinR0, yearlyR0, erryR=binbyyear(datew, wolf, yearw)
#yearbinR=datewy
#yearlyR=wolfy

yearbinR=yearbinR0
yearlyR=yearlyR0
#erryR=erryR

#print len(wolfy),len(yearlyR0) 




monthbinR=datemw
monthlyR=wolfm

fco=range(1000) ; fc=[] 	
for i in range(0,len(fco)):
	fc.append((float(fco[i])/2500.)+0.9)

	
print 'AG'
restoplot, aa, bb, tt, pp, pdf, fca, RAG, yearlyRc, residualag, sigmaag=comp_res(fc, binyearRGO, binsimRGO, yearbinR, yearlyR,lastyear, binstaryRGO, erryR, mexp, type='area')

timeres, datares, Rsim, ressim=comp_all(fca, binyearRGO, binsimRGO, yearbinR, yearlyR, lastyear)				


fig14=figure(14,figsize=(10.0,10.0),dpi=300)
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

ax1 = fig14.add_subplot(211)
#plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.axis([1874,1977,0., 250.])
plt.plot(binyearRGO,RAG, color='r', linewidth=3) 
plt.plot(binyearRGO,yearlyRc, color='g', linewidth=3) 
plt.title('Rc RaG')
#plt.xlabel('Time')
plt.ylabel('Rc / Rag')

ax2 = fig14.add_subplot(212)
#plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.axis([1874,1977,-100, 100.])
plt.plot(binyearRGO,residualag, color='r', linewidth=3) 
plt.title('Residuals')
plt.xlabel('Time')
plt.ylabel('residuals')

#plt.show()
savefig(dirOut+'Residuals_time_AreaRGO_'+str(fca).strip()+'_'+str(firstyear).strip()+'_'+str(lastyear).strip()+instance+'.png',dpi=300)





print 'END AG', fca
print 'NG'
restoplotn, aan, bbn, ttn, ppn, pdfn, fcn, RNG, yearlyRc, residualng, sigmang=comp_res(fc, binyearRGO, binngyRGO, yearbinR, yearlyR,lastyear, binstngyRGO, erryR, 1., type='Ng')
print 'END NG', fcn


fig16=figure(16,figsize=(10.0,10.0),dpi=90)
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

ax1 = fig16.add_subplot(211)
#plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.axis([1874,1977,0., 250.])
plt.plot(binyearRGO,RNG, color='r', linewidth=3) 
plt.plot(binyearRGO,yearlyRc, color='g', linewidth=3) 
plt.title('Rc RNG')
#plt.xlabel('Time')
plt.ylabel('Rc / RNG')

ax2 = fig16.add_subplot(212)
#plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.axis([1874,1977,-100, 100.])
plt.plot(binyearRGO,residualng, color='r', linewidth=3) 
plt.title('Residuals')
plt.xlabel('Time')
plt.ylabel('residuals')

#plt.show()
savefig(dirOut+'Residuals_time_NGRGO_'+str(fcn).strip()+'_'+str(firstyear).strip()+'_'+str(lastyear).strip()+instance+'.png',dpi=72)


print 'yearly AG ', firstyear, lastyear, mexp, fca , sigmaag
print 'yearly NG ', firstyear, lastyear, '1 ', fcn , sigmang
#print fca, fcn

fig12=figure(12,figsize=(10.0,10.0),dpi=90)
#rcParams['figure.figsize'] = 10, 10
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.plot(fc,restoplot, color='red', linewidth=3) 
xx=[0.9,1.3] ; yy=[0.,0.]
plt.plot(xx,yy, color='black', linewidth=3) 

#plt.axis([min(dateRGO),max(dateRGO),0., 40.])
#plt.xlabel('Years')
#plt.ylabel('Sunspot Number')
#plt.title('Sunspot Number SIDC')

plt.title('Residuals')
plt.xlabel('Correction factor')
plt.ylabel('deltaa-deltab')
savefig(dirOut+'ResidualsAreaRGO_'+str(firstyear).strip()+'_'+str(lastyear).strip()+'_'+str(mexp).strip()+instance+'.png',dpi=72)


#import pdb; pdb.set_trace()

fig15=figure(15,figsize=(10.0,10.0),dpi=90)
#rcParams['figure.figsize'] = 10, 10
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.axis([0.9, 1.3, 0., 0.1]) 
plt.plot(fc,pdf, color='red', linewidth=3) 
xx=[1.159,1.159] ; yy=[0., 1.]
xx=[fca,fca] ; yy=[0., 1.]
plt.plot(xx,yy, color='black', linewidth=2) 

xxp=[fca+2.*sigmaag,fca+2.*sigmaag]
xxm=[fca-2.*sigmaag,fca-2.*sigmaag]
plt.plot(xxm,yy, '--', color='red', linewidth=2) 
plt.plot(xxp,yy, '--', color='red', linewidth=2) 
plt.text(0.95, 0.01,'SIGMA= '+str(sigmaag).strip(), fontsize=13, color='r')
#plt.axis([min(dateRGO),max(dateRGO),0., 40.])
#plt.xlabel('Years')
#plt.ylabel('Sunspot Number')
#plt.title('Sunspot Number SIDC')

#plt.title('p value T-Test')
plt.xlabel('Correction factor')
plt.ylabel('pdf p T-Test')
savefig(dirOut+'PDFvalueAreaRGO_'+str(firstyear).strip()+'_'+str(lastyear).strip()+'_'+str(mexp).strip()+instance+'.png',dpi=72)


fig30=figure(30,figsize=(10.0,10.0),dpi=90)
#rcParams['figure.figsize'] = 10, 10
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.axis([0.9, 1.3, 0., 1.]) 
plt.plot(fc,pp, color='red', linewidth=3) 
xx=[1.159,1.159] ; yy=[0., 1.]
xx=[fca,fca] ; yy=[0., 1.]
plt.plot(xx,yy, color='black', linewidth=2) 

xxp=[fca+2.*sigmaag,fca+2.*sigmaag]
xxm=[fca-2.*sigmaag,fca-2.*sigmaag]
plt.plot(xxm,yy, '--', color='red', linewidth=2) 
plt.plot(xxp,yy, '--', color='red', linewidth=2) 
plt.text(0.95, 0.1,'SIGMA= '+str(sigmaag).strip(), fontsize=13, color='r')
#plt.axis([min(dateRGO),max(dateRGO),0., 40.])
#plt.xlabel('Years')
#plt.ylabel('Sunspot Number')
#plt.title('Sunspot Number SIDC')

#plt.title('p value T-Test')
plt.xlabel('Correction factor')
plt.ylabel('p value T-Test')
savefig(dirOut+'PvalueAreaRGO_'+str(firstyear).strip()+'_'+str(lastyear).strip()+'_'+str(mexp).strip()+instance+'.png',dpi=72)





import pdb; pdb.set_trace()


#MONTHLY DATA
binmonthRGO, binareamRGO, binstarmRGO=binbymonth(dateRGOw,areaRGOw, yearRGOw, monthRGOw)
binmonthwRGO, binwolfmRGO, binstwolfRGO=binbymonth(dateRGOw,wolfRGO, yearRGOw, monthRGOw)
binmonthmRGO, binngmRGO, binstngmRGO=binbymonth(dateRGOw,ngRGOw,yearRGOw, monthRGOw)
fig11=figure(11,figsize=(10.0,10.0),dpi=90)
#rcParams['figure.figsize'] = 10, 10
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

plt.axes([0.2, 0.1, 0.6, 0.8]) 

plt.plot(binareamRGO,binwolfmRGO, 'o',color='r', linewidth=1) 
#plt.plot(binareamSOON,binwolfmSOON, 'x',color='b', linewidth=1) 
#plt.axis([1981,1983,0.,4.])
#plt.xlabel('Years')
#plt.ylabel('Sunspot Number')
#plt.title('Sunspot Number SIDC')

#plt.title('Daily area RGO + SOON (ZOOM)')
plt.xlabel('Monthly Sunspot Area(msh)')
plt.ylabel('Monthly Wolf Number V1.0')
savefig(dirOut+"Monthly_SunspotArea_Wolf.png",dpi=72)

#import pdb; pdb.set_trace()

binsimmRGO=[]
for i in range(0,len(binareamRGO)):
	binsimmRGO.append(binareamRGO[i]**mexp)
#import pdb; pdb.set_trace()
restoplotm, aam, bbm, ttm, ppm, pdfm, fcam, RAGm, monthlyRc, residualam, sigmaam=comp_res(fc, binmonthRGO, binsimmRGO, monthbinR, monthlyR, lastyear)
print 'END AG monthly', fcam

print fca, fcn, fcam

import pdb; pdb.set_trace()


fig17=figure(17,figsize=(10.0,10.0),dpi=90)
#rcParams['figure.figsize'] = 10, 10
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.plot(fc,restoplotn, color='red', linewidth=3) 
xx=[0.9,1.3] ; yy=[0.,0.]
plt.plot(xx,yy, color='black', linewidth=3) 

#plt.axis([min(dateRGO),max(dateRGO),0., 40.])
#plt.xlabel('Years')
#plt.ylabel('Sunspot Number')
#plt.title('Sunspot Number SIDC')

plt.title('Residuals')
plt.xlabel('Correction factor')
plt.ylabel('deltaa-deltab')
savefig(dirOut+'ResidualsNGRGO_'+str(firstyear).strip()+'_'+str(lastyear).strip()+'_'+str(mexp).strip()+instance+'.png',dpi=72)


#import pdb; pdb.set_trace()

fig18=figure(18,figsize=(10.0,10.0),dpi=90)
#rcParams['figure.figsize'] = 10, 10
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.plot(fc,ppn, color='red', linewidth=3) 
xx=[1.159,1.159] ; yy=[0., 1.]
plt.plot(xx,yy, color='black', linewidth=2) 

#plt.axis([min(dateRGO),max(dateRGO),0., 40.])
#plt.xlabel('Years')
#plt.ylabel('Sunspot Number')
#plt.title('Sunspot Number SIDC')

#plt.title('p value T-Test')
plt.xlabel('Correction factor')
plt.ylabel('p value T-Test')
savefig(dirOut+'PvalueNGRGO_'+str(firstyear).strip()+'_'+str(lastyear).strip()+'_'+str(mexp).strip()+instance+'.png',dpi=72)


import pdb; pdb.set_trace()



pdfp=[] 
for i in range(0,len(pp)-1):
	value=pp[i]/(fc[i]*10.)
	pdfp.append(value)
#import pdb; pdb.set_trace()

fig16=figure(16,figsize=(10.0,10.0),dpi=90)
#rcParams['figure.figsize'] = 10, 10
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.plot(tt,pdf, color='red', linewidth=3) 
xx=[1.159,1.159] ; yy=[0., 1.]
plt.plot(xx,yy, color='black', linewidth=2) 

#plt.axis([min(dateRGO),max(dateRGO),0., 40.])
#plt.xlabel('Years')
#plt.ylabel('Sunspot Number')
#plt.title('Sunspot Number SIDC')

#plt.title('p value T-Test')
plt.xlabel('Correction factor')
plt.ylabel('pdf distribution')
savefig(dirOut+'realPDFvalueAreaRGO_'+str(firstyear).strip()+'_'+str(lastyear).strip()+'_'+str(mexp).strip()+instance+'.png',dpi=72)





#import pdb; pdb.set_trace()

for i in range(0,len(binyearRGO)):
	for j in range(0, len(yearbinR)):
		if mt.modf(yearbinR[j])[1] == mt.modf(binyearRGO[i])[1]:
			#print 'comp' , binyearRGO[i], yearbinR[j]
			yearlyRrgo.append(yearlyR[j])
			if mt.modf(yearbinR[j])[1] <= lastyear:
				binsimRGOb.append(binsimRGO[i])
				binareayRGOb.append(binareayRGO[i])
				yearlyRrgob.append(yearlyR[j])
			if mt.modf(yearbinR[j])[1] > lastyear:
				yearlyRrgoa.append(yearlyR[j])
				binareayRGOa.append(binareayRGO[i])				
				binsimRGOa.append(binsimRGO[i])


prgo, mrgo, errgo=fits.linear3fit(binsimRGO,yearlyRrgo)
#import pdb; pdb.set_trace()

prgob, mrgob, errgob=fits.linear3fit(binsimRGOb,yearlyRrgob)
prgoa, mrgoa, errgoa=fits.linear3fit(binsimRGOa,yearlyRrgoa)

RAGrgo=[]
for i in range(0,len(binsimRGO)):
	RAGrgo.append(prgo[0]*binsimRGO[i]+prgo[1])
textrgo= 'All (A ='+str(prgo[0])[0:7]+'+/-'+str(errgo[0])[0:7]+')'+'x AG^0.87 + (B='+str(prgo[1])[0:7]+'+/-'+str(errgo[1])[0:7]+')'

RAGrgob=[]
for i in range(0,len(binsimRGOb)):
	RAGrgob.append(prgob[0]*binsimRGOb[i]+prgob[1])
textrgob= 'Before (A ='+str(prgob[0])[0:7]+'+/-'+str(errgob[0])[0:7]+')'+'x AG^0.87 + (B='+str(prgob[1])[0:7]+'+/-'+str(errgob[1])[0:7]+')'


RAGrgoa=[]
for i in range(0,len(binsimRGOa)):
	RAGrgoa.append(prgoa[0]*binsimRGOa[i]+prgoa[1])
textrgoa= 'After (A ='+str(prgoa[0])[0:7]+'+/-'+str(errgoa[0])[0:7]+')'+'x AG^0.87 + (B='+str(prgoa[1])[0:7]+'+/-'+str(errgoa[1])[0:7]+')'

#import pdb; pdb.set_trace()



#===============================================================================
#========================SUNSPOT AREA VS WOLF YEARLY VAL========================
#===============================================================================
fig13=figure(13,figsize=(10.0,10.0),dpi=90)
#rcParams['figure.figsize'] = 10, 10
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.plot(binareayRGO,binwolfyRGO, 'o',color='r', linewidth=1) 
#plt.plot(binareaySOON,binwolfySOON, 'x',color='b', linewidth=1) 
plt.plot(binareayRGO,RAGrgo, color='r', linewidth=1) 
plt.plot(binareayRGOb,RAGrgob, color='g', linewidth=1) 
plt.plot(binareayRGOa,RAGrgoa, color='b', linewidth=1) 
plt.text(1000, 50,textrgo, fontsize=13, color='r')
plt.text(1000, 40,textrgob, fontsize=13, color='g')
plt.text(1000, 30,textrgoa, fontsize=13, color='b')
#plt.plot(binareaySOON,binsimSOON,color='b', linewidth=1) 
#plt.axis([1981,1983,0.,4.])
#plt.xlabel('Years')
#plt.ylabel('Sunspot Number')
#plt.title('Sunspot Number SIDC')

#plt.title('Daily area RGO + SOON (ZOOM)')
plt.xlabel('Yearly Sunspot Area(msh)')
plt.ylabel('Yearly Wolf Number V1.0')
savefig(dirOut+"Yearly_SunspotArea_Wolf.png",dpi=72)



#===============================================================================
#=================================MONTLHY GROUPS RGO============================
#===============================================================================
binyearRGO, binngyRGO, binstngyRGO=binbyyear(dateRGOw,ngRGOw, yearRGOw)
fig1=figure(1,figsize=(10.0,10.0),dpi=90)
#rcParams['figure.figsize'] = 10, 10
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

plt.axes([0.2, 0.1, 0.6, 0.8]) 
bintime, binng, binstdng=binbymonth(dateRGO, ngRGO, yearRGO, monthRGO)
plt.plot(dateRGO,ngRGO, color='g', linewidth=1) 
#plt.plot(days,nbgr, color='g', linewidth=1) 
#plt.errorbar(bintime,binng, yerr=binstdng,color='black', fmt='.')
#plt.plot(bintime,binng, color='black', linewidth=3) 
plt.plot(binyearRGO,binngyRGO, color='r', linewidth=2) 
plt.axis([min(dateRGO),max(dateRGO),0., 40.])
#plt.xlabel('Years')
#plt.ylabel('Sunspot Number')
#plt.title('Sunspot Number SIDC')

plt.title('Groups per day')
plt.xlabel('Date in fraction of year')
plt.ylabel('Number of groups')
savefig(dirOut+"NBGRRGO.png",dpi=72)

#===============================================================================
#===================================MONTLHY AREA RGO============================
#===============================================================================
fig2=figure(2,figsize=(10.0,10.0),dpi=90)
#rcParams['figure.figsize'] = 10, 10
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

plt.axes([0.2, 0.1, 0.6, 0.8]) 
plt.plot(dateRGO,areaRGO, color='r', linewidth=1) 
bintime, binarea, binstdar=binbymonth(dateRGO, areaRGO, yearRGO, monthRGO)
#plt.errorbar(bintime,binarea, yerr=binstdar,color='black', fmt='.')
plt.plot(bintime,binarea, color='black', linewidth=3) 
plt.axis([min(dateRGO),max(dateRGO),0.,max(areaRGO)])
#plt.xlabel('Years')
#plt.ylabel('Sunspot Number')
#plt.title('Sunspot Number SIDC')

plt.title('Daily sunspot area')
plt.xlabel('Date in fraction of year')
plt.ylabel('Sunspot area (msh)')
savefig(dirOut+"AreaRGO.png",dpi=72)


import pdb; pdb.set_trace()

