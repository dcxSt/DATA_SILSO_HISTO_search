# methods to help me display some information graphically

# import statements
import db_connection
import db_search
import time
import matplotlib.pyplot as plt
import numpy as np

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

def data_by_obs_alias_histo():
    data = db_search.select_all_data(the_database="DATA_SILSO_HISTO")
    obs_alias_dictionary = {}
    for i in data:
        obs_alias = i[7]

# returns data by observer where each observer has a list of 10 sublists (1/flag)
def get_data_by_obs_seperate_flags():
    data_by_obs = data_by_obs_alias_good()
    data_by_obs_seperate_flags =  {}
    for observer in data_by_obs:
        data_by_obs_seperate_flags[observer]=[[],[],[],[],[],[],[],[],[],[]]
        for i in data_by_obs[observer]:
            flag = i[15]
            
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

# shows figure of some observer's observations seperated by flag
def display_seperate_flags(observer,interval=None,yaxis="Sunspots"):
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
    plt.show()

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








