"""
The writer is an object that ... well ... er.. writes. More seriously, it writes
nested structures of data into a table like format in Excel. 

Notes:
    None

TO DOs:
    Tons
"""
import xlsxwriter
import pandas

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
        self._formats = {}
        self._cursors = {}

    def __get_lengths(self, obj):
        """Get max char length for each column.
        
        Args:
            :obj: list, list obj containing list objects 
        """
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

        for item in store:
            max_ = max(store[item])
            # currency float length runs small
            min_ = min(store[item]) if min(store[item]) > 12 else 12
            store[item] = {'min': min_, 'max': max_}

        return store

    def __get_vertices(self, cursor, obj):
        """ Generate table dimensions based on current
        position in sheet.

        Args:
            :obj: pandas dataframe or a list containing objs with
                  obj.__len__ implemented 
        """
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

    # necessary methods
    def write(self, sheet, obj):
        """Writes an individual list or pandas.core.DataFrame object to 
        xlsxwriter.Workbook.sheet object.

        Args:
            :sheet: str, name of sheet
            :obj: list or pandas.core.DataFrame.object, data to be written
        """
        file_ = self._workbook
        format_ = self._formatter

        # transform data into list of lists
        if isinstance(obj, pandas.core.frame.DataFrame):
            data_ = []
            data_.extend([obj.columns.values])
            data_.extend(obj.values)
        elif isinstance(obj, list):
            if isinstance(obj[0], dict):
                data_ = [list(obj[0].keys())]
                for record in obj:
                    data_.append(list(record.values()))
            elif isinstance(obj[0], list):
                data_ = obj
        else:
            raise TypeError("Data is not a DataFrame or list object.")

        # find sheet or create sheet object
        if sheet not in file_.sheetnames:
            file_.add_worksheet(sheet)
            sheet_ = file_.get_worksheet_by_name(sheet)
            kursor = self._cursors[sheet] = Kursor(6, 1)
        else:
            sheet_ = file_.get_worksheet_by_name(sheet)
            kursor = self._cursors.get(sheet)
            if kursor:
                kursor.next_table
            else:
                raise AttributeError('Kursor object doesn\'t exist.')

        # write data to sheet
        lengths = self.__get_lengths(data_)
        vertices = self.__get_vertices(kursor, obj)
        kursor.x = vertices['start_row']
        kursor.y = vertices['start_column']

        for row in range(vertices['rows']):
            kursor.y = vertices['start_column']
            for column in range(vertices['columns']):
                make_pretty = format_.create(
                    value=data_[row][column],
                    max=lengths[column]['max'])
                if row == 0:
                    make_pretty.update(format_._HEAD_)
                elif row > 0 and row < vertices['rows']:
                    make_pretty.update(format_._BODY_)
                else:
                    make_pretty.update(format_._FOOT_)
                make_pretty = file_.add_format(make_pretty)
                sheet_.write(kursor.x, kursor.y, data_[row][column], make_pretty)
                kursor.plus_column
            kursor.plus_row
        kursor.y = vertices['start_column']

        # set column lengths to something decent
        for column in range(kursor.y, kursor.y + vertices['columns']):
            max_ = lengths[column-kursor.y]['max']
            min_ = lengths[column-kursor.y]['min']
            sheet_.set_column(column, column, (max_ + min_)/2)

        return True

    def close(self):
        """Close workbook."""
        print('Closing workbook.')
        return self._workbook.close()

    # representations
    def __repr__(self):
        return '<{name} object at {mem} >'.format(
            name=self.__class__.__name__,
            mem=hex(id(self)),
        )

    def __str__(self):
        return '<[filename = {file}.xlsx and tabs {tabs}]>'.format(
            name=self.__class__.__name__,
            file=self._workbook.filename,
            tabs=self._workbook.sheetnames
        )

    # attributes
    @property
    def cursors(self):
        return getattr(self, '_cursors')


        




