# methods to help me display some information graphically

# import statements
import db_connection
import db_search
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline
from scipy.ndimage.filters import gaussian_filter1d


# method that organises the data from good_database into dictionary searchable by observer alias
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
    

# takes observerS aliasES and database and plots each observer on the same plot
def display_compare_observers(observers,the_database="DATA_SILSO_HISTO",
interval=None,save_as=None,figsize=(12,17)):
    if the_database=="GOOD_DATA_SILSO":
        obs_dic = data_by_obs_alias_good()
        gindex,sindex,windex = 2,3,4
    else:
        obs_dic = data_by_obs_alias_histo(the_database=the_database)
        gindex,sindex,windex = 4,5,6
    
    if interval:
        low = time.strftime(interval[0])
        high = time.strftime(interval[1])

    cmap = plt.get_cmap("tab10")# colors

    # plot the figures
    plt.figure(figsize=figsize)

    plt.subplot(311)
    plt.title("comparing observers groups")
    count=0
    for observer in observers:
        try:
            if interval:
                [x,y] =np.transpose([[i[1],i[gindex]] for i in obs_dic[observer] if time.strftime(str(i[1]))>= low and time.strftime(str(i[1]))<= high and i[gindex]!=None])
            else:
                [x,y] = np.transpose([[i[1],i[gindex]] for i in obs_dic[observer] if i[gindex]!=None])
            plt.plot(x,y,"x",label=observer,color=cmap(count))
        except:
            print("no data for "+observer+" in groups")
            pass
        count+=1
    plt.legend()
    plt.grid()
    plt.xlabel("Date")
    plt.ylabel("Groups")

    plt.subplot(312)
    plt.title("comparing observers sunspots")
    count=0
    for observer in observers:
        try:
            if interval:
                [x,y] = np.transpose([[i[1],i[sindex]] for i in obs_dic[observer] if time.strftime(str(i[1]))>= low and time.strftime(str(i[1]))<= high and i[sindex]!=None])
            else:
                [x,y] = np.transpose([[i[1],i[sindex]] for i in obs_dic[observer] if i[sindex]!=None])
            plt.plot(x,y,"x",label=observer,color=cmap(count))
        except:
            print("no data for "+observer+" in sunspots")#trace
            pass
        count+=1
    plt.legend()
    plt.grid()
    plt.xlabel("Date")
    plt.ylabel("Sunspots")

    plt.subplot(313)
    plt.title("comparing observers wolf")
    count=0
    for observer in observers:
        try:
            if interval:
                [x,y] = np.transpose([[i[1],i[windex]] for i in obs_dic[observer] if time.strftime(str(i[1]))>=low and time.strftime(str(i[1]))<= high and i[windex]!=None])
            else:
                [x,y] = np.transpose([[i[1],i[windex]] for i in obs_dic[observer] if i[windex]!=None])
            plt.plot(x,y,"x",label=observer,color=cmap(count))
        except:
            print("no data for "+observer+" in wolf")#trace
            pass
        count+=1
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Wolf")
    plt.grid()

    if save_as:
        plt.savefig(save_as)
    plt.show()



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


# rounds each element in list to nearset int
def round_to_int(wolf):# can be wolf or sunspots
    new_wolf=[]
    for i in wolf:
        new_wolf.append(int(i+0.5))
    return new_wolf

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








