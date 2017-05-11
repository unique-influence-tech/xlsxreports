# -*- coding: utf-8 -*-
'''
Provides the `<class 'reports.writer.Writer'>` class, a derivative of xlsxwriter that 
writes nested arrays into tables on multiple tabs keeping track of each position on each
tab for further editing. 
'''
import xlsxwriter
import datetime 
import pandas
import string
import numpy
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

    def __init__(
        self, 
        file_, 
        locale='us', 
        in_mem=True, 
        constant_mem=True, 
        verbose=False):

        if in_mem: # (1)
            self._settings_['in_memory'] = True
        if constant_mem: # (2)
            self._settings_['constant_memory'] = True

        self._workbook = xlsxwriter.Workbook(file_, self._settings_) 
        
        # settings
        self._formatter = FormatFactory(locale=locale)
        self._verbose = verbose 

        # caching 
        self._cursors = {} # cursor caching 
        self._maps_cache = {} # table map caching

    # User Methods
    def write(self, sheet, data_):
        '''Writes an individual list or pandas.core.DataFrame object to 
        xlsxwriter.Workbook.sheet object.

        Args:
            :sheet: str, name of sheet
            :obj: list or pandas.core.DataFrame.object, data to be written

        Notes:
            (write.1): 
                Notice data[:-1] passed to .__build_format(). This is to avoid
                including the totals row affecting the formatting. By summing values, float
                decimal remainders extend out which causes currency value to be formatted as 
                pure floats (without $)

        Usage:
            >> import reports
            >> report = reports.writer.Writer("file.xlsx")
            >> report.write('sheet 1', data) # table 1 written
            >> report.write('sheet 1', data) # table 2 written 

        Refs:
            None
        '''
        try:
            if not getattr(data_, '_has_totals'):
                raise Warning("There's no totals row in this table.")
        except AttributeError:
            pass

        file_ = self._workbook
        format_ = self._formatter
        data = self.__parse(data_)
        
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

        table_specs = self.__get_table_info(kursor, data)
        format_map = self.__build_format(kursor, data[:-1]) # (write.1)

        # Write Process
        kursor.x = table_specs['start_row']
        kursor.y = table_specs['start_column']

        for row in range(table_specs['rows']):
            kursor.y = table_specs['start_column']
            for column in range(table_specs['columns']):
                if row == 0:
                    foremat = format_map['HEAD'][column]['format']
                elif row > 0 and row < table_specs['rows']-1:
                    foremat = format_map['BODY'][column]['format']
                else:
                    foremat = format_map['FOOT'][column]['format']
                foremat = file_.add_format(foremat)
                sheet_.write(kursor.x, kursor.y, data[row][column], foremat)
                kursor.plus_column
            kursor.plus_row

        kursor.y = table_specs['start_column']

        self.__cache_map(sheet, table_specs) # cache table map

        if self._verbose:
            return "table {num} has been written to {sheet}".format(
                num=len(self._maps_cache[sheet]),
                sheet=sheet)

    def apply(self, sheet, table, **options):
        '''Apply features to the current workbook.

        Args:
            :sheet: str, sheetname you're trying to access
            :table: str, _maps_cache table w.r.t. sheet --> 'table_1', 'table_2'
            :options: define feature and required fields for feature

        Usage:
            >> Writer.apply(
                'sheet 1', 
                'table 1', 
                feature='conditional formatting',
                column='impressions'
                type='data_bar',
                bar_color='green')
            >> Writer.apply(
                'sheet 1', 
                'table 2', 
                feature='conditional formatting',
                column='impressions'
                type='3_color_scale')

        Refs:
            None
        '''
        file_ = self._workbook
        sheet_ = file_.get_worksheet_by_name(sheet)
        table_info = self._maps_cache[sheet][table]
        upper = list(string.ascii_uppercase[1:]) # start at COLUMN B 

        if options.get('feature') == 'conditional formatting':
            cf_format = options.get('type')
            column = options.get('column')
            header = table_info['headers'].index(column)
            style = {'type': cf_format}
            if cf_format == 'data_bar':
                bar_color = options.get('bar_color')
                if not bar_color:
                    raise ValueError("You need to supply a data bar color.")
                style.update({'bar_color':bar_color})
            if options.get('field_type') == 'percent':
                style.update({'min_type':'percent', 'max_type':'percent'})
            selector = '{startcol}{startrow}:{endcol}{endrow}'.format(
                startcol=upper[header],
                startrow=table_info['start_row'] + 1,
                endcol=upper[header],
                endrow=table_info['stop_row'] - 1)
            sheet_.conditional_format(selector, style)
        
        # TODO: More features

        if self._verbose:
            return "{feature} has been applied to table {num} on {sheet}".format(
                feature=options.get('feature'),
                num=len(self._maps_cache[sheet]),
                sheet=sheet)

    def close(self):
        '''Close workbook.'''
        print('Closing workbook.')
        return self._workbook.close()

    # Internal Methods
    def __parse(self, obj):
        '''Parse DataFrame object into list of lists.'''
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

    def __build_format(self, cursor, obj):
        ''' Create a format map for head, body and footer.'''
        base = {}
        format_map = {'HEAD':'', 'BODY':'', 'FOOT':''}

        for index in range(len(obj[0])):
            formatter = FormatFactory()
            format_ = formatter.create(
                column_name=obj[0][index],
                value=obj[1][index],
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
    
    def __get_table_info(self, cursor, obj):
        '''Generate table information.'''
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
            'headers': list(obj[0]),
            'rows': rows,
            'columns': columns,
            'start_row': x,
            'start_column': y,
            'stop_row': x + len(obj),
            'stop_column': y + len(obj[0]),
        }

    def __cache_map(self, sheet, map_):
        '''Cache table map.'''
        specs = self._maps_cache.get(sheet)

        if not specs:
            self._maps_cache[sheet] = dict()
            self._maps_cache[sheet]['table 1'] = map_
        else:
            table = 'table {num}'.format(num=len(specs)+1)
            self._maps_cache[sheet][table] = map_

    # Representations
    def __repr__(self):
        return '<{name} object at {mem}>'.format(
            name=self.__class__.__name__,
            mem=hex(id(self)),
        )

    def __str__(self):
        return '<[filename = {file} and tabs = {tabs}]>'.format(
            name=self.__class__.__name__,
            file=self._workbook.filename,
            tabs=list(self._workbook.sheetnames.keys())
        )

    # Attributes
    @property
    def cursors(self):
        return getattr(self, '_cursors')

