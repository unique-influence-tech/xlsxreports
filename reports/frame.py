# -*- coding: utf-8 -*-
'''
'''
import pandas
import re

class ReportFrame(pandas.core.frame.DataFrame):
    '''
    '''
    def __init__(self, *args, **kwargs):
        super(ReportFrame, self).__init__(*args, **kwargs)
        self._base = self.columns
        self._calculated = {}

    def total(self):
        pass

    def calculate(self, **kwargs):
        """ 
        """
        # args 
        name = kwargs.get('name')
        phrase = kwargs.get('phrase')

        # re stuff
        base = "[a-zA-Z]+ [+-/*]{1,1} [a-zA-Z0-9]*"
        addition = " [+-/*]{1,1} [a-zA-Z0-9]*"
        compyle = re.compile(base)
        match = compyle.match(phrase)
        
        if not match:
            return False
        
        while match.group() != phrase:
            base += addition
            compyle = re.compile(base)
            match = compyle.match(phrase)
        
        parse = match.group().split(' ')

        # The user must enforce the rules of PEMDAS. 
        for index in range(0, len(parse), 2):
            if index == 0:
                if parse[index+1] == '-':
                    self[name] = self[parse[index]] - self[parse[index+2]]
                if parse[index+1] == '+':
                    self[name] = self[parse[index]] + self[parse[index+2]]
                if parse[index+1] == '*':
                    self[name] = self[parse[index]] * self[parse[index+2]]
                if parse[index+1] == '/':
                    self[name] = self[parse[index]] / self[parse[index+2]]
            elif index < len(parse)-1:
                if parse[index+1] == '-':
                    self[name] -= self[parse[index+2]]
                if parse[index+1] == '+':
                    self[name] += self[parse[index+2]]
                if parse[index+1] == '*':
                    self[name] *= self[parse[index+2]]
                if parse[index+1] == '/':
                    self[name] /= self[parse[index+2]]

        self._calculated.update(
            {name:{
                'operators':parse[1::2],
                'columns':parse[::2]}
            })

        return True
            
    # Calculated Properties 
    @property
    def data(self):
        return self._data

    @property
    def base(self):
        return self._base

    @property
    def calculated(self):
        return self._updated









 


