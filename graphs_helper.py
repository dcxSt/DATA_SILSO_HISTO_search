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
        # only plot if flag section non-empty so that legend isnt too big
        if len(x[flag_index])>0:
            plt.plot(x[flag_index],ysunspots[flag_index],"x",label="flag = "+str(flag_index),color=cmap(flag_index))
    plt.grid()
    plt.legend()

    plt.subplot(313)
    plt.xlabel("Date")
    plt.xlabel("Groups Number")
    for flag_index in range(len(x)):
        # only plot if flag section non-empty so that legend isnt too big
        if len(x[flag_index])>0:
            plt.plot(x[flag_index],ygroups[flag_index],"x",label="flag = "+str(flag_index),color=cmap(flag_index))
    plt.grid()
    plt.legend()

    plt.show()
















