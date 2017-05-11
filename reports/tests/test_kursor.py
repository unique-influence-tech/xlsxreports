# -*- coding: utf-8 -*-
"""
"""
import pytest
import random

from reports.kursor import Kursor

class TestKursor:
    """Tests for the reports.kursor.Kursor object."""

    @classmethod
    def setup_class(cls):
        '''Create 3 arbitrary kursors'''
        cls.kursorA = Kursor(1, 50)
        cls.kursorB = Kursor(50, 1)
        cls.kursorC = Kursor(25, 25)

    @classmethod
    def teardown_class(cls):
        '''Delete Kursor'''
        del cls.kursorA
        del cls.kursorB
        del cls.kursorC

    def test_kursor_properties(cls):
        '''Test Kursor properties'''
        assert cls.kursorA.position == '[AX1]'
        assert cls.kursorB.position == '[A50]'
        assert cls.kursorC.position == '[Y25]'
        assert cls.kursorA.coordinates == (1, 50)
        assert cls.kursorB.coordinates == (50, 1)
        assert cls.kursorC.coordinates == (25, 25)

    def test_kursor_representations(cls):
        '''Test Kursor object representations'''
        assert str(cls.kursorA) == "<Kursor object x=1 y=50>"
        assert str(cls.kursorB) == "<Kursor object x=50 y=1>"
        assert str(cls.kursorC) == "<Kursor object x=25 y=25>"
        assert repr(cls.kursorA) == ("<[Kursor object (x=1 y=50) "
            "at hex mem loc = {mem}]>").format(mem=hex(id(cls.kursorA)))
        assert repr(cls.kursorB) == ("<[Kursor object (x=50 y=1) "
            "at hex mem loc = {mem}]>").format(mem=hex(id(cls.kursorB)))
        assert repr(cls.kursorC) == ("<[Kursor object (x=25 y=25) "
            "at hex mem loc = {mem}]>").format(mem=hex(id(cls.kursorC)))
