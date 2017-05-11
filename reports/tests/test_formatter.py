# -*- coding: utf-8 -*-
"""
"""
import pytest

from reports.formatter import FormatFactory

class TestFormatFactory:
    '''Tests for the reports.format.FormatFactory.'''
    @classmethod
    def setup_class(cls):
        '''Set up FormatFactory's'''
        cls.factory = FormatFactory(locale='us')

    @classmethod
    def teardown_class(cls):
        '''Teardown FormatFactory'''
        del cls.factory

    def test_localize_currency_method(cls):
        '''Test currency localization'''
        assert cls.factory.localize_currency() == '$#,##0.00'
        assert cls.factory.localize_currency(locale='gbp') == u'\u00A3'+'#,##0.00'
        assert cls.factory.localize_currency(locale='eu') == u'\u20AC'+'#,##0.00'
        assert cls.factory.localize_currency(locale='jpn') == u'\u00A5'+'#,##0.00'

    def test_create_method(cls):
        '''Test create method'''
        float_numerical = '#,##0.00'
        float_percent = "#0.00%"
        float_currency = '$#,##0.00'

        A = cls.factory.create(value=4.56, column_name='revenue')
        B = cls.factory.create(value=4.56, column_name='numerical')
        C = cls.factory.create(value=4.56, column_name='CTR')

        assert A['num_format'] == float_currency
        assert B['num_format'] == float_numerical
        assert C['num_format'] == float_percent

    def test_representations(cls):
        '''Test representations'''
        assert str(cls.factory) == '{"locale": "us"}'
        assert repr(cls.factory) == ("<[FormatFactory object at "
            "loc = {mem}]>").format(mem=hex(id(cls.factory)))



