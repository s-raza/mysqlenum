#!/usr/bin/python
# 
# Enumerate details of a MySQL database through a form field that is vulnerable to SQL injection 
# Copyright (C) 2019
# Salman Raza <raza.salman@gmail.com>
#
# GNU General Public License v3.0
#
# This program is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>

from Formatting import *


class UserInput():
    
    def __init__(self, target=None):
        
        self.target = target
        self.table = {}
        self.col = {}
        self.long_row = None
        self.invalid_inputs = [""," ","\n","\r","\r\n","\n\r"]
        
    def show_prompts(self):

        self.select_table()
        self.select_col()
        self.select_row_limit()

        return [self.table, self.col]

    def check_prereq(self, reqs = []):
        
        funcs = {func.split('select_')[1]:getattr(self,func) for func in dir(self) if (callable(getattr(self, func))) and func.startswith('select_')}

        return funcs

    def validate_range(self, to_validate, lower, upper):

        if to_validate > lower and to_validate <= upper and to_validate not in self.invalid_inputs:
            return True
        else:
            return False

    def get_input(self, prompt):

        while True:
            input = raw_input(prompt)

            if input not in self.invalid_inputs:
                break
        return input


    def select_table(self):
        '''Prompt for selecting a table to enumerate it's rows'''
        
        print(render_tables(self.target))
        tables = self.target.DB['tables']
        total_tables = len(self.target.DB['tables'])
            
        while True:
            table_index = int(self.get_input("Select Table [{}-{}]: ".format("1",total_tables)))

            if self.validate_range(table_index, 0, total_tables):
                break

        selected_table = list(tables.keys())[int(table_index)-1]
        self.table['selected'] = selected_table
        self.table['num_rows'] = self.target.DB['tables'][selected_table]['row_count']

        return selected_table

    def select_col(self):
        '''Prompt for selecting the column in a table to enumerate it's rows'''

        if self.table.get('selected') is None:
            self.select_table()

        table = self.table['selected']
        cols = self.target.DB['tables'][table]['cols']
        total_cols = len(self.target.DB['tables'][table]['cols'])
        print(render_cols(cols))
        
        while True:
            col_index = int(self.get_input("Select Column to enumerate [{}-{}]: ".format("1",total_cols)))

            if self.validate_range(col_index, 0, total_cols):
                break
                
        selected_col = list(cols.keys())[int(col_index)-1]
        self.col['selected'] = selected_col

        return selected_col

    def select_row_limit(self):
        '''Prompt for selecting the number of rows to enumerate for the selected table.column. Some tables may have thousands of rows. Enumerating limited number of rows is usually enough for most requirements.'''
        
        if self.table.get('selected') is None:
            self.select_table()

        if self.col.get('selected') is None:
            self.select_col()

        selected_table = self.table['selected']
        selected_col = self.col['selected']
        total_rows = int(self.target.DB['tables'][selected_table]['row_count'])
        already_enumerated = len(self.target.get_curr_enum_rows(selected_table, selected_col))
        
        while True:

            selected_limit = self.get_input("Number of rows to enumerate [Total: {}, Enumerated: {}]: ".format(total_rows, already_enumerated))
            
            if selected_limit == '':
                selected_limit = total_rows
            else:
                selected_limit = int(selected_limit)

            if self.validate_range(selected_limit, 0, total_rows):
                break
        
        self.col['limit'] = selected_limit

        return selected_limit

    def select_long_row(self):
        '''Prompt for selecting the long row, to enumerate it's complete contents'''
        
        if self.table.get('selected') is None:
            self.select_table()

        if self.col.get('selected') is None:
            self.select_col()

        table = self.table['selected']
        col = self.col['selected']
        long_row_list = self.target.get_long_rows_for_table_col(table,col)
        print(render_long_rows(self.target.DB['tables'], table, col, long_row_list))
        
        while True:
        
            long_row = int(self.get_input("Select the row to enumerate it's complete contents [{}-{}]: ".format("1",len(long_row_list))))
            
            if self.validate_range(long_row, 0, len(long_row_list)):
                break
                
        long_row = long_row_list[long_row-1]
        self.long_row = long_row
        
        return long_row
