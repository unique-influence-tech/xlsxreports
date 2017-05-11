# -*- coding: utf-8 -*-
'''
Provides the `<class 'reports.kursor.Kursor'>` class, a simple cursor object to keep
position on each Excel Workbook tab. 
'''
import string 

class Kursor:
    """2D vector-like object to keep track of position
    in Excel files.

    Args:
        :x: int, start position of row in x-y plane
        :y: int, start position of column in x-y plane
    
    Refs:
        None

    Usage:
        >> import Kursor
        >> kursor = Kursor(1,1)
        >> kursor.position 
        '[A1]'
        >> kursor.coordinates
        (1,1)
        >> kursor.plus_row
        >> kursor.position
        '[A2]'
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Internal Methods
    def __get_xlsx_position(self):
        """Return user friendly Excel sheet position."""
        num = 0
        list_ = list(string.ascii_uppercase)
        list_.insert(0, "")

        for char1 in list_:
            for char2 in list_[1:]:
                num += 1
                string_ = '[{col}{row}]'.format(
                    col=char1+char2,
                    row=str(self.x)
                    )
                if num == self.y:
                    return string_

    # Representations
    def __str__(self):
        return "<{name} object x={x} y={y}>".format(
            name=self.__class__.__name__,
            x=self.x,
            y=self.y
        )

    def __repr__(self):
        return "<[{name} object (x={x} y={y}) at hex mem loc = {mem}]>".format(
            name=self.__class__.__name__,
            x=self.x,
            y=self.y,
            mem=hex(id(self))
        )

    # Properties
    @property
    def coordinates(self):
        return (self.x, self.y)

    @property
    def position(self):
        return self.__get_xlsx_position()

    # kursor movement properties
    @property
    def next_table(self):
        self.x += 3

    @property
    def plus_row(self):
        self.x += 1

    @property
    def plus_column(self):
        self.y += 1

        









    











