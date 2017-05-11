# -*- coding: utf-8 -*-
"""
"""
import pytest

def pytest_addoption(parser):
    '''Add new command line arguments to pytest parser.

    Ref:
        https://docs.pytest.org/en/latest/example/simple.html
    '''
    parser.addoption(
        "--test_filename", 
        action="store", 
        default="/tmp/pytest_test_write.xlsx",
        help="The complete test write file path.")