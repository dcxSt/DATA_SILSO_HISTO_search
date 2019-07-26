# this script is a bit like graphs helper, it contains methods to plot
# things for use in a jupyter notebook. Specifically
# plots and charts that bring into evidence the types of changes I 
# implemented; comparing the original with the new.

# imports
import db_connection
import db_search
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import time
import scipy
from scipy.interpolate import spline
from scipy.ndimage.filters import gaussian_filter1d
import random
import math

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

# method to generate a pie chart that shows how much data was modified
def compare_pie_modify():
    data_o,observers_o,rubrics_o,data_h,observers_h,rubrics_h,data_g,data_b,observers_b,rubrics_b = fetch_all_data()
    ids_o,ids_h = [i[0] for i in data_o],[i[0] for i in data_h]
    created = len(set(ids_h) - set(ids_o))
    destroyed = len(set(ids_o) - set(ids_h))
    changed_observer_ids = []
    changed_rubrics_ids = []
    changed_data_ids = []
    


