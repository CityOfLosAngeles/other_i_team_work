from __future__ import division
import pandas as pd
import numpy as np
import sklearn.utils
import datetime as dt
from dateutil.relativedelta import relativedelta
import os
from datetime import datetime, timedelta
from calendar import isleap


def convert_datetime(df):
    datecols = df.dtypes.index[df.dtypes.index.str.contains('DATE')==True].values
    for item in datecols:
        try:
            df[item]= pd.to_datetime(df[item])
        except:
            df[item]=df[item]


def null_counter(df):
    column_name = []
    value_ = []

    for item in df.columns:

        if len(df[df[item].isnull()]) == 0:
            continue

        cols = item
        counts_ = len(df[df[item].isnull()])
        column_name.append(cols)
        value_.append(counts_)

    null_frame = pd.DataFrame({'Column':column_name,
                  'Null Count':value_})
    null_frame['% null']= ((null_frame['Null Count']/len(df))*100).round(decimals=2)

    return null_frame.sort_values(by='Null Count',ascending=False).reset_index(drop=True)

def age_generator(df,start_date,end_date=None,static_date=None):

    """
    Description
    -----------
    Used to calculate the time difference between to DataFrame time objects and reformulate
    by exact "age"

    Parameters
    ----------
    'DF': DataFrame to use,
    'start_date': The column that contains the start date
    'end_date': If your end date is variable and tied to a DF column, use the column name here
    'static_date': To calculate using a standalone date such as file run date or end of the year date


    Returns
    -------
    Object
    """

    def date_as_float(dt_):
        size_of_day = 1. / 366.
        size_of_second = size_of_day / (24. * 60. * 60.)
        days_from_jan1 = dt_ - datetime(dt_.year, 1, 1)
        if not isleap(dt_.year) and days_from_jan1.days >= 31+28:
            days_from_jan1 += timedelta(1)
        return dt_.year + days_from_jan1.days * size_of_day + days_from_jan1.seconds * size_of_second


    if static_date == None and end_date ==None:
        end_fraction = [date_as_float(pd.Timestamp(dt.datetime.now())) for i in range(len(df))]
    elif static_date != None:
        end_fraction = [date_as_float(pd.Timestamp(static_date)) for i in range(len(df))]
    else:
        end_fraction = [date_as_float(df[end_date][i]) for i in range(len(df))]
    start_fraction = [date_as_float(df[start_date][i]) for i in range(len(df))]

    return [end_fraction[i]-start_fraction[i] for i in range(len(df))]


def pivot_column_add(df):
    if 'All' in df.columns.values:
        d = {values+'_category_percent': (df[values]/df['All']) for i,values in enumerate(df.columns)}
        df= pd.merge(df , pd.DataFrame.from_dict(d),left_index=True,right_index=True)
        d2 = {values+'_per_diff_from_whole': (df[values]-df[values]['All']) for i,values in enumerate(df.columns[df.columns.values.tolist().index("All_category_percent")+1:])}
        df = pd.merge(df, pd.DataFrame.from_dict(d2),left_index=True,right_index=True)
        d3 = {values+'_relative_percent': (df[values]/df[values]['All']) for i,values in enumerate(df.columns[0:df.columns.values.tolist().index("All")])}
        df = pd.merge(df, pd.DataFrame.from_dict(d3),left_index=True,right_index=True)
        return df

    print ('Error: Input Pivot Table does not include \'All\' column')

def bin_counter(df,field,min_,max_):
    bin_counts, bin_edges = np.histogram(df[field],
                                          bins=[x for x in range(int((round(df[field].max())+1)))],
                                         range=None, normed=False, weights=None, density=None)

    bin_count = pd.DataFrame({'Count':bin_counts,
                  'Bin Min':bin_edges[:-1],
                 'Bin Max':bin_edges[1:]})

    return "{:.1f}%".format((bin_count[(bin_count['Bin Min']>=min_)&(bin_count['Bin Max']<=max_)])['Count'].sum()/bin_count['Count'].sum()*100)+\
' within '+str(min_)+' and '+str(max_)

def eth_map(df,field_name):
    df.replace(to_replace={field_name:{'Filipino':'Asian_Filipino','Asian':'Asian_Filipino'}},inplace=True)

def folder_setup():
    current_dir = os.getcwd()
    os.chdir('..')
    base_path = os.getcwd()
    data_folder = (os.path.join(base_path,'data'))
    output_folder = (os.path.join(base_path,'outputs'))
    return base_path, data_folder,output_folder

def year_eligible(df,job_length,per_age,years=20,age=50):
    """
    Parameters
    ---------------------
    df : DataFrame
    job_length : field for job length
    per_age : field for age of officer
    years : number of years needed to retire
    age: minimum age needed for retirement

    """


    if (df['GEN_TIER']=='Tier 2' or df['GEN_TIER']=='Tier 4') and df[job_length]>=years:
        return 1
    elif df['GEN_TIER']=='Tier 3' and (df[job_length]>=(years-10)) and df[per_age]>=age:
        return 1

    elif (df['GEN_TIER']=='Tier 5' or df['GEN_TIER']=='Tier 6') and df[job_length]>=years and df[per_age]>=age:
        return 1
    else:
        return 0


def mismatch(df,column1,column2,reference_column):
    """
    Returns a dataframe with the non-matching values of two columns

    Parameters
    ---------------------
    df : DataFrame
    column1: The first column to compare
    column2: The second column to compare
    reference_column: A column such as an index so you can reference discrepancies
    """
    return df[df[column1]!=df[column2]][[reference_column,column1,column2]]

def legacy_recode(df,legacy_field):
    """
    Used to map attrition reasons to PaySr's legacy code

    Parameters
    ---------------------
    df: Dataframe to use
    legacy_field: Field containing Legacy Code
    """
    legacy_map = {9:'Temp Active-Payoffs',
                  10:'Full-Time Supplement State Rate',
                  11:'Full-Time Regular',
                  12:'Full-Time Exempt',
                  19:'Transferred Out',
                  23:'Personal Leave',
                  26:'Military Leave',
                  27:'Workers Compensation',
                  52:'Disability Retirement',
                  54:'Retired',
                  55:'Deceased',
                  56:'Terminated (Voluntary)',
                  57:'Discharged',   #discharged appears to be
                  59:'Probationary Termination',
                  60:'End of Temporary Appointment',
                  61:'Sworn to Civilian'}

    return df[legacy_field].map(legacy_map)

def column_list(df):
    return df.columns.values
