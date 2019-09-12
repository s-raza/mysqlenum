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
from Main import start
from Tools.ScreenColors import clr

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

if __name__ == '__main__':

    show_banner()

    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file_read", help="Read in previously enumerated file", action="store_true")
    parser.add_argument("-debug","--debug", help="Show debug messages : Use d=DEBUG, w=WARNING, i=INFO, e=ERROR, c=CRITICAL")
    parser.add_argument("-u","--target_url", help="Full path to the vulnerable URL", required=True)
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
            
    start(target_url=args.target_url,
        data=args.data,
        vuln_field=args.vuln_field,
        table_limit=args.table_limit,
        debug=args.debug,
        terminator=args.terminator,
        request_type=args.request_type,
        file_read=args.file_read)

