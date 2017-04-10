# -*- coding: utf-8 -*-
'''
'''
import datetime
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

        # User must enforce the rules of PEMDAS.
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

    def totals(self):
        ''' Sum rows that have numerical values and add the totals as
        the last row of the data set. 

        Args:
            None

        Refs:
            None
        '''
        temp = {}
        store = {}
        calculated = self._calculated
        
        # Convert object to list for easy summations
        obj = []
        obj.extend([self.columns.values])
        obj.extend(self.values)
        headers = obj[0].tolist()
        records = obj[1:]

        for record in records: 
            for index in range(len(record)):
                key = temp.get(index)
                if isinstance(record[index], str):
                    continue
                if isinstance(record[index], datetime.date):
                    continue
                if key:
                    temp[index].append(record[index])     
                else:
                    temp.update({index:[record[index]]})
        
        for index in range(len(headers)):
            name = calculated.get(headers[index])
            if not name:
                result = sum(temp[index]) if temp.get(index) else '-'
            else:
                ops = name.get('operators')
                cols = name.get('columns')
                result = None 
                for index_ in range(len(ops)):
                    col1 = headers.index(cols[index_])
                    col2 = headers.index(cols[index_+1])
                    if result:
                        if ops[index_] == '-':
                            result -= sum(temp[col2])
                        if ops[index_] == '+':
                            result += sum(temp[col2])
                        if ops[index_] == '*':
                            result *= sum(temp[col2])
                        if ops[index_] == '/':
                            result /= sum(temp[col2])
                    else:
                        if ops[index_] == '-': 
                            result = sum(temp[col1]) - sum(temp[col2])
                        if ops[index_] == '+': 
                            result = sum(temp[col1]) - sum(temp[col2])
                        if ops[index_] == '*': 
                            result = sum(temp[col1]) * sum(temp[col2])
                        if ops[index_] == '/': 
                            result = sum(temp[col1]) / sum(temp[col2])

            store[headers[index]] = {0: result}

        return self.__init__(
                self.append(pandas.DataFrame(store), 
                ignore_index=True)
                )
            
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
            name=self.__class__.__name__,
            hex=hex(id(self)))

    def __str__(self):
        return "<[{name} subclassed Pandas obj]>".format(name=self.__class__.__name__)










 


