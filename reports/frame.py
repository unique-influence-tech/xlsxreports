# -*- coding: utf-8 -*-
'''
'''
import pandas
import re

class ReportFrame(pandas.core.frame.DataFrame):
    '''A subclassed DataFrame object to handle calculated rows and  
    totals internally. 
    '''
    def __init__(self, *args, **kwargs):
        super(ReportFrame, self).__init__(*args, **kwargs)
        self._base = self.columns
        self._calculated = {}

    def totals(self):
        ''''''
        pass

    def calculate(self, **kwargs):
        """Add a calculated field to DataFrame. Keep track of 
        its operators and the columns used to calculate. 

        Args:
            :name: str, name of new column
            :phrase: str, simple phrase (e.g. "clicks / impressions", "spend / clicks")

        Refs:
            None
        """
        name = kwargs.get('name')
        phrase = kwargs.get('phrase')
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
            
    # Attributes 
    @property
    def base(self):
        return self._base

    @property
    def calculated(self):
        return self._calculated

    # Representations
    def __repr__(self):
        return "<[{name} obj at {hex}]>".format(
            name=self.__class__.name,
            hex=hex(id(self)))

    def __str__(self):
        return "<[{name} subclassed Pandas obj]>".format(name=self.__class__.name)










 


