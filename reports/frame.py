# -*- coding: utf-8 -*-
'''
'''
import datetime
import pandas 
import re

class ReportFrame(pandas.core.frame.DataFrame):
    '''A subclassed DataFrame object to handle calculated rows and  
    totals internally. 

    Args:
        :totals: boolean, if the frame has a totals row 
    
    Refs:
        (1) http://stackoverflow.com/questions/2215923/avoid-specifying-all-arguments-in-a-subclass

    '''
    def __init__(self, *args, **kwargs):
        # (1)
        if kwargs.get('totals', False):
            totals = kwargs.pop('totals')
        else:
            totals = False
        super(ReportFrame, self).__init__(*args, **kwargs)
        self._base = self.columns
        self._calculated = {}
        self._has_totals = totals

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

        base = "[\s][+-/*]{1,1}[\s]"
        columns = re.split(base, phrase)    
        operators = re.findall(base, phrase)
        
        assert(len(columns) > len(operators))
        
        for index in range(len(operators)):
            columns.insert(index*2-1, operators[index].strip())
        
        # User must enforce the rules of PEMDAS.
        for index in range(0, len(columns), 2):
            if index == 0:
                if columns[index+1] == '-':
                    self[name] = self[columns[index]] - self[columns[index+2]]
                if columns[index+1] == '+':
                    self[name] = self[columns[index]] + self[columns[index+2]]
                if columns[index+1] == '*':
                    self[name] = self[columns[index]] * self[columns[index+2]]
                if columns[index+1] == '/':
                    self[name] = self[columns[index]] / self[columns[index+2]]
            elif index < len(columns)-1:
                if columns[index+1] == '-':
                    self[name] -= self[columns[index+2]]
                if columns[index+1] == '+':
                    self[name] += self[columns[index+2]]
                if columns[index+1] == '*':
                    self[name] *= self[columns[index+2]]
                if columns[index+1] == '/':
                    self[name] /= self[columns[index+2]]

        self._calculated.update(
            {name:{
                'operators':columns[1::2],
                'columns':columns[::2]}
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
        records = obj[1:len(obj)-1]
    
        if self._has_totals:
            records = records[:-1]

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
                data=self[:-1].append(pandas.DataFrame(store), ignore_index=True),
                totals=True)

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










 


