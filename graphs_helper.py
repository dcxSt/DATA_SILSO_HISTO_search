# methods to help me display some information graphically

# import statements
import db_connection
import db_search
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
import scipy
from scipy.interpolate import spline
from scipy.ndimage.filters import gaussian_filter1d
from statsmodels.nonparametric.smoothers_lowess import lowess
import random
import math

# plotting converters
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()



# method that organises the data from good_database into dictionary 
# searchable by observer alias ; 
# key = obs_alias , value = data
def data_by_obs_alias_good():
    data = db_search.select_all_data(the_database="GOOD_DATA_SILSO")
    obs_alias_dictionary = {}
    for i in data:
        obs_alias = i[7]
        if obs_alias in obs_alias_dictionary:
            obs_alias_dictionary[obs_alias].append(i)
        else:
            obs_alias_dictionary[obs_alias]=[i]
    return obs_alias_dictionary

# same as above but for different database format
# really slow - avoid using
def data_by_obs_alias_histo(the_database="DATA_SILSO_HISTO"):
    data = db_search.select_all_data(the_database=the_database)
    observers = db_search.select_all_observers()
    obs_alias_dictionary = {}
    for i in data:
        fk_obs = i[3]
        for j in observers:
            if j[0] == fk_obs:
                obs_alias = j[1]
                if obs_alias in obs_alias_dictionary:
                    obs_alias_dictionary[obs_alias].append(i)
                else:
                    obs_alias_dictionary[obs_alias]=[i]
    #print([i for i in obs_alias_dictionary])#trace
    return obs_alias_dictionary

# returns data by observer where each observer has a list of 10 sublists (1/flag)
def get_data_by_obs_seperate_flags(the_database="GOOD_DATA_SILSO"):
    if the_database=="GOOD_DATA_SILSO":
        data_by_obs = data_by_obs_alias_good()
    else:
        data_by_obs = data_by_obs_alias_histo(the_database)
    data_by_obs_seperate_flags =  {}
    for observer in data_by_obs:
        data_by_obs_seperate_flags[observer]=[[],[],[],[],[],[],[],[],[],[]]
        for i in data_by_obs[observer]:
            if the_database=="GOOD_DATA_SILSO":
                flag = i[15]
            else:
                flag = i[10]
            
            if flag==1:
                data_by_obs_seperate_flags[observer][1].append(i)
            elif flag==2:
                data_by_obs_seperate_flags[observer][2].append(i)
            elif flag==3:
                data_by_obs_seperate_flags[observer][3].append(i)
            elif flag==4:
                data_by_obs_seperate_flags[observer][4].append(i)
            elif flag==5:
                data_by_obs_seperate_flags[observer][5].append(i)
            elif flag==6:
                data_by_obs_seperate_flags[observer][6].append(i)
            elif flag==7:
                data_by_obs_seperate_flags[observer][7].append(i)
            elif flag==8:
                data_by_obs_seperate_flags[observer][8].append(i)
            elif flag==9:
                data_by_obs_seperate_flags[observer][9].append(i)
            else:
                data_by_obs_seperate_flags[observer][0].append(i)
    return data_by_obs_seperate_flags

# shows figure of some observer's observations seperated by flag only for GOOD_DATA_SILSO
def display_seperate_flags(observer,interval=None,yaxis="Sunspots",save_as=None):
    data_by_obs_seperate_flags = get_data_by_obs_seperate_flags()
    if yaxis.lower()=="sunspots":
        yindex=3
    elif yaxis.lower()=="wolf":
        yindex=4
    elif yaxis.lower()=="groups":
        yindex=2
    else:
        print("No valid yaxis selected")
        raise Exception
    
    if interval:
        low=time.strftime(interval[0])
        high=time.strftime(interval[1])
        
    plt.figure(figsize=(15,8))
    plt.title(observer)
    plt.xlabel("Date")
    plt.ylabel(yaxis)
    
    x,y=[[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[]]#10 in each, for each flag + noflag
    for flag_section_index in range(len(data_by_obs_seperate_flags[observer])):
        for i in data_by_obs_seperate_flags[observer][flag_section_index]:
            if interval:
                date=time.strftime(str(i[1]))
                if date<= high and date>= low:
                    x[flag_section_index].append(i[1])
                    y[flag_section_index].append(i[yindex])
            else:
                x[flag_section_index].append(i[1])
                y[flag_section_index].append(i[yindex])
                
    cmap = plt.get_cmap("tab10")
    # I found cmap here
    # https://stackoverflow.com/questions/42086276/get-default-line-colour-cycle 
    
    for flag_index in range(len(x)):
        # only do this if there is anything inside, we don't want a huge legend when there are only 2 colors
        if len(x[flag_index])>0:
            plt.plot(x[flag_index],y[flag_index],"x",label="flag = "+str(flag_index),color=cmap(flag_index))
        
    plt.grid()
    plt.legend()
    if save_as:
        plt.savefig(save_as)
    plt.show()

# shows figure with 3 subfigures: groups, sunspots, wolf
def display_seperate_flags_all(observer,interval=None):
    data_by_obs_seperate_flags = get_data_by_obs_seperate_flags()
    if interval:
        low=time.strftime(interval[0])
        high=time.strftime(interval[1])

    plt.figure(figsize=(12,12))
    plt.title(observer)
    
    x=[[],[],[],[],[],[],[],[],[],[]]
    ywolf=[[],[],[],[],[],[],[],[],[],[]]
    ysunspots=[[],[],[],[],[],[],[],[],[],[]]
    ygroups=[[],[],[],[],[],[],[],[],[],[]]

    for flag_section_index in range(len(data_by_obs_seperate_flags[observer])):
        for i in data_by_obs_seperate_flags[observer][flag_section_index]:
            if interval:
                date=time.strftime(str(i[1]))
                if date<=high and date>=low:
                    x[flag_section_index].append(i[1])
                    ygroups[flag_section_index].append(i[2])
                    ysunspots[flag_section_index].append(i[3])
                    ywolf[flag_section_index].append(i[4])
            else:
                x[flag_section_index].append(i[1])
                ygroups[flag_section_index].append(i[2])
                ysunspots[flag_section_index].append(i[3])
                ywolf[flag_section_index].append(i[4])

    cmap = plt.get_cmap("tab10")

    # plot wolf
    plt.subplot(311)
    plt.xlabel("Date")
    plt.ylabel("Wolf Number")
    for flag_index in range(len(x)):
        # only plot if flag section non-empty so that legend isnt too big
        if len(x[flag_index])>0:
            plt.plot(x[flag_index],ywolf[flag_index],"x",label="flag = "+str(flag_index),color=cmap(flag_index))
    plt.grid()
    plt.legend()
       
    # plot sunpots
    plt.subplot(312)
    plt.xlabel("Date")
    plt.ylabel("Sunspots Number")
    for flag_index in range(len(x)):
        # only plot if flag section non-empty so that legend isn't too big
        if len(x[flag_index])>0:
            plt.plot(x[flag_index],ysunspots[flag_index],"x",label="flag = "+str(flag_index),color=cmap(flag_index))
    plt.grid()
    plt.legend()

    plt.subplot(313)
    plt.xlabel("Date")
    plt.ylabel("Groups Number")
    for flag_index in range(len(x)):
        # only plot if flag section non-empty so that legend isn't too big
        if len(x[flag_index])>0:
            plt.plot(x[flag_index],ygroups[flag_index],"x",label="flag = "+str(flag_index),color=cmap(flag_index))
    plt.grid()
    plt.legend()

    plt.show()

# takes observer alias and g/s/r and plots different databases in different colors
# plots nothing if there 
def display_all_databases(observer,interval=None,yaxis="Sunspots",save_as=None,zero_if_null=False):
    obs_dic_good = data_by_obs_alias_good()
    obs_dic_bad = data_by_obs_alias_histo(the_database="BAD_DATA_SILSO")
    obs_dic_histo = data_by_obs_alias_histo(the_database="DATA_SILSO_HISTO")
    
    if yaxis.lower() == "sunspots":
        # indices = (histo_index ,  good_index)
        indices = (5,3)
    elif yaxis.lower() == "wolf":
        indices = (6,4)
    elif yaxis.lower() == "groups":
        indices = (4,2)
    else:
        print("yaxis not correct, can only be 'groups', 'sunspots' or 'wolf'")
        raise Exception

    if interval:
        low = time.strftime(interval[0])
        high = time.strftime(interval[1])
    
    # plot the data
    plt.figure(figsize=(12,9))
    plt.title(observer)
    plt.xlabel("Date")
    plt.ylabel(yaxis)

    cmap = plt.get_cmap("tab10")# colors

    # make lists of data from GOOD_DATA_SILSO, and plot
    try:
        if interval:
            [xgood,ygood] = np.transpose([[i[1],i[indices[1]]] for i in obs_dic_good[observer] if time.strftime(i[1]) >= low and time.strftime(i[1]) < high and i[indices[1]]!=None])
        else:
            [xgood,ygood] = np.transpose([[i[1],i[indices[1]]] for i in obs_dic_good[observer] if i[indices[1]]!=None])
        plt.plot(xgood,ygood,"o",label="GOOD_DATA_SILSO",color=(0.5,0.99,0.5,1.0))
    except:
        print("no data for god")
        pass

    # make lists of data from BAD_DATA_SILSO, in red
    try:
        if interval:
            [xbad,ybad] = np.transpose([[i[1],i[indices[0]]] for i in obs_dic_bad[observer] if time.strftime(i[1]) > low and time.strftime(i[1]) < high and i[indices[0]!=None]])
        else:
            [xbad,ybad] = np.transpose([[i[1],i[indices[0]]] for i in obs_dic_bad[observer] if i[indices[0]]!=None])
        plt.plot(xbad,ybad,"o",label="BAD_DATA_SILSO",color=(0.55,0.8,1.0,1.0))
    except:
        print("no data for bad")
        pass

    # make lists of data from DATA_SILSO_HISTO, in red
    try:
        if interval:
            [xhisto,yhisto] = np.transpose([[i[1],i[indices[0]]] for i in obs_dic_histo[observer] if time.strftime(i[1]) > low and time.strftime(i[1]) < high and i[indices[0]]!=None])
        else:
            [xhisto,yhisto] = np.transpose([[i[1],i[indices[0]]] for i in obs_dic_histo[observer] if i[indices[0]]!=None])
        plt.plot(xhisto,yhisto,"x",label="DATA_SILSO_HISTO",color=(1.0,0.4,0.4,1.0))
    except:
        print("no data for silso histo")
        pass
    
    plt.legend()
    if save_as:
        plt.savefig(save_as)
    plt.show()
    

# takes observerS aliases and database and plots each observer on the same plot.
# This function has alot of functionality, it's work listing it out.\n
# interval = 2d-tuple (date1,date2) with date1<date2\n
# figsize size of the figure also 2d-tuple\n
# online_sn (boolean) if True plots a smoothed plot of the current sunspot number V2.0 with smoothing factor smoothness\n
# exclude_these_rubrics is a list of rubrics number you don't want to plot, leave list empty if none
def display_compare_observers(observers,the_database="DATA_SILSO_HISTO",
interval=None,save_as=None,figsize=(12,17),online_sn=False,smoothness=50.0,
exclude_these_rubrics=[],include_flags=(None,0,1,2,3,4,5,6,7,8,9)):
    if the_database=="GOOD_DATA_SILSO":
        obs_dic = data_by_obs_alias_good()
        gindex,sindex,windex = 2,3,4
        rubricsindex = 12
        flagindex = 15
    else:
        obs_dic = data_by_obs_alias_histo(the_database=the_database)
        gindex,sindex,windex = 4,5,6
        rubricsindex = 2
        rubrics = db_search.select_all_rubrics()
        exclude_these_rubrics = [i[0] for i in rubrics if i[1] in exclude_these_rubrics]# replace rubrics_number with fk_rubrics 
        flagindex = 10

    if interval:
        low = time.strftime(interval[0])
        high = time.strftime(interval[1])

    
    if len(observers) > 10:
        cmap = plt.get_cmap("tab20")# cmap = color map
    else:
        cmap = plt.get_cmap("tab10")# cmap = color map

    # plot the figures
    plt.figure(figsize=figsize)

    # GROUPS
    plt.subplot(311)
    plt.title("comparing observers groups")
    count=0
    for observer in observers:
        try:
            if interval:
                [x,y] =np.transpose([[i[1],i[gindex]] for i in obs_dic[observer] if time.strftime(str(i[1]))>= low and time.strftime(str(i[1]))<= high and i[gindex]!=None and i[rubricsindex] not in exclude_these_rubrics and i[flagindex] in include_flags])
            else:
                [x,y] = np.transpose([[i[1],i[gindex]] for i in obs_dic[observer] if i[gindex]!=None and i[rubricsindex] not in exclude_these_rubrics and i[flagindex] in include_flags])
            plt.plot(x,y,"x",label=observer,color=cmap(count))
        except:
            print("no data for "+observer+" in groups")
            pass
        count+=1
    plt.legend()
    plt.grid()
    plt.xlabel("Date")
    plt.ylabel("Groups")

    # SUNSPOTS
    plt.subplot(312)
    plt.title("comparing observers sunspots")
    count=0
    for observer in observers:
        try:
            if interval:
                [x,y] = np.transpose([[i[1],i[sindex]] for i in obs_dic[observer] if time.strftime(str(i[1]))>= low and time.strftime(str(i[1]))<= high and i[sindex]!=None and i[flagindex] in include_flags])
            else:
                [x,y] = np.transpose([[i[1],i[sindex]] for i in obs_dic[observer] if i[sindex]!=None and i[flagindex] in include_flags])
            plt.plot(x,y,"x",label=observer,color=cmap(count))
        except:
            print("no data for "+observer+" in sunspots")#trace
            pass
        count+=1
    plt.legend()
    plt.grid()
    plt.xlabel("Date")
    plt.ylabel("Sunspots")

    # WOLF
    plt.subplot(313)
    plt.title("comparing observers wolf")
    count=0
    online_interval = None
    for observer in observers:
        try:
            if interval:
                [x,y] = np.transpose([[i[1],i[windex]] for i in obs_dic[observer] if time.strftime(str(i[1]))>=low and time.strftime(str(i[1]))<= high and i[windex]!=None and i[flagindex] in include_flags])
            else:
                [x,y] = np.transpose([[i[1],i[windex]] for i in obs_dic[observer] if i[windex]!=None and i[flagindex] in include_flags])
            plt.plot(x,y,"x",label=observer,color=cmap(count))
            # find interval for the potential smooth
            if online_interval==None:
                online_interval = (min(x),max(x))
            elif online_interval[0]>min(x): online_interval = (min(x),online_interval[1])
            elif online_interval[1]<max(x): online_interval = (online_interval[0],max(x))
        except:
            print("no data for "+observer+" in wolf")#trace
            pass
        count+=1
    
    # plot the online smoothed sunspot value
    if online_sn==True:
        x,y_smooth = get_smoothed_sn(interval=online_interval,smoothness=smoothness)
        plt.plot(x,y_smooth,"-",color=(0.0,0.0,0.0,0.5),label="smoothed official sn v2.0")
    
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Wolf")
    plt.grid()

    if save_as:
        plt.savefig(save_as)
    plt.show()


# takes date interval and returns x,y arrays of smoothed data to plot from the online sunspots number
# the higher the smoothness, the smoother the plot
def get_smoothed_sn(interval=(dt.date(1880,1,1),dt.date(1920,1,1)),smoothness=20.0):
    data = db_search.select_online_sn()
    if interval==None:
        x_date = [i[0] for i in data]
        x = [i[1] for i in data]
        y = [i[2] for i in data]
    else:
        x_date = [i[0] for i in data if i[0] > interval[0] and i[0] < interval[1]]
        x = [i[1] for i in data if i[0] > interval[0] and i[0] < interval[1]]
        y = [i[2] for i in data if i[0] > interval[0] and i[0] < interval[1]]

    filtered = lowess(y,x,is_sorted=True,frac=float(smoothness)/len(x),it=0)
    x_smooth = filtered[:,0]
    y_smooth = filtered[:,1]
    return x_date,y_smooth


# Plots the drift of an observer, uses wolf number V.2.0 as baseline
# \n- interval takes string tuple of len 2
# \n- squish_wolf is to squish the scaling factor of wolf number plotted
# \n- cutoff is a factor that determines where you start cutting off outlier data
# \nThe slope displayed is indicative of drift
def display_wolf_drift(observer,the_database="DATA_SILSO_HISTO",
interval=None,save_as=None,figsize=(15,11),squish_wolf=0.005,cutoff=4):
    if the_database=="GOOD_DATA_SILSO":
        obs_dic = data_by_obs_alias_good()
        windex = 4
    else:
        obs_dic = data_by_obs_alias_histo(the_database=the_database)
        windex = 6
    if interval:
        low = dt.date(int(interval[0][:4]),int(interval[0][5:7]),int(interval[0][8:10]))
        high = dt.date(int(interval[1][:4]),int(interval[1][5:7]),int(interval[1][8:10]))

    

    # get the data
    if interval:
        [x,y] = np.transpose([[i[1],i[windex]] for i in obs_dic[observer] if i[1]>=low and i[1]<=high and i[windex]!=None])
    else:
        [x,y] = np.transpose([[i[1],i[windex]] for i in obs_dic[observer] if i[windex]!=None])
    x,y=list(x),list(y)

    # plot the figure
    plt.figure(figsize=figsize)
    plt.title("Wolf Drift "+str(observer))
    plt.plot(x,[squish_wolf*i for i in y],"o",color=(0.2,0.2,1.0,0.05),label="scaled wolf "+observer)
    x_smooth,y_smooth = get_smoothed_sn(interval=(np.array(x).min(),np.array(x).max()),smoothness=60)
    plt.plot(x_smooth,[squish_wolf*i for i in y_smooth],"-",color=(0.0,0.0,0.0,0.3),label="scaled wolf official v2.0")

    # get the data for the official sn
    online_data = db_search.select_online_sn()
    x_online,y_online = [],[]
    for i in online_data:
        if i[0] in x:
            x_online.append(i[0])
            y_online.append(i[2])

    # the online data has holes in it so we need to get rid of those for the x
    x_new,y_new=[],[]
    for i in range(len(x_online)):
        x_new.append(x_online[i])
        y_new.append(y[x.index(x_online[i])])
    x,y=x_new[:],y_new[:]
    
    print(list(x)==list(x_online))

    y_plot = [(y[i]-y_online[i])/(y_online[i]+1) for i in range(len(x))]
    
    # plot the mean
    y_mean = np.mean(y_plot)
    plt.plot([np.array(x).min(),np.array(x).max()],[y_mean,y_mean],'-',color=(0.1,0.9,0.1,0.4),label="mean")# plot the mean

    #plt.plot([np.array(x).min(),np.array(x).max()],[cutoff*y_mean,cutoff*y_mean],'-',label="cutoff1",color=(0.0,1.0,0.0,0.2))
    #plt.plot([np.array(x).min(),np.array(x).max()],[-cutoff*y_mean,-cutoff*y_mean],'-',label="cutoff2",color=(0.0,1.0,0.0,0.2))
    
    # get rid of outliers
    x_exclude_outliers,y_plot_exclude_outliers=[],[]
    for i in range(len(x)):
        if np.abs(y_mean)*cutoff>np.abs(y_plot[i]):
            x_exclude_outliers.append(x[i])
            y_plot_exclude_outliers.append(y_plot[i])
    
    plt.plot(x_exclude_outliers,y_plot_exclude_outliers,"rx",label="frac{obs - sn2.0}{sn2.0 + 10}")

    # get rid of zeros to do line of best fit for the rest
    x_exclude_zeros,y_plot_exclude_zeros=[],[]
    for i in range(len(x_exclude_outliers)):
        if y_plot_exclude_outliers[i]!=0:
            x_exclude_zeros.append(x_exclude_outliers[i])
            y_plot_exclude_zeros.append(y_plot_exclude_outliers[i])

    y_mean_no0 = np.mean(y_plot_exclude_zeros)
    plt.plot([np.array(x).min(),np.array(x).max()],[y_mean_no0,y_mean_no0],"-",color=(0.2,0.9,0.9,0.8),label="mean no zero")# plot the new mean

    # line of best fit (2 variables)
    x_exclude_zeros_decimal = dates_to_decimal(x_exclude_zeros)
    popt,pcov = scipy.optimize.curve_fit(line,x_exclude_zeros_decimal,y_plot_exclude_zeros,p0=[0,0])
    [a,b] = popt
    yline = [line(i,a,b) for i in x_exclude_zeros_decimal]
    plt.plot(x_exclude_zeros,yline,'b-',label="slope = "+str(a))

    # now I want to plot a line of best fit
    # we want to exclude all those points that are 0 because they don't really tell us anything
    
    plt.xlabel("Date")
    plt.ylabel("frac{obs - v2.0}{v2.0}")
    
    plt.grid()
    plt.legend()
    if save_as:
        plt.savefig(save_as)
    plt.show()

# converts an array of dates into an array of floats that represent dates
def dates_to_decimal(dates):
    decimal_dates=[]
    for d in dates:
        year = int(str(d)[:4])
        month = int(str(d)[5:7])
        day = int(str(d)[8:10])
        days=day
        for i in range(1,month+1):
            if i in [2,4,6,8,9,11]:# 31 days
                days+=31
            elif i == 3 and year%4==0:# feb leapyear
                days+=29
            elif i==3:
                days+=28
            elif i in [5,7,10,12]:
                days+=30
        if year%4==0:
            days_decimal=days/366.
        else:
            days_decimal=days/365.
        decimal_date = year + days_decimal
        decimal_dates.append(decimal_date)
    return decimal_dates

# converts an array of decimal_dates to array of dates
def decimal_to_dates(dates):
    real_dates=[]
    mon_len = [31,28,31,30,31,30,31,31,30,31,30,31]
    for d in dates:
        year = int(d)
        if year%4==0:# leap year
            days = int((d-year)*366+0.5)
            real_dates[1]=29
        else:
            days = int((d-year)*365+0.5)
            real_dates[1]=28
        m=0
        while mon_len[m] < days:
            days -= mon_len[m]
            m+=1
        month = m+1
        day = days
        real_dates.append(dt.date(year,month,day))
    return real_dates

# line of best fit 2 unknowns function
# it's a helper function for those that are using scipy.optimize.curve_fit for a line of best fit
def line(x,a,b):
    return a*x + b

# method to identify observers in DATA_SILSO_HISTO.OBSERVERS and how much data is associated with each one
def size_data_by_observer_hist():
    observers = db_search.select_all_observers()
    data = db_search.select_all_data()
    #obs_alias_dictionary = graphs_helper.data_by_obs_alias_histo()

    #key = observer, value = data
    dic = {}
    for o in observers:
        dic[o] = [d for d in data if d[3]==o[0]]# slow but short
        print(len(dic[o]),end="\t")
    print("\n")
    print(len(dic))
    
    obs_sorted = [[len(dic[o]),o] for o in dic]
    obs_sorted.sort(reverse=True)# biggest to smallest
    obs_sorted = [i[1] for i in obs_sorted]
    
    #### plot some nice figures

    # plot a histogram of the number of data each observer has

    # those with greater or equal to 2000 datapoints
    x_2000 = [o[1] for o in obs_sorted if len(dic[o])>=2000]
    bins_2000 = len(x_2000)
    heights_2000 = [len(dic[o]) for o in obs_sorted if len(dic[o])>=2000]
    colors_2000 = [(len(dic[o])/13000,0.3,2000/len(dic[o]),1.0) for o in obs_sorted if len(dic[o])>=2000]
    
    # those with x \in [800,2000)
    x_800 = [o[1] for o in obs_sorted if len(dic[o])>=800 and len(dic[o])<2000]
    bins_800 = len(x_800)
    heights_800 = [len(dic[o]) for o in obs_sorted if len(dic[o])>=800 and len(dic[o])<2000]
    colors_800 = [(len(dic[o])/2000,0.3,800/len(dic[o]),1.0) for o in obs_sorted if len(dic[o])>=800 and len(dic[o])<2000]
    
    # those with x \in [300,800)
    x_300 = [o[1] for o in obs_sorted if len(dic[o])>=300 and len(dic[o])<800]
    bins_300 = len(x_300)
    heights_300 = [len(dic[o]) for o in obs_sorted if len(dic[o])>=300 and len(dic[o])<800]
    colors_300 = [(len(dic[o])/1000,0.3,300/len(dic[o]),1.0) for o in obs_sorted if len(dic[o])>=300 and len(dic[o])<800]
    
    # those with x \in [70,300)
    x_70 = [o[1] for o in obs_sorted if len(dic[o])>=70 and len(dic[o])<300]
    bins_70 = len(x_70)
    heights_70 = [len(dic[o]) for o in obs_sorted if len(dic[o])>=70 and len(dic[o])<300]
    colors_70 = [(len(dic[o])/300,0.3,70/len(dic[o]),1.0) for o in obs_sorted if len(dic[o])>=70 and len(dic[o])<300]
    
    # those with x \in [0,70)
    x_0 = [o[1] for o in obs_sorted if len(dic[o])<70]
    bins_0 = len(x_0)
    heights_0 = [len(dic[o]) for o in obs_sorted if len(dic[o])<70]
    colors_0 = [(len(dic[o])/70,0.3,1/(len(dic[o])+1),1.0) for o in obs_sorted if len(dic[o])<70]
    
    
    
    
    plt.figure(figsize=(14,20))
    
    plt.subplot(321)
    plt.bar(x=[i for i in range(bins_2000)],height=heights_2000,align='center',tick_label=x_2000,color=colors_2000)
    plt.xticks(rotation=90)
    plt.title("Number of observations plot range [2000,13000)",color='green')
    
    plt.subplot(322)
    plt.bar(x=[i for i in range(bins_800)],height=heights_800,align='center',tick_label=x_800,color=colors_800)
    plt.xticks(rotation=90)
    plt.title("Number of observations plot range [800,2000)",color='green')
    
    plt.subplot(323)
    plt.bar(x=[i for i in range(bins_300)],height=heights_300,align='center',tick_label=x_300,color=colors_300)
    plt.xticks(rotation=90)
    plt.title("Number of observations plot range [300,800)",color='green')
    
    plt.subplot(324)
    plt.bar(x=[i for i in range(bins_70)],height=heights_70,align='center',tick_label=x_70,color=colors_70)
    plt.xticks(rotation=90)
    plt.title("Number of observations plot range [70,300)",color='green')
    
    plt.subplot(325)
    plt.bar(x=[i for i in range(bins_0)],height=heights_0,align='center',tick_label=x_0,color=colors_0)
    plt.xticks(rotation=90)
    plt.title("Number of observations plot range [0,70)",color="green")
    
    plt.subplot(326)
    fancy_colors = [(random.random(),random.random(),random.random(),1.0) for o in obs_sorted]
    plt.bar(x=[i for i in range(len(dic))],height=[len(dic[o]) for o in obs_sorted],color=fancy_colors)
    plt.title("Number of observations plot",color="green")
    
    #plt.savefig("figures/histogram_number_data.png")
    
    plt.show()

# Takes interval and list of observer aliases and does an event plot to show you when they recorded what data
def event_plot(interval=None,observer_aliases=None,
figsize=(13,13),fontsize=12,gridlines=False,
title=None,save_as=None):
    observers = db_search.select_all_observers()
    data = db_search.select_all_data(the_database='DATA_SILSO_HISTO')
    
    # make list of the observers you will be needing, and exclude extra dates
    if observer_aliases:
        observers = [o for o in observers if o[1] in observer_aliases]
    # just in-case the user put in an alias that doesn't exist
    obs_aliases = [o[1] for o in observers]
    if observer_aliases:
        if len(obs_aliases)<len(observer_aliases):
            for i in set(observer_aliases) - set(obs_aliases):
                print("missing",i)
    # restrict data to only that that is observed by observers
    data = [d for d in data if d[3] in [o[0] for o in observers]]
    data = [d for d in data if d[1]!=None]
    if interval:
        mini=dt.date(int(interval[0][:4]),int(interval[0][5:7]),int(interval[0][8:10]))
        sup=dt.date(int(interval[1][:4]),int(interval[1][5:7]),int(interval[1][8:10]))
        data = [d for d in data if d[1]>=mini and d[1]<=sup]
    else: # if not interval find mini and sup
        mini = min([d[1] for d in data])
        sup = max([d[1] for d in data])

    
    # dictionary : key = observer alias , value = dates observed
    dic = {}
    for o in observers:
        dic[o[1]] = [d[1] for d in data if d[3]==o[0]]# where fk_rubrics == rubrics_id
        if len(dic[o[1]])==0: del dic[o[1]]# don't want empty observers
    aliases = [o for o in dic]
    
    # format the dates, make them decimal form
    dates=[dates_to_decimal([d for d in dic[o]]) for o in dic]

    #print("Aliases\n",aliases)#trace
        
    # plot the eventplot
    # ref : https://matplotlib.org/gallery/lines_bars_and_markers/eventplot_demo.html#sphx-glr-gallery-lines-bars-and-markers-eventplot-demo-py 
    # ref : https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.eventplot.html 
    # ref : https://stackoverflow.com/questions/26402130/matplotlib-string-xticks 
    fig,ax = plt.subplots(figsize=figsize)
    
    colors = [(1,0,0,1),(0,1,0,1),(0,0,1,1),(1,0.7,0,1),(1,0,1,1),(0,1,1,1)]
    colors = colors*(len(dates)//6+1)
    
    plt.eventplot(positions=dates,colors=colors[:len(dates)],linelengths=0.8,linewidths=0.1)
                     
    ax.set_yticks([i for i in range(len(aliases))])
    ax.set_yticklabels(aliases,rotation='horizontal',fontsize=fontsize)
    
    if gridlines: ax.grid()
    #ax.grid(which="both",b=True)
    if title: plt.title(title)
    if save_as: plt.savefig(save_as)
    
    plt.show()

# helper method for stacked_area_plot
# generates dates of all days in specified interval (inclusive)
def days_in(start,end):
    curr = start
    while curr <= end:
        yield curr
        curr += dt.timedelta(days=1)

# Takes interval, and does a stacked area plot witht he observers in that interval
def stacked_area_plot(interval=None,figsize=(18,14),save_as=None,
smoothness=50,observers_list=None,display_others=True,display_legend=True,
plot_title=None): 
    # process the interval if there is one
    if interval:
        low = dt.date(int(interval[0][:4]),int(interval[0][5:7]),int(interval[0][8:10]))
        high = dt.date(int(interval[1][:4]),int(interval[1][5:7]),int(interval[1][8:10]))
    else:
        low = dt.date(1600,1,1)
        high = dt.date(1949,12,31)

    # make an x array with every day of every year in the interval
    x = [d for d in days_in(low,high)]

    # select data in interval, put into dictionary by observer
    data = db_search.select_all_data()
    data = [d for d in data if d[1]!=None]
    data = [d for d in data if d[1]>=low and d[1]<=high]
    observers = db_search.select_all_observers()
    obs_fk_alias_dic = {}
    for o in observers: obs_fk_alias_dic[o[0]]=o[1]
    
    dates_by_obs = {}
    for d in data:
        alias = obs_fk_alias_dic[d[3]]
        try: dates_by_obs[alias].append(d[1])
        except: dates_by_obs[alias] = [d[1]]

    for i in dates_by_obs: dates_by_obs[i].sort()

    # make array of 1s and zeros for each day in the interval for each observer
    binary_obs_dic = {}# key = alias , value = array of 0s and 1s
    for o in dates_by_obs:
        binary_obs_dic[o]=[]
        index = 0
        for dte in x:
            if index<len(dates_by_obs[o]):
                if dte!=dates_by_obs[o][index]: binary_obs_dic[o].append(0)
                else:
                    binary_obs_dic[o].append(1)
                    index +=1
            else: binary_obs_dic[o].append(0)
    
    # make the histogram dictionary 
    # key = number of observations ; value = number of days where this occurs
    n_per_day_hist_dic = {}
    for i in range(len(x)):
        n=0
        for o in binary_obs_dic: n+=binary_obs_dic[o][i]
        try: n_per_day_hist_dic[n]+=1
        except: n_per_day_hist_dic[n] = 1
        

    # make 1s and 0s array smooth with statsmodel lowess filter
    x_decimal = dates_to_decimal(x)
    smoothed_binary_obs_dic = {}
    for o in binary_obs_dic:
        filtered = lowess(binary_obs_dic[o],x_decimal,frac=float(smoothness)/len(x),is_sorted=True,it=0)
        smoothed_binary_obs_dic[o] = filtered[:,1]

    plt.figure(figsize=figsize)

    ### I never got round to doing the histogram above... :'(
    # I can do this in seperate method...

    # plot the historgram
    #plt.subplot(211)

    # plot the area plot
    #plt.subplot(212)
    
    
    
    # if a list of observers if given, group everyone not on that list into one alias - other
    smoothed_binary_obs_array=[]
    others=[]
    labels_array=[]
    if observers_list:
        for o in smoothed_binary_obs_dic:
            if o in observers_list:
                smoothed_binary_obs_array.append(np.array(smoothed_binary_obs_dic[o]))
                labels_array.append(o)
            else:
                others.append(np.array(smoothed_binary_obs_dic[o]))
        if others and display_others==True:
            smoothed_binary_obs_array.append([sum(i) for i in np.transpose(others)])
            labels_array.append("others")
        plt.stackplot(x,smoothed_binary_obs_array,labels=labels_array)
    else:
        smoothed_binary_obs_array = [np.array(smoothed_binary_obs_dic[o]) for o in smoothed_binary_obs_dic]
        plt.stackplot(x,smoothed_binary_obs_array,labels=[o for o in smoothed_binary_obs_dic])
    if display_legend: plt.legend()
    if title: plt.title(plot_title)

    if save_as: plt.savefig(save_as)
    plt.show()

# takes observer - plots histogram frequency vs wolf
# zero is boolean choses wether to include zero into the plot
def frequency_wolf_histogram(observer,interval=None,figsize=(18,14),
save_as=None,option="wolf",zero=True,bins=30,only_blue=False):
    if not option: option="wolf"
    elif option.lower() not in ("wolf","sunspots","groups"):
        print("Error, you did not chose a valid option, it must be in ('wolf','sunspots','groups')")
        return
    option=option.lower()

    # get the observer's data
    data = db_search.select_all_data()
    observers = db_search.select_all_observers()
    fk=None
    for o in observers:
        if o[1]==observer:
            fk=o[0]
            continue
    if not fk: 
        print("\nI'm sorry I don't recognise that observer (it's case sensitive)")
        return
    data_o = [d for d in data if d[3]==fk]
    

    # make the wolf array with the frequencies = weights
    if option=="wolf": x = [d[6] for d in data_o if d[6]!=None]
    elif option=="sunspots": x = [d[5] for d in data_o if d[5]!=None]
    else: x = [d[4] for d in data_o if d[4]!=None]
    max_w = max(x)
    weights = [0]*(max_w+1)
    for w in x: weights[w]+=1

    x_array = [i for i in range(0,max_w+1)]
    if zero==False:
        weights = weights[1:]# take out the zero measurements
        x_array = x_array[1:]

    # plot the histogram
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.hist(x_array, weights=weights, bins=max_w, color='lightblue', alpha=0.9)
    if option!="groups" and not only_blue:ax.hist(x_array, weights=weights, bins =bins, color='salmon', alpha=0.3)# alpha is transparency

    ax.set(title='Histogram Frequency observations '+option, ylabel='frequency',xlabel=option)

    ax.margins(0.05)
    ax.set_ylim(bottom=0)
    if save_as: plt.savefig(save_as)
    plt.show()
    return weights# Temporary - just for testing the poisson best fit...

# plot two histograms comparing the observers' sunspots, group and wolf (1,2,3) for their over-lapping interval
# plot also a smoothed date / frequency plot with both observers (4)
# below (5+6) plot the calibration factor that determines the relative k coefficient
def comparing_two_observers(obs1,obs2,figsize=(10,15),save_as=None,smoothness=100):
    gs00 = mpl.gridspec.GridSpec(3, 2)
    fig = plt.figure(figsize=figsize)
    axs = []
    ### plot the 3 histograms
    # fetch the data from the helper method
    groups_data,sunspots_data,wolf_data = get_hist_data(obs1,obs2)

    ax = fig.add_subplot(gs00[0,0])
    ax.set(title="Histogram Groups",ylabel="frequency groups",xlabel="groups number")
    
    [x_array1,weights1,x_array2,weights2] = groups_data
    ax.hist(x_array1,weights=weights1,bins=len(x_array1),color='lightblue',alpha=0.7,label=obs1)# obs1
    ax.hist(x_array2,weights=weights2,bins=len(x_array2),color='salmon',alpha=0.3,label=obs2)# obs2
    ax.legend()

    ax = fig.add_subplot(gs00[0,1])
    ax.set(title="Histogram Sunspots",ylabel="log freq sunspots",xlabel="sunspots number")

    [x_array1,weights1,x_array2,weights2] = sunspots_data
    ax.hist(x_array1,weights=weights1,bins=len(x_array1),color='lightblue',alpha=0.7,label=obs1)# obs1
    ax.hist(x_array2,weights=weights2,bins=len(x_array2),color='salmon',alpha=0.3,label=obs2)# obs2
    ax.legend()

    ax = fig.add_subplot(gs00[1,0])
    ax.set(title="Histogram Wolf",ylabel="log freq wolf",xlabel="wolf number")

    [x_array1,weights1,x_array2,weights2] = wolf_data
    ax.hist(x_array1,weights=weights1,bins=len(x_array1),color='lightblue',alpha=0.7,label=obs1)# obs1
    ax.hist(x_array2,weights=weights2,bins=len(x_array2),color='salmon',alpha=0.3,label=obs2)# obs2
    ax.legend()

    ### smoothed frequency observation plot
    ax = fig.add_subplot(gs00[1,1])
    ax.set(title="Freq of observation",ylabel="observations / day",xlabel="year")

    # get the data of each of the observers
    fk1,fk2,data,observers = get2observers_data(obs1,obs2)
    if not fk1 or not fk2:
        print("\nI'm sorry I don't recognise one or more of the observers (it's case sensitive)")
        if not fk1: print(obs1)
        if not fk2: print(obs2)
        return
    data_o1,data_o2 = [d for d in data if d[3]==fk1],[d for d in data if d[3]==fk2]
    dates1,dates2 = [d[1] for d in data_o1],[d[1] for d in data_o2]
    dates1.sort()
    dates2.sort()
    low = min(dates1+dates2)
    high = max(dates1+dates2)
    x = [day for day in days_in(low,high)]

    # get frequency array for both observers [0,0,1,1,1,1,0,0,1,...]
    freq1,freq2,index1,index2=[],[],0,0
    for day in x:
        if index1<len(dates1):
            if day!=dates1[index1]: freq1.append(0)
            else: 
                freq1.append(1)
                index1+=1
        else: freq1.append(0)
        if index2<len(dates2):
            if day!=dates2[index2]: freq2.append(0)
            else:
                freq2.append(1)
                index2+=1
        else: freq2.append(0)
    
    # smooth with statsmodel lowess filter
    x_decimal = dates_to_decimal(x)
    filtered1 = lowess(freq1,x_decimal,frac=0.05,is_sorted=True,it=0)
    smoothed1 = filtered1[:,1]
    filtered2 = lowess(freq2,x_decimal,frac=0.05,is_sorted=True,it=0)
    smoothed2 = filtered2[:,1]

    # actully plot it
    ax.plot(x,smoothed1,"b-",label=obs1)
    ax.plot(x,smoothed2,"r-",label=obs2)
    ax.legend()


    ### k factor derivation plot # carrington derivation reloaded
    ax = fig.add_subplot(gs00[2,:])
    ax.set(title=obs1+" vs "+obs2,xlabel=obs1+" sunspots",ylabel=obs2+" sunspots")

    # make array of dates they have in common
    index1,index2,dates_in_common,groups,sunspots,wolfs = 0,0,[],[],[],[]
    for date in x:
        if index1>=len(dates1) or index2>=len(dates2): break
        if date == dates1[index1]:
            index1+=1
            if date == dates2[index2]:
                index2+=1
                dates_in_common.append(date)
        elif date == dates2[index2]:
            index2+=1
        
    # okay this is kindof ineficient but right now that's not important
    groups1,sunspots1,wolfs1,groups2,sunspots2,wolfs2=[],[],[],[],[],[]
    for d in data_o1:
        if d[1] in dates_in_common:
            groups1.append(d[4])
            sunspots1.append(d[5])
            wolfs1.append(d[6])
    for d in data_o2:
        if d[1] in dates_in_common:
            groups2.append(d[4])
            sunspots2.append(d[5])
            wolfs2.append(d[6])
    if len(groups1)!=len(groups2): raise Exception

    for i in range(len(groups1)):
        if groups1[i] !=None and groups2[i] !=None:
            groups.append([groups1[i],groups2[i]])
        if sunspots1[i] != None and sunspots2[i] != None:
            sunspots.append([sunspots1[i],sunspots2[i]])
        if wolfs1[i] != None and wolfs2[i] != None:
            wolfs.append([wolfs1[i],wolfs2[i]])
    groups = np.transpose(groups)
    sunspots = np.transpose(sunspots)
    wolfs = np.transpose(wolfs)

    # for now we will only look at the sunspots number
    # get parameters for line of best fit

    ax.plot(sunspots[0],sunspots[1],"rx")
    
    if save_as:plt.save_fig(save_as)
    plt.show()

# small helper method for the histograms method...
def get2observers_data(obs1,obs2):
    # get the observers' data
    data = db_search.select_all_data()
    observers = db_search.select_all_observers()
    fk1,fk2 = None,None
    for o in observers:
        #print(o[1],end=", ")#trace
        if o[1]==obs1: fk1=o[0]
        elif o[1]==obs2: fk2=o[0]
    return fk1,fk2,data,observers

# helper method for frequency_wolf_histogram, gets the histogram data
def get_hist_data(obs1,obs2):
    # copied from frequency_wolf_histogram
    fk1,fk2,data,observers = get2observers_data(obs1,obs2)
    if not fk1 or not fk2:
        print("\nI'm sorry I don't recognise one or more of the observers (it's case sensitive)")
        if not fk1: print(obs1)
        if not fk2: print(obs2)
        return
    data_o1 = [d for d in data if d[3]==fk1]
    data_o2 = [d for d in data if d[3]==fk2]
    dates1 = [d[1] for d in data if d[1]!=None]
    dates2 = [d[1] for d in data if d[1]!=None]
    inf = max(min(dates1),min(dates2))
    sup = min(max(dates1),max(dates2))
    if inf>sup:
        print("These observers do not over-lap, I cannot compare them with this method")
        return
    # trim the data so that it only has the overlapping period
    data_o1 = [d for d in data_o1 if d[1]<=sup and d[1]>=inf]
    data_o2 = [d for d in data_o2 if d[1]<=sup and d[1]>=inf]

    # groups first - doing them seperately for readability
    xg1 = [d[4] for d in data_o1 if d[4]!=None]
    xg2 = [d[4] for d in data_o2 if d[4]!=None]
    max_w1,max_w2 = max(xg1),max(xg2)
    weights1,weights2 = [0]*(max_w1+1),[0]*(max_w2+1)
    for w in xg1: weights1[w]+=1
    for w in xg2: weights2[w]+=1
    x_array1 = [i for i in range(0,max_w1+1)]
    x_array2 = [i for i in range(0,max_w2+1)]
    groups_data = [x_array1[:],weights1[:],x_array2[:],weights2[:]]

    # sunspots second
    xs1 = [d[5] for d in data_o1 if d[5]!=None]
    xs2 = [d[5] for d in data_o2 if d[5]!=None]
    max_w1,max_w2 = max(xs1),max(xs2)
    weights1,weights2 = [0]*(max_w1+1),[0]*(max_w2+1)
    for w in xs1: weights1[w]+=1
    for w in xs2: weights2[w]+=1
    x_array1 = [i for i in range(0,max_w1+1)]
    x_array2 = [i for i in range(0,max_w2+1)]
    # calculate and plot the log of the frequency otherwise the histogram is kinda useless
    weights1,weights2 = [np.log(w) for w in weights1],[np.log(w) for w in weights2]
    sunspots_data = [x_array1[:],weights1[:],x_array2[:],weights2[:]]

    # wolf third, and last
    xw1 = [d[6] for d in data_o1 if d[6]!=None]
    xw2 = [d[6] for d in data_o2 if d[6]!=None]
    max_w1,max_w2 = max(xw1),max(xw2)
    weights1,weights2 = [0]*(max_w1+1),[0]*(max_w2+1)
    for w in xw1: weights1[w]+=1
    for w in xw2: weights2[w]+=1
    x_array1 = [i for i in range(0,max_w1+1)]
    x_array2 = [i for i in range(0,max_w2+1)]
    # calculate and plot the log of the frequency otherwise the histogram is kinda useless
    weights1,weights2 = [np.log(w) for w in weights1],[np.log(w) for w in weights2]
    wolf_data = [x_array1[:],weights1[:],x_array2[:],weights2[:]]

    return groups_data,sunspots_data,wolf_data


#comparing_two_observers("WOLF - P - M","Wolfer")
#print()


# CARRINGTON
# to help out with the Carrington investigation
def get_full_carrington_dictionaries():
    # get the big dictionary
    obs_alias_dictionary = data_by_obs_alias_good()

    # dictionaries with key=date : value=[groups,sunspots,wolf]
    carrington303_dic = {}
    carrington199_dic = {}

    for i in obs_alias_dictionary["Carrington"]:
        date_string = str(i[1])
        rubrics_number = i[12]
        
        actual_date = i[1]
        groups = i[2]
        sunspots = i[3]
        wolf = i[4]
        
        
        if rubrics_number == 303:
            #if date_string[:4] == "1859" or date_string[:4] == "1860":
            carrington303_dic[actual_date] = [groups,sunspots,wolf]
        elif rubrics_number == 199:
            carrington199_dic[actual_date] = [groups,sunspots,wolf]
    return carrington303_dic,carrington199_dic

# CARRINGTON
# helper for get_carrington_dictionaries_59to60
# originally this was to figure out if there are discrepancies in date
# but now I allowed carrington303 to have data from before 1859 so it's to filter those too
def blacklist_dates(carrington303_dic,carrington199_dic):
    blacklist = []
    for date in carrington199_dic:
        try:
            if carrington303_dic[date]:
                pass
        except:
            #print("199",date,":",carrington199_dic[date],"has no corresponding 303...")#trace
            blacklist.append(date)

    for date in carrington303_dic:
        try:
            if carrington199_dic[date]:
                pass
        except:
            #print("303",date,":",carrington303_dic[date],"has not corresponding 199...")#trace
            blacklist.append(date)
    return blacklist

# CARRINGTON
# makes searchable dictionary for carrington
def get_carringdon_dictionaries_59to60():
    carrington303_dic,carrington199_dic = get_full_carrington_dictionaries()
    blacklist = blacklist_dates(carrington303_dic,carrington199_dic)

    # generate the intersection versions, shorter versions
    new_303_dic = {}
    new_199_dic = {}
    for date in carrington199_dic:
        if date not in blacklist:
            new_303_dic[date] = carrington303_dic[date]
            new_199_dic[date] = carrington199_dic[date]
    return new_303_dic, new_199_dic

# CARRINGTON
# rounds each element in list to nearset int
def round_to_int(wolf):# can be wolf or sunspots
    new_wolf=[]
    for i in wolf:
        new_wolf.append(int(i+0.5))
    return new_wolf

# CARRINGTON
# returns sunspots numbers, for derived carrington
def get_sunspots(groups,wolf):
    sunspots=[]
    if len(groups)!=len(wolf):
        raise Exception
    for i in range(len(groups)):
        # r = 10 g + s
        s = int(wolf[i] -10*groups[i])
        if s<0:
            s=1
        sunspots.append(s)
    return sunspots




