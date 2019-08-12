# this script is a bit like graphs helper, it contains methods to plot
# things for use in a jupyter notebook. Specifically
# plots and charts that bring into evidence the types of changes I 
# implemented; comparing the original with the new.

# imports
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
import random
import math
import pickle

# helper method for many functions to get data, observers and rubrics from each database
def fetch_all_data():
    data_o = db_search.select_all_data_general(the_database="ORIGINAL_DATA_SILSO_HISTO",table_name="DATA")#o is for original
    observers_o = db_search.select_all_data_general(the_database="ORIGINAL_DATA_SILSO_HISTO",table_name="OBSERVERS")
    rubrics_o = db_search.select_all_data_general(the_database="ORIGINAL_DATA_SILSO_HISTO",table_name="RUBRICS")
    data_h = db_search.select_all_data_general(the_database="DATA_SILSO_HISTO",table_name="DATA")#h is for histo
    observers_h = db_search.select_all_data_general(the_database="DATA_SILSO_HISTO",table_name="OBSERVERS")
    rubrics_h = db_search.select_all_data_general(the_database="DATA_SILSO_HISTO",table_name="RUBRICS")
    data_g = db_search.select_all_data_general(the_database="GOOD_DATA_SILSO",table_name="DATA")#h is for histo
    data_b = db_search.select_all_data_general(the_database="BAD_DATA_SILSO",table_name="DATA")#B IS FOR BAD
    observers_b = db_search.select_all_data_general(the_database="BAD_DATA_SILSO",table_name="OBSERVERS")
    rubrics_b = db_search.select_all_data_general(the_database="BAD_DATA_SILSO",table_name="RUBRICS")
    return data_o,observers_o,rubrics_o,data_h,observers_h,rubrics_h,data_g,data_b,observers_b,rubrics_b

# helper method, identifies id numbers that the databases have in common etc.
def find_overlap():
    data_o,observers_o,rubrics_o,data_h,observers_h,rubrics_h,data_g,data_b,observers_b,rubrics_b = fetch_all_data()
    ids_o,ids_h = [i[0] for i in data_o],[i[0] for i in data_h]
    ids_o.sort()
    ids_h.sort()
    i = 0
    overlap = []# number of data-points they share
    original_only = []
    final_only = []

    # if you have already run this expensive for loop pickled the 
    # result there is no need to do so a second time 
    try:
        f = open("overlap_original_final_ids.pickle","rb")
        [overlap,original_only,final_only] = pickle.load(f)
        f.close()

    except FileNotFoundError:
        for i in range(222000):
            if i in ids_o and i in ids_h:
                overlap.append(i)
            elif i in ids_o:
                original_only.append(i)
            elif i in ids_h:
                final_only.append(i)
        # pickle the 3 lists because it takes ages to run otherwise
        f = open("overlap_original_final_ids.pickle","wb")
        pickle.dump([overlap,original_only,final_only],f)
        f.close()
    
    return overlap,original_only,final_only,data_o,observers_o,data_h,observers_h

# method to plot a pie chart that shows how much data was deleted / input
def pie_charts_1():
    overlap, original_only, final_only,data_o,observers_o,data_h,observers_h = find_overlap()

    # make a dictionary for the two lower pie charts
    # key = observer, value = number of ids deleted / inserted
    deleted_obs_dic,inserted_obs_dic = {},{}
    cursor, mydb = db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    cursor_o, mydb_o = db_connection.database_connector(the_database="ORIGINAL_DATA_SILSO_HISTO")

    for o in observers_h:
        query = "SELECT * FROM DATA WHERE FK_OBSERVERS="+str(o[0])+" AND "
        query += "ID IN "+str(tuple(final_only))
        cursor.execute(query,())
        result = cursor.fetchall()
        if len(result)!=0:
            inserted_obs_dic[o[1]] = len(result)# by alias
    for o in observers_o:
        query = "SELECT * FROM DATA WHERE FK_OBSERVERS="+str(o[0])+" AND "
        query += "ID IN "+str(tuple(original_only))
        cursor_o.execute(query,())
        result = cursor_o.fetchall()
        if len(result)!=0:
            deleted_obs_dic[o[1]] = len(result)# by alias

    db_connection.close_database_connection(mydb_o)
    db_connection.close_database_connection(mydb)

    # plot the 4 pie-charts
    fig = plt.figure(figsize=(14,14)) # create the canvas for plotting

    # first subplot - original database
    plt.subplot(221)
    labels = ["data in both","deleted data"]
    sizes = [len(overlap),len(original_only)]
    colors = ["lightskyblue","lightcoral"]
    explode = (0,0.1)
    plt.title("Original : dtapts="+str(len(overlap)+len(original_only)))

    plt.pie(sizes,explode=explode,labels=labels,colors=colors,
    startangle=90,autopct='%1.1f%%',shadow=True)

    # second subplot - final database
    plt.subplot(222)
    labels = ["data in both","inserted"]
    sizes = [len(overlap),len(final_only)]
    colors = ["lightskyblue","yellowgreen"]
    explode = (0,0.1)
    plt.title("Final : dtapts="+str(len(overlap)+len(final_only)))

    plt.pie(sizes,explode=explode,labels=labels,colors=colors,
    startangle=90,autopct='%1.1f%%',shadow=True)

    # third subplot - deleted
    plt.subplot(223)
    x = [o for o in deleted_obs_dic]
    pcnt = [100*deleted_obs_dic[o]/len(original_only) for o in deleted_obs_dic]
    colors = plt.cm.rainbow(np.array([i-int(i) for i in np.linspace(0,4.13,len(x))]))

    sizes = [deleted_obs_dic[o] for o in deleted_obs_dic]
    plt.title("Deleted - by observer : "+str(len(original_only)))
    
    patches, texts = plt.pie(sizes,colors=colors)
    labels = [x[i]+" "+str(np.round(pcnt[i],3))+"%" for i in range(len(x))]
    plt.legend(patches, labels, loc='left center',bbox_to_anchor=(0.1,1.4),
            fontsize=6)


    # fourth subplot - inserted
    plt.subplot(224)
    x = [o for o in inserted_obs_dic]
    pcnt = [100*inserted_obs_dic[o]/len(final_only) for o in inserted_obs_dic]
    colors = plt.cm.rainbow(np.array([i-int(i) for i in np.linspace(0,2.13,len(x))]))
    sizes = [inserted_obs_dic[i] for i in inserted_obs_dic]
    plt.title("Inserted - by observers : "+str(len(final_only)))

    patches,texts = plt.pie(sizes,colors=colors)
    labels = [x[i]+" "+str(np.round(pcnt[i],3))+"% , n="+inserted_obs_dic[x[i]] for i in range(len(x))]
    plt.legend(patches, labels, loc='left center', bbox_to_anchor=(0.0, 1.),
           fontsize=8)

    #for i in texts: i.set_fontsize(6)

    plt.savefig("pie-charts-1.png")
    plt.show(fig)
    
# method to plot pie chart and bar chart to show how the data was modified
def pie_charts_2():
    cursor,mydb = db_connection.database_connector(the_database="DATA_SILSO_HISTO")
    query = "SELECT * FROM DATA WHERE ID IN (SELECT ID FROM ORIGINAL_DATA_SILSO_HISTO.DATA)"
    cursor.execute(query,())    
    overlap_h = cursor.fetchall()# be careful overlap has differnt meaning than in pie_charts_1
    query = "SELECT * FROM ORIGINAL_DATA_SILSO_HISTO.DATA WHERE ID IN (SELECT ID FROM DATA)"
    cursor.execute(query,())
    overlap_o = cursor.fetchall()
    overlap_h.sort() # probs uncesseary but I want to be sure
    overlap_o.sort()
    if len(overlap_o)!=len(overlap_h): raise Exception
    db_connection.close_database_connection(mydb)

    # find the no data-points and fields that were affected
    # n__f__m == NUMBER (n) of elements in FIELD (f) that were MODIFIED (m)
    ndatem,nfkrubm,nfkobsm,ngroupsm,nsunspotsm,nwolfm,ncommentm,ndateinsertm = 0,0,0,0,0,0,0,0
    same,modified,modified2times = 0,0,0
    for i in range(len(overlap_h)):
        dtpt_h,dtpt_o = overlap_h[i],overlap_o[i]
        date_h,fk_rub_h,fk_obs_h,groups_h,sunspots_h,wolf_h,comment_h,date_insert_h = dtpt_h[1],dtpt_h[2],dtpt_h[3],dtpt_h[4],dtpt_h[5],dtpt_h[6],dtpt_h[8],dtpt_h[9]
        date_o,fk_rub_o,fk_obs_o,groups_o,sunspots_o,wolf_o,comment_o,date_insert_o = dtpt_o[1],dtpt_o[2],dtpt_o[3],dtpt_o[4],dtpt_o[5],dtpt_o[6],dtpt_o[8],dtpt_o[9]
        stayed_same=True
        modified_twice=False
        if date_o != date_h:
            ndatem+=1
            stayed_same=False
        if fk_rub_h != fk_rub_o:
            nfkrubm+=1
            if not stayed_same: modified_twice=True
            stayed_same=False
        if fk_obs_h != fk_obs_o:
            nfkobsm+=1
            if not stayed_same: modified_twice=True
            stayed_same=False
        if groups_h!=groups_o:
            ngroupsm+=1
            if not stayed_same: modified_twice=True
            stayed_same=False
        if sunspots_h!=sunspots_o:
            nsunspotsm+=1
            if not stayed_same: modified_twice=True
            stayed_same=False
        if wolf_h!=wolf_o:
            nwolfm+=1
            if not stayed_same: modified_twice=True
            stayed_same=False
        if comment_h!=comment_o:
            ncommentm+=1
            if not stayed_same: modified_twice=True
            stayed_same=False
        if date_insert_h!=date_insert_o:
            ndateinsertm+=1
            if not stayed_same: modified_twice=True
            stayed_same=False
        if stayed_same: same+=1
        else: modified+=1
        if modified_twice: modified2times+=1
    
    # plot the figure
    fig = plt.figure(figsize=(14,7))

    # plot the piechart
    plt.subplot(121)
    labels = ["exactly the same","modified once","modified more than once"]
    sizes = [same,modified-modified2times,modified2times]
    colors = ["lightskyblue","green","magenta"]
    explode = (0.05,0.05,0.05)
    plt.title("Num Modifications (not including flags)\nDoes not include inserted or deleted data")
    plt.pie(sizes,explode=explode,labels=labels,colors=colors,
    autopct='%1.1f%%',shadow=True,startangle=120)

    # plot the bar chart
    ax = plt.subplot(122)
    plt.title("Modifications made")
    categories = ["Date","Fk_rub","Fk_obs","Grps","Sunspots","Wolf","Comment"]
    y_pos = np.arange(len(categories))
    num_modified = [ndatem,nfkrubm,nfkobsm,ngroupsm,nsunspotsm,nwolfm,ncommentm]
    ax.bar(y_pos,num_modified,align="center",alpha=0.5)
    plt.xticks(y_pos,categories)
    for counter, value in enumerate(num_modified):
        ax.text(counter - 0.25, value + 200, str(value), color='red', fontweight='bold')
    plt.ylabel("number modified")

    plt.savefig("pie-charts-2-modified-database.png")
    plt.show()
    

# method to plot pie chart and bar chart with the different flags
def pie_charts_3():
    data = db_search.select_all_data(the_database="DATA_SILSO_HISTO")
    num_flags_dic = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,0:0}
    for i in data:
        if i[10]==None: num_flags_dic[0]+=1
        else: num_flags_dic[i[10]]+=1

    fig = plt.figure(figsize=(14,7))

    # first subplot - pie chart with flags
    ax = plt.subplot(121)
    
    sizes = [num_flags_dic[1],num_flags_dic[2],num_flags_dic[3],
    num_flags_dic[4],num_flags_dic[5],num_flags_dic[6],num_flags_dic[7],
    num_flags_dic[8],num_flags_dic[9]]
    
    colors = plt.cm.rainbow(np.linspace(0.05,0.95,9))
    #colors = ["lightskyblue"]+[i for i in colors]
    plt.title("Flags pie chart\n(flag=0 is just above 90%)")
    patches, texts,autotexts = plt.pie(sizes,colors=colors,autopct='%1.2f%%',shadow=True)
    labels = ["flag "+str(i)+" n="+str(num_flags_dic[i]) for i in range(1,10)]

    plt.legend(patches,labels,fontsize=10)

    # second subplot - bar chart of flags
    ax = plt.subplot(122)
    plt.title("Flags")
    categories = ["1","2","3","4","5","6","7","8","9"]
    y_pos = np.arange(len(categories))
    num_each = [num_flags_dic[i] for i in num_flags_dic][:-1]
    ax.bar(y_pos,num_each,align="center",alpha=0.5)
    plt.xticks(y_pos,categories)
    for counter, value in enumerate(num_each):
        ax.text(counter - 0.25, value+50, str(value),color='red',fontweight="bold")
    plt.ylabel("number of dtapts flagged")
    plt.xlabel("type of flag")
    
    plt.savefig("pie-charts-3-flags.png")
    plt.show()
    
pie_charts_3()



