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

def select_long_row(target, table, col, long_row_list):
    '''Prompt for selecting the long row, to enumerate it's complete contents'''
    
    print(render_long_rows(target.DB['tables'], table,col, long_row_list))
    
    while True:
    
        long_row = int(input("Select the row to enumerate it's complete contents [{}-{}]: ".format("1",len(long_row_list))))
        
        if long_row > 0 and long_row <= len(long_row_list):
        
            break
            
    long_row = long_row_list[long_row-1]
    
    return long_row

def select_row_limit(target, selected_table, selected_col):
    '''Prompt for selecting the number of rows to enumerate for the selected table.column. Some tables may have thousands of rows. Enumerating limited number of rows is usually enough for most requirements.'''
    
    total_rows = int(target.DB['tables'][selected_table]['row_count'])
    already_enumerated = len(target.get_curr_enum_rows(selected_table, selected_col))
    
    while True:
    
        selected_limit = input("Number of rows to enumerate [Total: {}, Enumerated: {}]: ".format(total_rows, already_enumerated))
        
        if selected_limit == '':
            
            selected_limit = total_rows
            
        else:
            
            selected_limit = int(selected_limit)
        
        if selected_limit > 0 and selected_limit <= total_rows:
        
            break
            
    return selected_limit

def select_col(target, selected_table):
    '''Prompt for selecting the column in a table to enumerate it's rows'''
    
    cols = target.DB['tables'][selected_table]['cols']
    
    total_cols = len(target.DB['tables'][selected_table]['cols'])
    
    print(render_cols(cols))
    
    while True:
    
        col_index = int(input("Select Column to enumerate [{}-{}]: ".format("1",total_cols)))
        
        if col_index > 0 and col_index <= total_cols:
        
            break
            
    selected_col = list(cols.keys())[int(col_index)-1]
    
    return selected_col
    
def select_table(target):
    '''Prompt for selecting a table to enumerate it's rows'''
    
    print(render_tables(target))
        
    tables = target.DB['tables']
    
    total_tables = len(target.DB['tables'])
        
    while True:
    
        table_index = int(input("Select Table [{}-{}]: ".format("1",total_tables)))
        
        if table_index > 0 and table_index <=  total_tables:
        
            break
    
    selected_table = list(tables.keys())[int(table_index)-1]
    
    return selected_table