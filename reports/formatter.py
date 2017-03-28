"""
    A factory to generate a dictionary with proper format for each value.

Notes:
    The localize_currency method is not completely thought out for use with the writer. 

     
"""
import datetime

class FormatFactory(dict):
    """A factory to create dictionaries with specific
    formatting. 
    
    Args:
        None

    Refs:

        (1) Note necessary because of 
            http://xlsxwriter.readthedocs.io/workbook.html#constructor

    Notes:
        (!) Currency floats will be floats with 2 digits after decimal point. All other floats
            will not have EXACTLY 2 digits after decimal point.

    """
    _HEAD_ = {
        'bold': True,
        'font_size':'13',
        'bottom':1}

    _BODY_ = {
        'font_size':'11'}

    _FOOT_ = {
        'font_size':'13',
        'bold': True,
        'top':1}

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
    
    @classmethod
    def localize_currency(cls, locale='us'):
        """Simple currency formatting."""
        if locale == 'us':
            return '$#,##0.00'
        if locale == 'eu':
            return u'\u20AC'+'#,##0.00'
        if locale == 'gbp':
            return u'\u00A3'+'#,##0.00'
        if locale == 'jpn':
            return u'\u00A5'+'#,##0.00'

    @classmethod
    def create(cls, **kwargs):
        """Create proper formatting."""
        
        value = kwargs.get('value')
        max_len = kwargs.get('max')
        vertices = kwargs.get('vertices')

        if isinstance(value, str):
            return cls(font_size='12')

        if isinstance(value, int):
            return cls(num_format='#,##0')

        # TO Dos: smart parser for currency and normal floats
        if isinstance(value, float):
            str_ = str(value).rsplit('.')
            currency = cls.localize_currency()
            if len(str_[1]) < 3 and float(str_[1]) != 0: # (!)
                return cls(num_format=currency)
            elif float(str_[1]) == 0:
                    if max_len < 3:
                        currency = currency.replace('#,##0.00', '#,##0')
                        return cls(num_format=currency)
            return cls(num_format='#,##0.00')

        if isinstance(value, datetime.date): # (1)
            return cls(num_format='yyyy-mm-dd')



    
        





