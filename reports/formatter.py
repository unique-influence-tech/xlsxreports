# -*- coding: utf-8 -*-
'''
Provides the `<class 'reports.formatter.FormatFactory'>` class, a class that generates format
objects. 
'''
import datetime
import json

class FormatFactory(dict):
    '''A collections object containing xlsx formatting.

    Args:
        None

    Refs:
        (1) Note necessary because of 
            http://xlsxwriter.readthedocs.io/workbook.html#constructor
            
    Usage:
        >> import FormatFactory
        >> format = FormatFactory(locale='us')
  
    '''
    _currency_ = ['value','revenue', 'spend', 'cost', '$']
    _percentage_ = ['tr', 'vr', 'rate', 'ratio', 'yield', "%"]

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.HEAD = {'bold': True,'font_size':'13', 'bottom':1}
        self.BODY = {'font_size':'11'}
        self.FOOT = {'bold': True,'font_size':'13','top':1}
        
    @classmethod
    def localize_currency(cls, locale='us'):
        '''Simple currency formatting.

        Args:
            :locale: str, abbreviated country name
        '''
        if locale == 'us':
            return '$#,##0.00'
        if locale == 'eu':
            return u'\u20AC'+'#,##0.00'
        if locale == 'gbp':
            return u'\u00A3'+'#,##0.00'
        if locale == 'jpn':
            return u'\u00A5'+'#,##0.00'

    @classmethod
    def find_float_format(cls, string):
        '''Float formats require context. See the class
        properties _currency_ and _percentage_. 
        '''
        for item in cls._currency_:
            lower = item.lower()
            upper = item.upper()
            proper = item.title()

            if lower in string or upper in string or proper in string:
                currency = cls.localize_currency()
                return cls(num_format=currency)

        for item in cls._percentage_:
            lower = item.lower()
            upper = item.upper()
            proper = item.title()

            if lower in string or upper in string or proper in string:
                return cls(num_format="#0.00%")
        
        return cls(num_format='#,##0.00')
                
    @classmethod
    def create(cls, **kwargs):
        '''Generate a formatting dictionary.

        Args:
            :value: str/float/int/datetime.date, various values 
            :max: int, max length of similar value in column
        '''
        value = kwargs.get('value')
        column = kwargs.get('column_name')

        if isinstance(value, str):
            return cls(font_size='12')

        if isinstance(value, int):
            return cls(num_format='#,##0')

        if isinstance(value, float):
            return cls.find_float_format(column) # floats can be currency or dollars

        if isinstance(value, datetime.date): # (1)
            return cls(num_format='yyyy-mm-dd')

    # Representations
    def __repr__(self):
        return '<[{name} object at loc = {mem}]>'.format(
            name=self.__class__.__name__,
            mem=hex(id(self)))

    def __str__(self):         
        return json.dumps(self)
    

    
        
        



    
        





