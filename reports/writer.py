# -*- coding: utf-8 -*-
'''
Provides the `<class 'reports.writer.Writer'>` class, a derivative of xlsxwriter that 
writes nested arrays into tables on multiple tabs keeping track of each position on each
tab for further editing. 
'''
import xlsxwriter
import datetime 
import pandas
import numpy
import pprint
import copy

from reports.kursor import Kursor
from reports.formatter import FormatFactory

class Writer:
    ''' Write pandas.core.frame.DataFrame objects
    to Excel file beyond what is available in the
    xlsxwriter package.

    Args:
        :file_: newly created file name
        :locale: client locale for currency purposes

    Usage:
        >> import Writer
        >> do something

    Refs:
        (1) http://xlsxwriter.readthedocs.io/workbook.html#constructor
        (2) http://xlsxwriter.readthedocs.io/workbook.html#constructor
    '''
    _settings_ = {
        'in_memory':False,
        'constant_memory': False,
        'default_date_format':'yyyy-mm-dd'
    }

    def __init__(self, file_, locale='us', in_mem=True, constant_mem=True):
        if in_mem: # (1)
            self._settings_['in_memory'] = True
        if constant_mem: # (2)
            self._settings_['constant_memory'] = True

        self._workbook = xlsxwriter.Workbook(file_, self._settings_) 
        self._formatter = FormatFactory(locale=locale)
        self._cursors = {}

    # User Methods
    def write(self, sheet, obj):
        '''Writes an individual list or pandas.core.DataFrame object to 
        xlsxwriter.Workbook.sheet object.

        Args:
            :sheet: str, name of sheet
            :obj: list or pandas.core.DataFrame.object, data to be written

        Notes:
             (write.1): Notice data[:-1] passed to .__get_format_map(). This is to avoid
                including the totals row affecting the formatting. By summing values, float
                decimal remainders extend out which causes currency value to be formatted as 
                pure floats (without $)
        '''
        try:
            if not getattr(obj, '_has_totals'):
                raise Warning("There's no totals row in this table.")
        except AttributeError:
            pass

        file_ = self._workbook
        format_ = self._formatter
        data = self.__parse(obj)
        
        if sheet not in file_.sheetnames:
            file_.add_worksheet(sheet)
            sheet_ = file_.get_worksheet_by_name(sheet)
            kursor = self._cursors[sheet] = Kursor(5, 1)
        else:
            sheet_ = file_.get_worksheet_by_name(sheet)
            kursor = self._cursors.get(sheet)
            if kursor:
                kursor.next_table
            else:
                raise AttributeError('Kursor object doesn\'t exist.')

        vertices = self.__get_vertices(kursor, data)
        format_map = self.__get_format_map(kursor, data[:-1]) # (write.1)

        # |---------- WRITE TO SHEET ----------|
        kursor.x = vertices['start_row']
        kursor.y = vertices['start_column']

        for row in range(vertices['rows']):
            kursor.y = vertices['start_column']
            for column in range(vertices['columns']):
                if row == 0:
                    foremat = format_map['HEAD'][column]['format']
                elif row > 0 and row < vertices['rows']-1:
                    foremat = format_map['BODY'][column]['format']
                else:
                    foremat = format_map['FOOT'][column]['format']
                foremat = file_.add_format(foremat)
                sheet_.write(kursor.x, kursor.y, data[row][column], foremat)
                kursor.plus_column
            kursor.plus_row

        kursor.y = vertices['start_column']

        return True

    def close(self):
        '''Close workbook.'''
        print('Closing workbook.')
        return self._workbook.close()

    # Internal Methods
    def __parse(self, obj):
        '''Parse data into list of list.'''
        if isinstance(obj, pandas.core.frame.DataFrame):
            data_ = []
            data_.extend([obj.columns.values])
            data_.extend(obj.values)
        elif isinstance(obj, list):
            if isinstance(obj[0], dict):
                data_ = [list(obj[0].keys())]
                for record in obj:
                    data_.append(list(record.values()))
            elif isinstance(obj[0], list) or isinstance(obj[0], numpy.ndarray):
                data_ = obj
        else:
            raise TypeError("Data is not a DataFrame or list object.")

        return data_

    def __get_format_map(self, cursor, obj):
        ''' Create a format map for head, body and footer.
        
        Args:
            :obj: list, list of lists containing data
            :cursor: kursor.Kursor obj
            :formatter: formatter.FormatFactory obj
        '''
        base = {}
        lengths = self.__get_lengths(obj)
        format_map = {'HEAD':'', 'BODY':'', 'FOOT':''}

        for index in range(len(obj[0])):
            formatter = FormatFactory()
            format_ = formatter.create(
                column_name=obj[0][index],
                value=obj[1][index],
                #max=lengths[index]['max']
                )
            base.update({
                index:{
                    'format':format_, 
                    'column':obj[0][index]
                    }
                })

        for key in format_map:
            clone = copy.deepcopy(base)
            format_map[key] = clone
            for index in range(len(obj[1])):
                format_ = format_map[key][index]['format']
                if key == 'HEAD':
                    format_.update(format_.HEAD)  
                if key == 'BODY':
                    format_.update(format_.BODY)  
                if key == 'FOOT':
                    format_.update(format_.FOOT)

        return format_map
    
    def __get_lengths(self, obj):
        '''Get max char length for each column.'''
        store = {}
        obj_ = obj[1:] # exclude header record 

        for record in obj_: 
            for index in range(len(record)):
                value = str(record[index])
                key = store.get(index)
                if isinstance(record[index], float):
                    value = value.split('.')[1]
                if key:
                    store[index].append(len(value))
                else:
                    store.update({index:[len(value)]})
        else:
            for item in store:
                max_ = max(store[item])
                # currency float length runs small
                min_ = min(store[item])
                store[item] = {'min': min_, 'max': max_}

        return store

    def __get_vertices(self, cursor, obj):
        ''' Generate table dimensions based on current
        position in sheet.

        Args:
            :cursor: kursor.Kursor obj
            :obj: pandas dataframe or a list containing objs with
                  obj.__len__ implemented 
        '''
        x, y = cursor.coordinates

        if isinstance(obj, pandas.core.frame.DataFrame):
            rows, columns = obj.shape
        elif isinstance(obj, list): 
            rows = len(obj)
            columns = set([len(record) for record in obj])
            if len(columns) > 1:
                raise ValueError("Records' column length does not match.")
            else:
                columns = columns.pop()

        return {
            'rows':rows,
            'columns':columns,
            'start_row': x,
            'start_column': y}

    # Representations
    def __repr__(self):
        return '<{name} object at {mem}>'.format(
            name=self.__class__.__name__,
            mem=hex(id(self)),
        )

    def __str__(self):
        return '<[filename = {file}.xlsx and tabs {tabs}]>'.format(
            name=self.__class__.__name__,
            file=self._workbook.filename,
            tabs=self._workbook.sheetnames
        )

    # Attributes
    @property
    def cursors(self):
        return getattr(self, '_cursors')


        




