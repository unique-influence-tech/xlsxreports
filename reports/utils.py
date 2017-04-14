# -*- coding: utf-8 -*-
'''
'''
import elizabeth
import random  
import pandas


def get_dummy_data_set(records=50):
    """ Generate a dummy data set that includes string, int, and float
    data types. This returns a pandas.core.data.DataFram object.

    Args:
        :records: int, number of records to return 
        :df: bool, pandas.core.Dataframe object or list object

    Refs:
        None
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











