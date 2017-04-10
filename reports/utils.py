# -*- coding: utf-8 -*-
'''
Utility functions used in library. 
'''
import collections
import elizabeth
import random  
import pandas

def get_operator():
    """
    """
    pass

def data(records=50, df=True):
    """Generate random data. This function will produce a pandas.core.Dataframe 
    object or a list of dict objects.

    Args:
        :records: int, number of records to return 
        :df: bool, pandas.core.Dataframe object or list object
    """
    get = elizabeth.Generic('en')

    if df:
        store = {'StackQ': [], 'COS': [], 'IMEI': [], 'Date':[], 'Money': []} 
    else:
        store = []
        
    for _ in range(records):
        if df:
            store['IMEI'].append(get.code.imei())
            store['StackQ'].append(get.development.stackoverflow_question())
            store['COS'].append(random._cos(_))
            store['Date'].append(get.datetime.date())
            store['Money'].append(float(get.business.price().strip('$')))
            
    if isinstance(store, dict):
        store = pandas.DataFrame(store)

    return store











