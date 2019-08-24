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

from prettytable import PrettyTable
from Tools.ScreenColors import clr
from textwrap import wrap

WRAP_WIDTH = 75

def get_wrapped(row_obj, txt):
    
    pass



def print_db_info(db, format=None):
    '''Print the DB information to the screen in a tabular format.'''
    
    if format == "table":
    
        info = PrettyTable(["{}: {}".format(clr.red("DB Name"),clr.white(db['info']['dbname'])),
                            "{}: {}".format(clr.red("DB User"),clr.white(db['info']['username'])),
                            "{}: {}".format(clr.red("DB Version"),clr.white(db['info']['version'])),
                            "{}: {}".format(clr.red("Tables"),clr.white(db['info']['table_count']))
                            ])
                            
        print(info)
        
    else:
        print(("\n{db}: {db_info}\t{user}: {user_info}\t{version}: {version_info}\t{tables}: {tables_info}\n") \
        .format(db=clr.red("DB Name"), db_info=clr.white(db['info']['dbname']),
        user=clr.red("DB User"), user_info=clr.white(db['info']['username']),
        version=clr.red("DB Version"), version_info=clr.white(db['info']['version']),
        tables=clr.red("Tables"), tables_info=clr.white(db['info']['table_count'])))

def remove_rn(txt):
    
    return txt.replace('\r',' ').replace('\n',' ')

def render_cols(table):

    cols = PrettyTable(["No.","Columns"])
          
    cols.align = "l"
    
    i = 0
    
    for col,_ in table.items():
    
        i = i+1
        
        cols.add_row([clr.red(str(i)),clr.yellow(col)])
    
    return cols

def render_rows(col,col_name):

    rows = PrettyTable(["No.",col_name])
          
    rows.align = "l"
    
    i = 0
    
    for row in col:
    
        i = i+1

        if len(row) > WRAP_WIDTH:
            
            lines = wrap(row, WRAP_WIDTH)

            rows.add_row([clr.red(str(i)),remove_rn(lines[0])])

            for line in lines[1:]:
                
                rows.add_row(['',remove_rn(line)])
        else:

            rows.add_row([clr.red(str(i)),remove_rn(row)])

    
    return rows

def render_long_rows(tables, table, col, long_row_list):
    
    long_rows = PrettyTable(["No.","Content","Actual Length","Row Index"])

    long_rows.align = "l"

    for num,i in enumerate(long_row_list):
        
        content = tables[table]['cols'][col][i][1]

        actual_length = tables[table]['cols'][col][i][0]
        
        # long_rows.add_row([num+1, wrap(content, WRAP_WIDTH)[0], actual_length, i])
        long_rows.add_row([num+1, remove_rn(content), actual_length, i])

    return long_rows

def render_tables(target):
    
    tables = PrettyTable(["No.","Tables"])
    
    tables.align = "l"
    
    i = 0
    
    for table,_ in target.DB['tables'].items():
        
        i = i+1
        
        tables.add_row([clr.red(str(i)),clr.yellow(table)])
        
    return tables

def print_table_info(db, format=None):
    '''Print the table information to the screen in a tabular format.'''
    
    if format == "table":
        
        
        i = 0
        for table,content in db['tables'].items():
            
            i = i+1
                            
            head = PrettyTable(["{}".format(clr.white(str(i))),
                            "{}: {}".format(clr.red("Table Name"),clr.white(table)),
                            "{}: {}".format(clr.red("Columns"),clr.white(content['col_count'])),
                            "{}: {}".format(clr.red("Rows"),clr.white(content['row_count']))
                            ])
        
            body = render_cols(content['cols'])
            
            print(head)
            
            print(body)
    
    
    else:

        for table,content in db['tables'].items():
            
            print("\n{table}: {table_info}\t{column}: {column_info}\t{rows}: {rows_info}" \
            .format(table=clr.red("Table Name"),table_info=clr.white(table),
            column=clr.red("Columns"),column_info=clr.white(content['col_count']),
            rows=clr.red("Rows"),rows_info=clr.white(content['row_count'])))
            
            print(clr.yellow("COLUMNS:"))
            
            for col in content['cols']:
            
                print(clr.yellow("\t{}".format(col)))