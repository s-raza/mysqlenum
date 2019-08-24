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

import os
from MySQLEnum import *
from Formatting import *
from builtins import input
import json

def construct_data(post_args, vuln_field):
    '''Construct the data that will be sent as a part of the GET or POST request to the target. One of these fields is specified as being vulnerable in the command line arguments, on which the SQL injection will be done.'''
    retval = {}
    
    if ":" not in post_args:

        print(clr.red("\n[!]") + "At least one parameter value must be set or if there is no parameter it should be left blank (E.g. -d 'param1:')\n   Exiting ...\n".format(vuln_field))
        exit(0)
    
    for i in post_args.split(","):
        
        param = i.split(":")
        retval[param[0]] = param[1]
        
    
    if vuln_field not in retval:
        
        print(clr.red("\n[!]") + "Vulnerable field '{}' not found in provided post arguments... exiting\n".format(vuln_field))
        exit(1)
    
    return retval

def show_enum_rows_option(target):
    '''Prompt if the user wishes to enumerate rows'''
        
    while True:
    
        if enumerate_rows(target):
        
            msg = "Enumerate rows? [y/n, default:n]: "
            
            again = input(msg)
                
            if again == "n":
                
                break
                
        else:
            
            break
    
def enumerate_rows(target):
    '''Present the options and prompts for selecting tables, columns, number of rows to enumerate'''

    enumerated_rows = []
    
    selected_table = select_table(target)
    num_rows = target.DB['tables'][selected_table]['row_count']
    
    print("\nTable selected: {} {}\n".format(clr.red(selected_table),clr.yellow("({} rows)".format(num_rows))))
    
    selected_col = select_col(target, selected_table)
    
    selected_limit = select_row_limit(target, selected_table, selected_col)
    
    print("\nColumn selected: {}\n".format(clr.red(selected_col)))
    
    print("\nEnumerating rows for {}.{}\n".format(clr.red(selected_table), clr.red(selected_col)))
    
    try:
        
        curr_rows = target.get_curr_enum_rows(selected_table,selected_col)
        
        if selected_limit == len(curr_rows):
                
            print(render_rows(curr_rows,selected_col))

        else:
            
            if len(curr_rows) > 0:
                    
                enumerated_rows = enumerated_rows + curr_rows
        
            rows = target.generate_rows(selected_col, selected_table, selected_limit)
            
            for row in rows:
                
                enumerated_rows.append(row)
                
            print(render_rows(enumerated_rows,selected_col))
            
        if(len(target.get_long_rows_for_table_col(selected_table, selected_col)) > 0):

            if input("Long rows present, enumerate them? [y/n, default:n]: ") in ['y','']:
                enumerate_long_rows(target, selected_table, selected_col)            

        return True
        
    except KeyboardInterrupt:
    
        print("\nRow enumeration aborted, partial enumeration results for {}.{}:\n".format(clr.red(selected_table),clr.red(selected_col)))
        
        print(render_rows(enumerated_rows,selected_col))
        
        if input("Continue enumerating rows for other tables? [y/n, default:n]: ") == 'y':
            enumerate_rows(target)
        else:
            return False

def select_long_row(target, table, col, long_row_list):
    '''Prompt for selecting the long row, to enumerate it's complete contents'''
    
    print(render_long_rows(target.DB['tables'], table,col, long_row_list))
    
    while True:
    
        long_row = int(input("Select the row to enumerate it's complete contents [{}-{}]: ".format("1",len(long_row_list))))
        
        if long_row > 0 and long_row <= len(long_row_list):
        
            break
            
    long_row = long_row_list[long_row-1]
    
    return long_row

def enumerate_long_rows(target, table, col):
       '''Enumerate the complete contents of a selected long row'''

       long_row_list = target.get_long_rows_for_table_col(table,col)
       
       selected_long_row = select_long_row(target, table, col, long_row_list)

       full_content = target.get_long_row_content(str(selected_long_row), table, col)

       target.DB['tables'][table]['cols'][col][selected_long_row][0] = str(len(full_content))

       target.DB['tables'][table]['cols'][col][selected_long_row][1] = full_content

       target.long_rows[table][col].remove(selected_long_row)

       print("\nContents for '{}.{}[{}]':\n{}\n".format(table, col, selected_long_row, full_content))


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

def get_file_name(url):
    '''Get the name of the json file that was saved for a particular url'''
    
    file = '-'.join(url.split('/')[2:])
    
    return './{}.json'.format(file)

def show_results(target):
    '''Print enumeration results'''
    
    print_db_info(target.DB, format="table")
       
    print(clr.yellow("\nENUMERATED TABLES FOR: {}\n".format(clr.red(target.DB['params']['target_url']))))
    
    print_table_info(target.DB, format="table")

def set_params(kwargs, params_from_file):
    '''Set commandline parameters provided with the -f switch. If a parameter is provided it is used, otherwise it is taken from the json file saved earlier.'''
    
    retval = {}
    
    for key,val in kwargs.items():
        
        if val is not None:
            retval[key] = val
        else:
            retval[key] = params_from_file[key]
    
    return retval

def start(*args,**kwargs):
    '''Main program loop'''

    file_read = kwargs['file_read']

    args_init = dict(kwargs)
    
    del args_init['file_read']
    
    file_name = get_file_name(kwargs['target_url'])
    
    if file_read:

        if os.path.isfile(file_name):
            
            with open(file_name, 'r') as f:
                db = json.load(f)

            args_init = set_params(args_init, db['params'])
            
            target = MYSQLENUM(args_init)

            target.DB = db
            
            target.DB['params'] = args_init

            target.populate_long_rows()
            
            # enumerate_rows(target)
            show_enum_rows_option(target)
            
            
                
        else:
            
            print(clr.red("\n[!]") + "File '{}' not found for URL: {}\n   Exiting ...\n".format(file_name,url))
            exit(1)

    else:
    
        kwargs['data'] = construct_data(kwargs['data'], kwargs['vuln_field'])
        
        print(clr.red("\nENUMERATING DATABASE ...\n"))
       
        target = MYSQLENUM(kwargs)
        
        target.enumerate()
        
        show_results(target)
        
        show_enum_rows_option(target)
    
    with open(file_name, 'w') as fp:
        json.dump(target.DB, fp, indent=4)
