# -*- coding: utf-8 -*-
"""

"""
import sys 
import pytest
import utils
import writer

class WriterTests:

    def write_method():
        """Tests for the writer.Writer().write()"""
        list_data_1 = utils.data(20)
        list_data_2 = utils.data(35)
        list_data_3 = utils.data(60)
                
        obj = writer.Writer('PyTest.xlsx')

        data_obj =  [
            list_data_1,
            list_data_2,
            list_data_3,
        ]

        for data_set in data_objs:
            obj.write('PyTestTab1', data_set)

        obj.close

        return True

