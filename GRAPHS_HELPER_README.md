# GRAPHS HELPER README

### This readme is bascially the documentation for the methods found in graphs_helper.py

*method that organises the data from good_database into dictionary searchable by observer alias ; key = obs_alias , value = data*

def data_by_obs_alias_good():

*same as above but for different database formatreally slow - avoid using*

def data_by_obs_alias_histo(the_database="DATA_SILSO_HISTO"):

*returns data by observer where each observer has a list of 10 sublists (1/flag)*

def get_data_by_obs_seperate_flags(the_database="GOOD_DATA_SILSO"):

*shows figure of some observer's observations seperated by flag only for GOOD_DATA_SILSO*

def display_seperate_flags(observer,interval=None,yaxis="Sunspots",save_as=None,the_database="GOOD_DATA_SILSO"):

*shows figure with 3 subfigures: groups, sunspots, wolf*

def display_seperate_flags_all(observer,interval=None,the_database="GOOD_DATA_SILSO",save_as=None):

*takes observer alias and g/s/r and plots different databases in different colorsplots nothing if there *

def display_all_databases(observer,interval=None,yaxis="Sunspots",save_as=None,zero_if_null=False):

*takes observerS aliases and database and plots each observer on the same plot.This function has alot of functionality, it's work listing it out.\ninterval = 2d-tuple (date1,date2) with date1<date2\nfigsize size of the figure also 2d-tuple\nonline_sn (boolean) if True plots a smoothed plot of the current sunspot number V2.0 with smoothing factor smoothness\nexclude_these_rubrics is a list of rubrics number you don't want to plot, leave list empty if none*

def display_compare_observers(observers,the_database="DATA_SILSO_HISTO",interval=None,save_as=None,figsize=(12,17),online_sn=False,smoothness=50.0,exclude_these_rubrics=[],include_flags=(None,0,1,2,3,4,5,6,7,8,9)):

*takes date interval and returns x,y arrays of smoothed data to plot from the online sunspots numberthe higher the smoothness, the smoother the plot*

def get_smoothed_sn(interval=(dt.date(1880,1,1),dt.date(1920,1,1)),smoothness=20.0):

*Plots the drift of an observer, uses wolf number V.2.0 as baseline\n- interval takes string tuple of len 2\n- squish_wolf is to squish the scaling factor of wolf number plotted\n- cutoff is a factor that determines where you start cutting off outlier data\nThe slope displayed is indicative of drift*

def display_wolf_drift(observer,the_database="DATA_SILSO_HISTO",interval=None,save_as=None,figsize=(15,11),squish_wolf=0.005,cutoff=4):

*converts an array of dates into an array of floats that represent dates*

def dates_to_decimal(dates):

*converts an array of decimal_dates to array of dates*

def decimal_to_dates(dates):

*line of best fit 2 unknowns functionit's a helper function for those that are using scipy.optimize.curve_fit for a line of best fit*

def line(x,a,b):

*method to identify observers in DATA_SILSO_HISTO.OBSERVERS and how much data is associated with each one*

def size_data_by_observer_hist():

*Takes interval and list of observer aliases and does an event plot to show you when they recorded what data*

def event_plot(interval=None,observer_aliases=None,figsize=(13,13),fontsize=12,gridlines=False,title=None,save_as=None):

*helper method for stacked_area_plotgenerates dates of all days in specified interval (inclusive)*

def days_in(start,end):

*Takes interval, and does a stacked area plot witht he observers in that interval*

def stacked_area_plot(interval=None,figsize=(18,14),save_as=None,smoothness=50,observers_list=None,display_others=True,display_legend=True,plot_title=None): 

*takes observer - plots histogram frequency vs wolfzero is boolean choses wether to include zero into the plotdata interval is tuple with 2 integerssup_freq is a positive integer*

def frequency_wolf_histogram(observer,interval=None,figsize=(18,14),save_as=None,option="wolf",zero=True,binwidth=5,only_blue=False,sup_freq=None,data_interval=None):

*plot two histograms comparing the observers' sunspots, group and wolf (1,2,3) for their over-lapping intervalplot also a smoothed date / frequency plot with both observers (4)below (5+6) plot the calibration factor that determines the relative k coefficient*

def comparing_two_observers(obs1,obs2,figsize=(10,15),save_as=None,smoothness=100):

*small helper method for the histograms method...*

def get2observers_data(obs1,obs2):

*helper method for frequency_wolf_histogram, gets the histogram data*

def get_hist_data(obs1,obs2):

*CARRINGTONto help out with the Carrington investigation*

def get_full_carrington_dictionaries():

*CARRINGTONhelper for get_carrington_dictionaries_59to60originally this was to figure out if there are discrepancies in datebut now I allowed carrington303 to have data from before 1859 so it's to filter those too*

def blacklist_dates(carrington303_dic,carrington199_dic):

*CARRINGTONmakes searchable dictionary for carrington*

def get_carringdon_dictionaries_59to60():

*CARRINGTONrounds each element in list to nearset int*

def round_to_int(wolf):# can be wolf or sunspots

*CARRINGTONreturns sunspots numbers, for derived carrington*

def get_sunspots(groups,wolf):

