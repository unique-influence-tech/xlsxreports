# -*- coding: utf-8 -*-
"""
Test Suite for reports.writer.Writer obj

Pytest Usage:
    $ pytest -v -s --test_filename="/tmp/your_test_write_file.xlsx"

Manual Test Usage:
    >>> import reports
    >>> data = reports.frame.ReportFrame(reports.sample_queries.sample_client_1())
    >>> data.totals()
    >>> writer = reports.writer.Writer('filename.xlsx', verbose=True)
    >>> writer.write('sheet', data)
    >>> writer.apply('sheet', 'table 1', feature="conditional formatting", column="impressions", type="3_color_scale")
"""
from .queries import sample_client_1

import os
import pytest
import pandas
import string
import random 

from reports.frame import ReportFrame
from reports.writer import Writer

class TestWriter:
    '''Test the reports.writer.Writer obj.'''

    @classmethod
    def setup_class(cls):
        """ Set up test file and sample data."""
        filename = pytest.config.getoption('--test_filename') # http://stackoverflow.com/questions/13275738
        cls.filename = filename if filename else "/tmp/pytest_test_write.xlsx" 
        cls.writer = Writer(cls.filename)
        cls.write_data = sample_client_1()
        cls.write_data_segments = cls.write_data.objective.unique().tolist()
        cls.write_data_segments.sort()

    @classmethod
    def teardown_class(cls):
        """Delete test excel file."""
        os.remove(cls.filename)

    def test_write_method(cls):
        """ Test Writer.writer method."""
        test_dict = {}

        for segment in cls.write_data_segments:   
            data = cls.write_data[cls.write_data.objective==segment]
            data.reset_index(inplace=True)
            write_me = ReportFrame(data)
            write_me.totals() # create summary row
            test_dict.update({segment:write_me})
            cls.writer.write(segment, write_me)

        try:
            cls.writer.close()
        except FileNotFoundError:
            raise FileNotFoundError("Supply a valid file path "
                "to the --test_filename parameter.")

        compare = pandas.read_excel(
            cls.filename,
            parse_cols="B:"+string.ascii_uppercase[len(write_me.columns)],
            names=write_me.columns.tolist(),
            skiprows=5,
            sheetname=None)
        
        for frame in test_dict:
            assert test_dict[frame].info() == compare[frame].info()
            assert test_dict[frame].shape == compare[frame].shape

    def test_basic_representations(cls):
        '''Test repr() and str() methods'''
        value_1 = ("<[filename = {filename}" 
            " and tabs = {tabs}]>").format(
                tabs=list(cls.writer._workbook.sheetnames.keys()),
                filename=cls.filename)
        value_2 = "<Writer object at {}>".format(hex(id(cls.writer)))
        assert str(cls.writer) == value_1
        assert repr(cls.writer) == value_2
    










