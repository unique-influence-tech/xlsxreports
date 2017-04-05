# -*- coding: utf-8 -*-
'''
Utility functions used in library. 
'''
import collections
import elizabeth
import random  
import pandas

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
        else:
            keep_order = collections.OrderedDict()
            keep_order['COS'] = random._cos(_)
            keep_order['Date'] = get.datetime.date(),
            keep_order['IMEI'] = get.code.imei()
            keep_order['Money'] = float(get.business.price().strip('$'))
            keep_order['StackQ'] = get.development.stackoverflow_question()
                     
            store.append(keep_order)
            
    if isinstance(store, dict):
        store = pandas.DataFrame(store)

    return store

def get_totals(self, obj):
    '''Get max char length for each column.'''
    store = {}
    obj_ = obj[1:] # exclude header record 

    for record in obj_: 
        for index in range(len(record)):
            key = store.get(index)
            if isinstance(record[index], str):
                continue
            if isinstance(record[index], datetime.date):
                continue
            if key:
                store[index].append(record[index])     
            else:
                store.update({index:[record[index]]})

    store = {index : sum(store[index]) for index in store}

    return store











