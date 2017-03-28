"""

To Dos:
    Write pytests for the writer object.

"""
import sys 
import pytest
import utils
import writer

def test_write_method():
    """Tests for the writer.Writer().write()"""
    list_data_1 = utils.data(50)
    list_data_2 = utils.data(100)
    list_data_3 = utils.data(150)
    
    dataframe_data_1 = utils.data(50, True)
    dataframe_data_2 = utils.data(100, True)
    dataframe_data_3 = utils.data(150, True)
    
    obj = writer.Writer('pytest.xlsx')

    data_obj =  [
        list_data_1,
        list_data_2,
        list_data_3,
        dataframe_data_1,
        dataframe_data_2,
        dataframe_data_3
    ]

    for data_set in in data_objs:
        obj.write('PyTestTab1', data_set)

    obj.close

    return True

def raise_system_exit():
    raise SystemExit(1)

def get_grid():
    pass

def test_mytest():
    with pytest.raises(SystemExit):
        raise_system_exit()
